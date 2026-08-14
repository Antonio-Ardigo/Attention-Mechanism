#!/usr/bin/env python3
"""Fetch a timestamped transcript for a source video, using open-source tooling.

Training material in this repo cites video sources. This pulls those sources down
so claims can be checked against what was actually said, rather than against
someone's memory of it.

    python3 tools/fetch_transcript.py UPtG_38Oq8o
    python3 tools/fetch_transcript.py 'https://youtu.be/UPtG_38Oq8o' --lang en

Writes two files into --out (default: sources/):

    <id>.transcript.md   timestamped transcript      (git-ignored - see sources/README.md)
    <id>.meta.json       title, author, duration     (committed)

and refreshes the citation table in sources/index.md.

Captions come from yt-dlp. Manual captions are preferred over auto-generated ones;
which was used is recorded in the metadata, because auto-generated captions
mistranscribe technical terms and material quoting them should say so.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
INDEX_START = "<!-- sources:start -->"
INDEX_END = "<!-- sources:end -->"


def die(message: str, hint: str | None = None) -> None:
    print(f"error: {message}", file=sys.stderr)
    if hint:
        print(f"hint:  {hint}", file=sys.stderr)
    raise SystemExit(1)


def load_yt_dlp():
    try:
        import yt_dlp  # noqa: PLC0415
    except ImportError:
        die(
            "yt-dlp is not installed",
            "pip3 install -r tools/requirements.txt",
        )
    return yt_dlp


def parse_video_id(value: str) -> str:
    """Accept a bare ID, a youtu.be link, or any youtube.com URL carrying v=."""
    if VIDEO_ID_RE.match(value):
        return value
    match = re.search(r"(?:v=|/shorts/|youtu\.be/|/embed/)([A-Za-z0-9_-]{11})", value)
    if match:
        return match.group(1)
    die(f"could not find a video id in {value!r}", "pass an 11-character id or a full YouTube URL")


def timestamp(seconds: float) -> str:
    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def pick_subtitles(info: dict, lang: str) -> tuple[str, bool]:
    """Return (subtitle track key, is_automatic). Prefer manual captions."""
    for track, automatic in ((info.get("subtitles") or {}), False), ((info.get("automatic_captions") or {}), True):
        if lang in track:
            return lang, automatic
        for key in track:
            if key.split("-")[0] == lang:
                return key, automatic
    die(
        f"no {lang!r} captions available for this video",
        "try --lang with another code, or --whisper to transcribe the audio instead",
    )


def download_json3(ydl_class, url: str, sub_lang: str, automatic: bool, workdir: Path) -> Path:
    options = {
        "skip_download": True,
        "writesubtitles": not automatic,
        "writeautomaticsub": automatic,
        "subtitleslangs": [sub_lang],
        "subtitlesformat": "json3",
        "outtmpl": str(workdir / "%(id)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
    }
    with ydl_class(options) as ydl:
        ydl.download([url])
    files = sorted(workdir.glob("*.json3"))
    if not files:
        die(
            "yt-dlp reported captions but downloaded none",
            "YouTube throttles caption requests from datacenter IPs; retry from a normal network "
            "or drop a transcript into sources/ by hand (see tools/README.md)",
        )
    return files[0]


def segments_from_json3(path: Path) -> list[tuple[float, str]]:
    """Flatten json3 caption events into (start_seconds, text) pairs."""
    data = json.loads(path.read_text(encoding="utf-8"))
    segments: list[tuple[float, str]] = []
    for event in data.get("events", []):
        pieces = event.get("segs") or []
        text = "".join(piece.get("utf8", "") for piece in pieces)
        text = text.replace("\n", " ").strip()
        if not text:
            continue
        start = event.get("tStartMs", 0) / 1000.0
        segments.append((start, text))
    return segments


def group_into_paragraphs(segments, seconds_per_block: float = 30.0):
    """Group caption fragments into readable blocks with one timestamp each.

    Auto-generated captions arrive as two- or three-word fragments, which are
    unreadable and useless for citation. Blocks of roughly half a minute give a
    timestamp precise enough to find the moment in the video and prose long
    enough to actually read.
    """
    blocks: list[tuple[float, str]] = []
    block_start: float | None = None
    words: list[str] = []

    for start, text in segments:
        if block_start is None:
            block_start = start
        words.append(text)
        if start - block_start >= seconds_per_block:
            blocks.append((block_start, " ".join(words)))
            block_start, words = None, []

    if words and block_start is not None:
        blocks.append((block_start, " ".join(words)))

    return [(start, re.sub(r"\s+", " ", text).strip()) for start, text in blocks]


def write_transcript(path: Path, info: dict, blocks, sub_lang: str, automatic: bool) -> None:
    kind = "auto-generated" if automatic else "manual"
    lines = [
        f"# {info.get('title', 'Untitled')}",
        "",
        f"- **Author:** {info.get('uploader', 'unknown')}",
        f"- **Source:** {info.get('webpage_url', '')}",
        f"- **Duration:** {timestamp(info.get('duration') or 0)}",
        f"- **Captions:** {sub_lang} ({kind})",
        f"- **Retrieved:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        "",
        "> Transcript of a third-party video, retrieved for citation and fact-checking.",
        "> Not committed to git. See `sources/README.md`.",
        "",
        "---",
        "",
    ]
    for start, text in blocks:
        lines.append(f"**[{timestamp(start)}]** {text}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_meta(path: Path, info: dict, sub_lang: str, automatic: bool, block_count: int) -> dict:
    meta = {
        "id": info.get("id"),
        "title": info.get("title"),
        "author": info.get("uploader"),
        "url": info.get("webpage_url"),
        "duration_seconds": info.get("duration"),
        "upload_date": info.get("upload_date"),
        "caption_language": sub_lang,
        "caption_kind": "automatic" if automatic else "manual",
        "transcript_blocks": block_count,
        "retrieved": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }
    path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return meta


def refresh_index(out_dir: Path) -> None:
    """Rebuild the citation table in sources/index.md from every *.meta.json."""
    index_path = out_dir / "index.md"
    rows = []
    for meta_file in sorted(out_dir.glob("*.meta.json")):
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
        rows.append(
            "| {title} | {author} | {duration} | {kind} | {retrieved} | [{id}]({url}) |".format(
                title=meta.get("title", ""),
                author=meta.get("author", ""),
                duration=timestamp(meta.get("duration_seconds") or 0),
                kind=meta.get("caption_kind", ""),
                retrieved=meta.get("retrieved", ""),
                id=meta.get("id", ""),
                url=meta.get("url", ""),
            )
        )

    table = "\n".join(
        [
            "| Title | Author | Length | Captions | Retrieved | Source |",
            "| --- | --- | --- | --- | --- | --- |",
            *rows,
        ]
    )
    block = f"{INDEX_START}\n{table}\n{INDEX_END}"

    if index_path.exists():
        current = index_path.read_text(encoding="utf-8")
        if INDEX_START in current and INDEX_END in current:
            head, rest = current.split(INDEX_START, 1)
            _, tail = rest.split(INDEX_END, 1)
            index_path.write_text(f"{head}{block}{tail}", encoding="utf-8")
            return

    index_path.write_text(
        "# Source index\n\n"
        "Videos cited by the training material in this repository. Transcripts themselves\n"
        "are git-ignored; this table is the committed record of what was consulted.\n\n"
        "Regenerate with `python3 tools/fetch_transcript.py <video>`.\n\n"
        f"{block}\n",
        encoding="utf-8",
    )


def transcribe_with_whisper(url: str, out_dir: Path, video_id: str):
    """Optional fallback for videos with no captions at all.

    Documented but not exercised in CI: it needs ffmpeg on PATH and downloads a
    model on first run.
    """
    if shutil.which("ffmpeg") is None:
        die(
            "--whisper needs ffmpeg on PATH",
            "install ffmpeg (apt install ffmpeg / brew install ffmpeg), or drop the --whisper flag "
            "to use the video's own captions",
        )
    try:
        from faster_whisper import WhisperModel  # noqa: PLC0415
    except ImportError:
        die(
            "faster-whisper is not installed",
            "pip3 install 'faster-whisper>=1.0'",
        )

    yt_dlp = load_yt_dlp()
    audio_path = out_dir / f"{video_id}.raw.m4a"
    options = {
        "format": "bestaudio/best",
        "outtmpl": str(audio_path.with_suffix("")) + ".%(ext)s",
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

    downloaded = next(out_dir.glob(f"{video_id}.raw.*"), None)
    if downloaded is None:
        die("audio download produced no file")

    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(str(downloaded))
    return [(segment.start, segment.text.strip()) for segment in segments]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch a timestamped transcript for a source video.",
        epilog="Transcripts are third-party content and stay git-ignored; see sources/README.md.",
    )
    parser.add_argument("video", help="YouTube video id or URL")
    parser.add_argument("--lang", default="en", help="caption language code (default: en)")
    parser.add_argument("--out", default="sources", type=Path, help="output directory (default: sources)")
    parser.add_argument(
        "--block-seconds",
        type=float,
        default=30.0,
        help="approximate seconds of speech per timestamped block (default: 30)",
    )
    parser.add_argument(
        "--whisper",
        action="store_true",
        help="transcribe the audio locally instead of using captions (needs ffmpeg + faster-whisper)",
    )
    args = parser.parse_args()

    video_id = parse_video_id(args.video)
    url = f"https://www.youtube.com/watch?v={video_id}"
    out_dir: Path = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    yt_dlp = load_yt_dlp()
    print(f"fetching metadata for {video_id} ...")
    try:
        with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True, "skip_download": True}) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as exc:  # yt-dlp raises a wide range of network/extractor errors
        die(
            f"could not read video metadata: {exc}",
            "check the id, or see tools/README.md for the manual transcript path",
        )

    print(f"  {info.get('title')} — {info.get('uploader')} ({timestamp(info.get('duration') or 0)})")

    if args.whisper:
        print("transcribing audio with faster-whisper ...")
        segments = transcribe_with_whisper(url, out_dir, video_id)
        sub_lang, automatic = f"{args.lang} (whisper)", True
    else:
        sub_lang, automatic = pick_subtitles(info, args.lang)
        kind = "auto-generated" if automatic else "manual"
        print(f"downloading {kind} captions [{sub_lang}] ...")
        with tempfile.TemporaryDirectory() as tmp:
            json3 = download_json3(yt_dlp.YoutubeDL, url, sub_lang, automatic, Path(tmp))
            segments = segments_from_json3(json3)

    if not segments:
        die("transcript came back empty")

    blocks = group_into_paragraphs(segments, args.block_seconds)

    transcript_path = out_dir / f"{video_id}.transcript.md"
    meta_path = out_dir / f"{video_id}.meta.json"
    write_transcript(transcript_path, info, blocks, sub_lang, automatic)
    write_meta(meta_path, info, sub_lang, automatic, len(blocks))
    refresh_index(out_dir)

    words = sum(len(text.split()) for _, text in blocks)
    print(f"wrote {transcript_path} ({len(blocks)} blocks, ~{words} words)")
    print(f"wrote {meta_path}")
    print(f"updated {out_dir / 'index.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
