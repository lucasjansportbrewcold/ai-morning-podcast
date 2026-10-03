# Morning Signal

Een privé dagelijkse AI-podcast voor op de fiets: twee hosts (Mia, AI-builder, en George, tech-expert)
bespreken het AI-nieuws en één verdieping, afgestemd op [mijn profiel](prompts/profile.md).

## Hoe het werkt

`run.py` draait elke ochtend op mijn laptop en doorloopt vijf stappen:

| Stap | Wat | Waarmee |
|---|---|---|
| `collect` | Nieuwe items uit RSS-feeds en YouTube-transcripten ([sources.yaml](sources.yaml)) | Python, geen AI |
| `research` | Selecteert nieuws, controleert bronnen, kiest en onderzoekt een deep dive → `notes.md` | `claude -p` met Read, Write, WebSearch, WebFetch |
| `write` | Schrijft het gesprek → `script.txt` + `episode.json` | `claude -p` met alleen Read en Write, geen web |
| `tts` | Zet het script om naar mp3 | Kokoro (lokaal, gratis) |
| `publish` | mp3 als GitHub Release, feed in `docs/feed.xml`, commit + push | `gh`, `git` |

Werkdagen: nieuws plus deep dive. Weekend: alleen een deep dive.

### Veiligheid

Feeds en webpagina's zijn onbetrouwbare tekst (prompt injection). Daarom:
- De Claude-stappen mogen alleen lezen in `prompts/` en de werkmap van vandaag, alleen schrijven in de
  werkmap, en hebben geen shell, geen MCP-servers en niet mijn globale CLAUDE.md.
- De schrijver heeft geen webtoegang en mag alleen feiten uit de gecontroleerde notities gebruiken.
- Publiceren (`gh`, `git push`) doet het Python-script, nooit Claude.

## Gebruik

```bash
.venv/Scripts/python run.py                    # aflevering van vandaag
.venv/Scripts/python run.py --from-step tts    # hervatten na een fout
.venv/Scripts/python run.py --no-publish       # wel maken, niet publiceren
```

Logs staan in `logs/<datum>.log`, tussenbestanden in `work/<datum>/` (beide niet in git).

## Installatie

```bash
uv venv -p 3.11 .venv
uv pip install -p .venv -r requirements.txt
mkdir models
curl -L -o models/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -L -o models/voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```

Daarnaast nodig: `ffmpeg`, `gh` (ingelogd) en `claude` (ingelogd) op het PATH.

## Luisteren

Abonneer in een podcast-app (bijv. AntennaPod) op:
`https://lucasjansportbrewcold.github.io/ai-morning-podcast/feed.xml`
