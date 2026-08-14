# tools/

Open-source tooling for sourcing the training material.

## fetch_transcript.py

Pulls a timestamped transcript for a video so claims in the training documents can be checked against what was actually said.

```bash
pip3 install -r tools/requirements.txt

python3 tools/fetch_transcript.py UPtG_38Oq8o
python3 tools/fetch_transcript.py 'https://youtu.be/UPtG_38Oq8o' --lang en
```

Writes into `sources/`:

- `<id>.transcript.md` — captions merged into readable blocks, each with an `mm:ss` timestamp. **Git-ignored** (see `sources/README.md`).
- `<id>.meta.json` — title, author, duration, and which kind of captions were used.

and refreshes the citation table in `sources/index.md`.

### Options

| Flag | Default | What it does |
| --- | --- | --- |
| `--lang` | `en` | Caption language code. Falls back to any regional variant (`en-GB`, `en-US`). |
| `--out` | `sources` | Output directory. |
| `--block-seconds` | `30` | Roughly how much speech goes into each timestamped block. Lower it for finer citations, raise it for more readable prose. |
| `--whisper` | off | Transcribe the audio locally instead of using captions. |

### Manual and auto-generated captions

Manual captions are preferred and the choice is recorded in the metadata as `caption_kind`. This matters: auto-generated captions mistranscribe technical vocabulary — "queries" becomes "query is", matrix names get mangled — so anything quoting them should be checked against the audio before it is presented as a quotation.

### The Whisper fallback

`--whisper` downloads the audio and transcribes it with [faster-whisper](https://github.com/SYSTRAN/faster-whisper). It exists for videos with no captions at all.

It needs `ffmpeg` on `PATH` and `pip3 install 'faster-whisper>=1.0'`, and it downloads a model on first run. **This path ships documented but unexercised** — the container this was developed in has no ffmpeg, so it has not been run end to end. The flag checks for ffmpeg up front and fails with an actionable message rather than part way through.

### When YouTube blocks the fetch

YouTube rejects requests from datacenter IP ranges:

```
ERROR: [youtube] <id>: Sign in to confirm you're not a bot.
```

This is not a bug in the tool — it is where the request came from. Options, in order of preference:

1. Run it from an ordinary network connection.
2. Pass cookies from a signed-in browser, per the [yt-dlp FAQ](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp).
3. Record the source by hand — write `sources/<id>.meta.json` with `"retrieval_method": "manual"` and a `retrieval_note` saying where the material actually came from, then regenerate the index:

   ```bash
   python3 -c "import sys; sys.path.insert(0,'tools'); \
     from fetch_transcript import refresh_index; from pathlib import Path; \
     refresh_index(Path('sources'))"
   ```

The tool never writes a partial or invented transcript when a fetch fails. A citation you cannot trust is worse than no citation.
