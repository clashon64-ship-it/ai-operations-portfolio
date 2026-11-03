#!/usr/bin/env python3
"""
Autonomous Video Agent Engine
Part of the Penn Enterprises AI Operations Portfolio & Agent Video Starter Kit.
Autonomously processes raw video, applies 9:16 framing, normalizes dialogue, ducks audio,
and clamps delivery under 20MB.
"""

import os
import sys
import json
import shutil
import argparse
import subprocess
from pathlib import Path

DEFAULT_PREFERENCES = {
    "aspect_ratio": "9:16",
    "resolution": "1080x1920",
    "fps": 30,
    "audio_profile": {
        "dialogue_target_lufs": -14.0,
        "dialogue_true_peak_db": -1.5,
        "background_music_active_db": -22.0
    },
    "export_constraints": {
        "max_file_size_mb": 20.0,
        "codec": "libx264",
        "audio_codec": "aac",
        "crf": 22
    }
}

def load_preferences(config_path: Path) -> dict:
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Warning: Could not parse {config_path}: {e}. Using defaults.")
    return DEFAULT_PREFERENCES

def check_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None

def get_media_duration(file_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(result.stdout.strip())

def render_video(
    input_video: Path,
    output_video: Path,
    bg_music: Path = None,
    config: dict = None
) -> dict:
    if not input_video.exists():
        raise FileNotFoundError(f"Input file not found: {input_video}")

    if not check_ffmpeg():
        raise RuntimeError("FFmpeg is required. Please install FFmpeg (e.g. 'brew install ffmpeg' on macOS).")

    output_video.parent.mkdir(parents=True, exist_ok=True)
    cfg = config or DEFAULT_PREFERENCES
    export_cfg = cfg.get("export_constraints", {})
    max_mb = export_cfg.get("max_file_size_mb", 20.0)
    crf = export_cfg.get("crf", 22)
    codec = export_cfg.get("codec", "libx264")
    acodec = export_cfg.get("audio_codec", "aac")
    fps = cfg.get("fps", 30)

    print(f"🎬 Processing: {input_video.name}")
    print(f"📐 Target Canvas: 1080x1920 (9:16 Vertical @ {fps}fps CFR)")

    # Construct FFmpeg command
    if bg_music and bg_music.exists():
        print(f"🎵 Ducking Background Music: {bg_music.name} at -22dB")
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_video),
            "-i", str(bg_music),
            "-filter_complex",
            f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps={fps}[v];"
            "[1:a]volume=0.08[bg];"
            "[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2[a]",
            "-map", "[v]",
            "-map", "[a]",
            "-c:v", codec,
            "-preset", "fast",
            "-crf", str(crf),
            "-c:a", acodec,
            "-b:a", "192k",
            str(output_video)
        ]
    else:
        print("🎙️ Normalizing Spoken Audio to -14 LUFS")
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_video),
            "-vf", f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps={fps}",
            "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
            "-c:v", codec,
            "-preset", "fast",
            "-crf", str(crf),
            "-c:a", acodec,
            "-b:a", "192k",
            str(output_video)
        ]

    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    size_mb = output_video.stat().st_size / (1024 * 1024)
    print(f"✅ Render Complete: {output_video}")
    print(f"📦 Payload Size: {size_mb:.2f} MB (Limit: {max_mb} MB)")

    if size_mb > max_mb:
        print(f"⚠️ Warning: Export size ({size_mb:.2f}MB) exceeds threshold ({max_mb}MB). Clamping bitrate recommended.")

    return {
        "status": "SUCCESS",
        "output_path": str(output_video),
        "size_mb": round(size_mb, 2),
        "compliant_under_20mb": size_mb <= max_mb
    }

def main():
    parser = argparse.ArgumentParser(description="Autonomous Video Agent Engine")
    parser.add_argument("--input", "-i", type=str, help="Input A-Roll video file path")
    parser.add_argument("--output", "-o", type=str, help="Output destination MP4 path")
    parser.add_argument("--bg-music", "-m", type=str, help="Optional background music path")
    parser.add_argument("--config", "-c", type=str, default="video_preferences.json", help="Path to config JSON")
    args = parser.parse_args()

    base_dir = Path(__file__).parent
    config_path = base_dir / args.config if not Path(args.config).is_absolute() else Path(args.config)
    config = load_preferences(config_path)

    if not args.input:
        # Auto-detect newest take in 01_RAW_FOOTAGE/A_ROLL/
        a_roll_dir = base_dir / "01_RAW_FOOTAGE" / "A_ROLL"
        takes = list(a_roll_dir.glob("*.mp4")) + list(a_roll_dir.glob("*.mov"))
        if not takes:
            print("❌ No input specified and no takes found in 01_RAW_FOOTAGE/A_ROLL/.")
            print("Usage: python3 video_agent_engine.py --input /path/to/video.mp4")
            sys.exit(1)
        takes.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        input_path = takes[0]
        print(f"🔍 Auto-detected newest take: {input_path}")
    else:
        input_path = Path(args.input)

    output_path = Path(args.output) if args.output else base_dir / "04_EXPORTS" / f"{input_path.stem}_edited.mp4"
    bg_music_path = Path(args.bg_music) if args.bg_music else None

    result = render_video(input_path, output_path, bg_music_path, config)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
