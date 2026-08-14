# sources/

Videos and other third-party material the training documents are built from.

## What lives here

| Committed | File | Why |
| --- | --- | --- |
| yes | `index.md` | Citation table — what was consulted, by whom, when |
| yes | `<id>.meta.json` | Title, author, duration, caption provenance |
| **no** | `<id>.transcript.md` | The transcript itself |
| **no** | `*.raw.*`, `*.vtt`, `*.srt`, `*.json3` | Intermediate caption/audio downloads |

## Why transcripts are not committed

A transcript is a near-complete reproduction of someone else's video. Publishing one in a repository republishes their work, which is not ours to do. The training material quotes short passages for commentary and study and cites the source; the full text stays on whoever's machine fetched it.

Everything a reader needs in order to check a claim — title, author, link, retrieval date — is in `index.md`, which *is* committed. Anyone can regenerate the transcript locally:

```bash
pip3 install -r tools/requirements.txt
python3 tools/fetch_transcript.py <video-id>
```

## When the fetch is blocked

YouTube rejects caption requests from datacenter IP ranges with *"Sign in to confirm you're not a bot"*. If you hit that, the tool exits with a clear error rather than writing a partial file. Either run it from an ordinary network connection, or record the source by hand: write a `<id>.meta.json` following the shape of the existing ones, set `"retrieval_method": "manual"`, and say in `retrieval_note` where the material actually came from. `UPtG_38Oq8o.meta.json` is an example of exactly that case.

Never fill in a `meta.json` with details you have not verified. The point of this directory is that a reader can trust the citation.
