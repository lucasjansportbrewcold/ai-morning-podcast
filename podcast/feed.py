"""Build the podcast RSS feed (docs/feed.xml) from episodes/*/episode.json."""

import json
from datetime import datetime
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

MAX_EPISODES = 60


def load_episodes(episodes_dir: Path) -> list[dict]:
    episodes = []
    for path in sorted(episodes_dir.glob("*/episode.json"), reverse=True):
        ep = json.loads(path.read_text(encoding="utf-8"))
        if ep.get("audio_url"):
            episodes.append(ep)
    return episodes[:MAX_EPISODES]


def _duration(seconds: float) -> str:
    s = int(round(seconds))
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"


def build_feed(podcast: dict, episodes: list[dict]) -> str:
    items = []
    for ep in episodes:
        pub = format_datetime(datetime.fromisoformat(ep["published"]))
        description = ep["summary"] + "\n\n" + ep.get("shownotes", "")
        items.append(f"""    <item>
      <title>{escape(ep["title"])}</title>
      <description>{escape(description)}</description>
      <pubDate>{pub}</pubDate>
      <guid isPermaLink="false">{escape(ep["guid"])}</guid>
      <enclosure url="{escape(ep["audio_url"])}" length="{ep["audio_bytes"]}" type="audio/mpeg"/>
      <itunes:duration>{_duration(ep["duration_seconds"])}</itunes:duration>
      <itunes:episodeType>full</itunes:episodeType>
    </item>""")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>{escape(podcast["title"])}</title>
    <link>{escape(podcast["base_url"])}/</link>
    <description>{escape(podcast["description"])}</description>
    <language>{podcast["language"]}</language>
    <itunes:author>{escape(podcast["author"])}</itunes:author>
    <itunes:block>Yes</itunes:block>
    <itunes:explicit>false</itunes:explicit>
{chr(10).join(items)}
  </channel>
</rss>
"""


def write_feed(podcast: dict, episodes_dir: Path, docs_dir: Path) -> int:
    episodes = load_episodes(episodes_dir)
    docs_dir.mkdir(exist_ok=True)
    (docs_dir / "feed.xml").write_text(build_feed(podcast, episodes), encoding="utf-8")
    return len(episodes)
