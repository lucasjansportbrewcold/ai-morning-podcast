"""Make and publish one episode of Morning Signal.

Steps: collect -> research (Claude) -> write (Claude) -> tts -> publish.
Usage:
    python run.py                      # today's episode, all steps
    python run.py --date 2026-10-03    # a specific date
    python run.py                      # rerun after a failure: resumes at the step that failed
    python run.py --from-step tts      # force a restart from a specific step
    python run.py --no-publish         # make the mp3 but don't upload or push
"""

import argparse
import json
import logging
import os
import re
import shutil
import subprocess
import sys
from datetime import date as Date, datetime, timedelta
from pathlib import Path

import yaml

from podcast import collect, feed, tts

ROOT = Path(__file__).resolve().parent
STEPS = ["collect", "research", "write", "tts", "publish"]
HISTORY_DAYS = 14

log = logging.getLogger("morning-signal")

MODE_INSTRUCTIONS = {
    "weekday": (
        "1. Select the 3 to 5 news items most relevant to the listener. Three strong items beat five weak ones.\n"
        "   Include one item on AI for (economic) research or the economics of AI whenever there is a\n"
        "   worthwhile one (new papers, data, evidence); search for it if the feeds have none.\n"
        "2. Choose one deep-dive topic that is not in the past deep-dive list. It may grow out of today's news\n"
        "   or come from the listener's interests (techniques, architectures, AI for research, Dutch business\n"
        "   opportunities). Research it properly: mechanisms, trade-offs, concrete examples."
    ),
    "weekend": (
        "No news section today (write 'None (weekend)' under ## News).\n"
        "Choose one deep-dive topic that is not in the past deep-dive list and research it thoroughly enough\n"
        "for a full episode. On Saturdays prefer a technique or architecture; on Sundays prefer AI for research,\n"
        "the economics of AI, or concrete business/automation ideas in a Dutch context."
    ),
}
STRUCTURE = {
    "weekday": (
        "Short greeting, then the news (about 45% of the length), then a natural transition into the\n"
        "deep dive (about 55%), then a one-line sign-off for the bike ride."
    ),
    "weekend": (
        "Short greeting, then the whole episode is the deep dive, structured as a conversation that builds up\n"
        "step by step, then a one-line sign-off."
    ),
}


def load_yaml(name: str) -> dict:
    return yaml.safe_load((ROOT / name).read_text(encoding="utf-8"))


def episode_dirs(before: Date) -> list[Path]:
    dirs = sorted(p for p in (ROOT / "episodes").glob("*") if p.is_dir() and p.name < before.isoformat())
    return dirs


def build_history(day: Date) -> tuple[str, set[str]]:
    """Recent episode topics and past deep dives (for the researcher), plus URLs already collected."""
    recent_cutoff = (day - timedelta(days=HISTORY_DAYS)).isoformat()
    recent, deep_dives, seen = [], [], set()
    for d in episode_dirs(day):
        meta_path = d / "episode.json"
        if not meta_path.exists():
            continue
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if meta.get("deep_dive"):
            deep_dives.append(f"- {d.name}: {meta['deep_dive']}")
        if d.name >= recent_cutoff:
            recent.append(f"### {d.name}: {meta.get('title', '')}\n{meta.get('shownotes', '').split('Sources')[0].strip()}")
            urls = d / "collected_urls.txt"
            if urls.exists():
                seen.update(u for u in urls.read_text(encoding="utf-8").splitlines() if u)
    text = "# History\n\n## Recent episodes\n\n" + ("\n\n".join(recent) or "(none yet)")
    text += "\n\n## Past deep-dive topics\n\n" + ("\n".join(deep_dives) or "(none yet)") + "\n"
    return text, seen


def run_claude(prompt: str, tools: list[str], allowed: list[str], model: str, timeout_min: int,
               mcp_servers: dict | None = None) -> None:
    exe = shutil.which("claude")
    if not exe:
        raise RuntimeError("claude CLI not found on PATH")
    cmd = [exe, "-p", "--model", model, "--output-format", "json",
           "--tools", ",".join(tools), "--allowedTools", *allowed,
           "--permission-mode", "dontAsk", "--setting-sources", "project",
           "--strict-mcp-config", "--mcp-config", json.dumps({"mcpServers": mcp_servers or {}})]
    # Keep the user's global CLAUDE.md out of the podcast agent's context.
    env = {**os.environ, "CLAUDE_CODE_DISABLE_CLAUDE_MDS": "1"}
    result = subprocess.run(cmd, input=prompt, cwd=ROOT, env=env, capture_output=True,
                            text=True, encoding="utf-8", timeout=timeout_min * 60)
    try:
        out = json.loads(result.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"claude exit {result.returncode}: {result.stderr[-1000:] or result.stdout[-1000:]}")
    log.info("claude: %s turns, %.0fs, result=%r", out.get("num_turns"), out.get("duration_ms", 0) / 1000,
             str(out.get("result", ""))[:80])
    if out.get("is_error") or result.returncode != 0:
        raise RuntimeError(f"claude failed: {str(out.get('result'))[:1000]}")


def resume_step(workdir: Path) -> str:
    """First step whose output is missing, so a second scheduled run picks up where a failed one stopped."""
    if (workdir / "audio.json").exists():
        return "publish"
    if (workdir / "script.txt").exists() and (workdir / "episode.json").exists():
        return "tts"
    if (workdir / "notes.md").exists():
        return "write"
    if (workdir / "collected.md").exists():
        return "research"
    return "collect"


def fill(template: str, **values) -> str:
    return (ROOT / "prompts" / template).read_text(encoding="utf-8").format(**values)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=Date.today().isoformat())
    parser.add_argument("--from-step", choices=STEPS,
                        help="default: resume after the last step that finished")
    parser.add_argument("--no-publish", action="store_true")
    args = parser.parse_args()

    day = Date.fromisoformat(args.date)
    workdir_rel = f"work/{day.isoformat()}"
    workdir = ROOT / workdir_rel
    workdir.mkdir(parents=True, exist_ok=True)
    (ROOT / "logs").mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(ROOT / "logs" / f"{day.isoformat()}.log", encoding="utf-8"),
                  logging.StreamHandler(sys.stdout)],
    )
    logging.getLogger("phonemizer").setLevel(logging.ERROR)  # harmless per-line word-count warnings

    cfg = load_yaml("config.yaml")
    mode = "weekend" if day.weekday() >= 5 else "weekday"
    weekday = day.strftime("%A")
    mia_voices = cfg["hosts"]["MIA"]["voices"]
    voices = {
        "MIA": (mia_voices[day.toordinal() % len(mia_voices)], cfg["hosts"]["MIA"]["lang"]),
        "GEORGE": (cfg["hosts"]["GEORGE"]["voices"][0], cfg["hosts"]["GEORGE"]["lang"]),
    }
    target_minutes = cfg["episode"]["target_minutes"]
    common = dict(date=day.isoformat(), weekday=weekday, mode=mode, workdir=workdir_rel)
    # Claude may only read the prompts and today's work dir; anything outside the project
    # (credentials, personal files) is denied, so untrusted web content can't exfiltrate it.
    read_rules = ["Read(./prompts/**)", f"Read(./{workdir_rel}/**)"]
    if (ROOT / "episodes" / day.isoformat() / "episode.json").exists() and not args.from_step:
        log.info("episode %s already published, nothing to do", day)
        return 0
    steps = STEPS[STEPS.index(args.from_step or resume_step(workdir)):]
    if args.no_publish:
        steps = [s for s in steps if s != "publish"]
    log.info("episode %s (%s), steps %s, Mia voice %s", day, mode, steps, voices["MIA"][0])

    try:
        if "collect" in steps:
            history, seen = build_history(day)
            (workdir / "history.md").write_text(history, encoding="utf-8")
            n = collect.collect(load_yaml("sources.yaml"), cfg["collect"], seen,
                                datetime.now().astimezone(), workdir, day.isoformat())
            log.info("collected %d items", n)

        if "research" in steps:
            prompt = fill("research.md", **common, mode_instructions=MODE_INSTRUCTIONS[mode])
            # WebFetch can't read PDFs; read_pdf saves a paper's text in the work dir, where Read may open it.
            papers = {"command": sys.executable,
                      "args": [str(ROOT / "podcast" / "pdf_server.py"), str(workdir / "papers")]}
            run_claude(prompt, ["Read", "Write", "WebSearch", "WebFetch"],
                       [*read_rules, f"Edit(./{workdir_rel}/**)", "WebSearch", "WebFetch",
                        "mcp__papers__read_pdf"],
                       cfg["claude"]["model"], cfg["claude"]["timeout_minutes"], {"papers": papers})
            if not (workdir / "notes.md").exists():
                raise RuntimeError("research step did not write notes.md")

        if "write" in steps:
            target_chars = target_minutes * cfg["episode"]["chars_per_minute"]
            prompt = fill("write.md", **common, structure=STRUCTURE[mode], target_minutes=target_minutes,
                          target_chars=target_chars, max_chars=int(target_chars * 1.05))
            # The writer gets no web access: it may only use facts from the checked notes.
            run_claude(prompt, ["Read", "Write"], [*read_rules, f"Edit(./{workdir_rel}/**)"],
                       cfg["claude"]["model"], cfg["claude"]["timeout_minutes"])
            for name in ("script.txt", "episode.json"):
                if not (workdir / name).exists():
                    raise RuntimeError(f"write step did not produce {name}")

        if "tts" in steps:
            turns = tts.parse_script((workdir / "script.txt").read_text(encoding="utf-8"))
            meta = json.loads((workdir / "episode.json").read_text(encoding="utf-8"))
            chars = sum(len(t) for _, t in turns)
            log.info("script: %d turns, %d chars (target %d)", len(turns), chars,
                     target_minutes * cfg["episode"]["chars_per_minute"])
            audio = tts.render(turns, voices, cfg["tts"]["speed"], ROOT / "models")
            seconds = tts.to_mp3(audio, workdir / f"morning-signal-{day.isoformat()}.mp3",
                                 cfg["tts"]["bitrate"], meta["title"], cfg["podcast"]["title"])
            log.info("audio: %.1f minutes", seconds / 60)
            (workdir / "audio.json").write_text(json.dumps({"duration_seconds": seconds}), encoding="utf-8")

        if "publish" in steps:
            publish(day, workdir, cfg, voices["MIA"][0])
    except Exception:
        log.exception("episode %s failed", day)
        return 1
    log.info("episode %s done", day)
    return 0


def publish(day: Date, workdir: Path, cfg: dict, mia_voice: str) -> None:
    podcast = cfg["podcast"]
    repo, tag = podcast["repo"], f"ep-{day.isoformat()}"
    mp3 = workdir / f"morning-signal-{day.isoformat()}.mp3"
    meta = json.loads((workdir / "episode.json").read_text(encoding="utf-8"))

    exists = subprocess.run(["gh", "release", "view", tag, "--repo", repo], capture_output=True).returncode == 0
    if exists:
        subprocess.run(["gh", "release", "upload", tag, str(mp3), "--clobber", "--repo", repo], check=True)
    else:
        subprocess.run(["gh", "release", "create", tag, str(mp3), "--repo", repo,
                        "--title", f"{day.isoformat()}: {meta['title']}", "--notes", meta["summary"]], check=True)

    notes = (workdir / "notes.md").read_text(encoding="utf-8")
    deep_dive = re.search(r"^## Deep dive:\s*(.+)$", notes, re.MULTILINE)
    episode_dir = ROOT / "episodes" / day.isoformat()
    episode_dir.mkdir(parents=True, exist_ok=True)
    for name in ("notes.md", "script.txt", "collected_urls.txt"):
        if (workdir / name).exists():
            shutil.copy(workdir / name, episode_dir / name)
    meta.update({
        "date": day.isoformat(),
        "guid": f"morning-signal-{day.isoformat()}",
        "published": datetime.now().astimezone().isoformat(timespec="seconds"),
        "audio_url": f"https://github.com/{repo}/releases/download/{tag}/{mp3.name}",
        "audio_bytes": mp3.stat().st_size,
        "duration_seconds": json.loads((workdir / "audio.json").read_text())["duration_seconds"],
        "deep_dive": deep_dive.group(1).strip() if deep_dive else "",
        "voices": f"Mia: {mia_voice}, George: {cfg['hosts']['GEORGE']['voices'][0]}",
    })
    meta["shownotes"] = meta.get("shownotes", "") + f"\n\nVoices: {meta['voices']}"
    (episode_dir / "episode.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    count = feed.write_feed(podcast, ROOT / "episodes", ROOT / "docs")
    log.info("feed: %d episodes", count)

    git = ["git", "-C", str(ROOT)]
    subprocess.run([*git, "add", "episodes", "docs"], check=True)
    subprocess.run([*git, "commit", "-q", "-m", f"feat: episode {day.isoformat()}"], check=True)
    subprocess.run([*git, "pull", "-q", "--rebase", "--autostash"], check=True)
    subprocess.run([*git, "push", "-q"], check=True)


if __name__ == "__main__":
    sys.exit(main())
