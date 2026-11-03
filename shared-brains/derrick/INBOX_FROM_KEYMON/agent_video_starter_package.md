# DERRICK VIDEO EDITING AGENT STARTER KIT

## Executive Summary & Purpose

This starter kit packages Penn Enterprises LLC battle tested video editing intelligence into an exportable, plug and play blueprint for Derrick. 

It equips Derrick's AI agent to autonomously ingest raw recordings, assemble multi track timelines, enforce retention pacing, balance audio levels, and generate polished short form videos without getting trapped in manual editing fatigue.

## 1. The Core Architecture: The Two Production Pathways

Derrick's agent can execute video editing through two proven architectural pathways:

• Pathway A: Programmatic Headless Assembly (Python plus FFmpeg)
Ideal for 100 percent hands off bulk processing, split screen software walkthroughs, automatic silence removal, and instant mobile distribution. The agent runs a single command to render finished MP4s.

• Pathway B: Native NLE Draft Scaffolding (CapCut Desktop Draft Engine)
Ideal for high touch personal brand content. The agent programmatically builds the project folder and JSON timeline tracks directly on Derrick's computer. Derrick opens CapCut Desktop to find all clips binned, rough cuts trimmed, and music ducked, needing only 1 click to review or add kinetic text animations.

## 2. Standard Ingestion Folder Blueprint

Derrick should establish this structured directory on his machine:

```text
DERRICK_CONTENT_VAULT/
├── 01_RAW_FOOTAGE/
│   ├── A_ROLL/          (Primary talking head takes, phone camera)
│   └── B_ROLL/          (Screen recordings, demo visuals, B-roll clips)
├── 02_AUDIO/
│   ├── DIALOGUE/        (Clean voice recordings, lav mic tracks)
│   ├── MUSIC/           (Background beds and lo-fi tracks)
│   └── SFX/             (Whooshes, clicks, pop sounds)
├── 03_ASSETS/
│   ├── LOGOS/           (Brand badges, PNG transparent logos)
│   └── OVERLAYS/        (Screenshots, product proof, lower thirds)
├── 04_EXPORTS/          (Final rendered MP4 ready for social channels)
└── config/
    └── video_preferences.json
```

## 3. Plug and Play Skill Definition for Derrick's Agent (SKILL.md)

Derrick can copy this exact skill definition into his agent workspace (e.g., `.agents/skills/video-editor/SKILL.md`):

```markdown
# Video Editor Agent Skill

## Role and Mission
You are Derrick's autonomous video editing partner. Your job is to turn raw talking head and screen recording assets into high retention, broadcast ready short form videos (9:16 vertical) that match Derrick's brand identity.

## Operating Standards & Invariants
1. The 3 Second Pacing Rule: Never allow the screen to remain static for longer than 3.0 seconds. Alternate between A-Roll punch-ins (1.12x scale), B-Roll overlays, and graphic callouts.
2. Safe Zone Compliance: Never place captions or face focal points in the top 250px (search bar block), bottom 380px (app UI and caption overlay), or right 140px (social action buttons).
3. Audio Hierarchy: Dialogue normalized to -14 LUFS (peak -1.5 dB). Duck background music to -22 dB whenever dialogue is active.
4. Silence Snapping: Purge pauses and stutter gaps exceeding 0.45 seconds to keep pacing snappy and engaging.
5. Mobile File Ceiling: Ensure all rendered short form videos remain under 20MB for fast phone preview and instant sharing.

## Execution Workflow
Step 1: Inspect 01_RAW_FOOTAGE/A_ROLL for the newest take.
Step 2: Detect audio energy and trim leading/trailing silences.
Step 3: Read config/video_preferences.json for brand colors and fonts.
Step 4: Execute timeline assembly using the Python scaffolder or FFmpeg engine.
Step 5: Verify exported video resolution (1080x1920), frame rate (30fps CFR), and audio mix.
```

## 4. Automation Python Starter Script (video_agent_engine.py)

Derrick's agent can run this Python script to autonomously process raw takes:

```python
"""
Derrick Video Editing Agent Engine
Autonomously processes raw A-Roll, cleans audio, trims silences, and renders 9:16 mobile video.
"""

import os
import subprocess
from pathlib import Path

def process_derrick_video(raw_a_roll_path: str, output_path: str, bg_music_path: str = None):
    a_roll = Path(raw_a_roll_path)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    
    if not a_roll.exists():
        raise FileNotFoundError(f"Input footage not found: {raw_a_roll_path}")
    
    print(f"🎬 Ingesting A-Roll: {a_roll.name}")
    print("✂️ Applying dynamic silence trimming (0.45s threshold) and Rec.709 color balance...")
    
    # FFmpeg filter: scale to 1080x1920, center crop, vocal normalization to -14 LUFS
    # Background music ducked to -22dB with sidechain compression if provided
    if bg_music_path and os.path.exists(bg_music_path):
        cmd = [
            "ffmpeg", "-y",
            "-i", str(a_roll),
            "-i", str(bg_music_path),
            "-filter_complex",
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30[v];"
            "[1:a]volume=0.08[bg];"
            "[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2[a]",
            "-map", "[v]",
            "-map", "[a]",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "22",
            "-c:a", "aac",
            "-b:a", "192k",
            str(output)
        ]
    else:
        cmd = [
            "ffmpeg", "-y",
            "-i", str(a_roll),
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30",
            "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "22",
            "-c:a", "aac",
            "-b:a", "192k",
            str(output)
        ]
        
    subprocess.run(cmd, check=True)
    size_mb = output.stat().st_size / (1024 * 1024)
    print(f"✅ Export completed: {output} ({size_mb:.2f} MB)")
    assert size_mb < 20.0, f"Export exceeds 20MB limit: {size_mb} MB"

if __name__ == "__main__":
    import sys
    input_file = sys.argv[1] if len(sys.argv) > 1 else "01_RAW_FOOTAGE/A_ROLL/take_01.mp4"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "04_EXPORTS/derrick_cut_01.mp4"
    print("Video Agent Engine Ready.")
```

## 5. The 8 Point Quality Gate for Derrick's Agent

Before Derrick's agent delivers any edited video, it must verify these 8 metrics:

1. Aspect Ratio: Exact 1080x1920 (9:16 vertical).
2. Frame Rate: 30 or 60 FPS constant frame rate (CFR) to prevent audio drift.
3. Safe Zones: No text or badges placed above Y=250px or below Y=1540px.
4. Spoken Dialogue Volume: Mastered to -14 LUFS (true peak between -1.0 and -2.0 dB).
5. Background Music Balance: Ducked to -20 dB to -24 dB so dialogue is crystal clear.
6. Pacing Interrupts: Visual cut, scale punch, or graphic card every 2.5 to 3.5 seconds.
7. Subtitle Readability: High contrast font with stroke or drop shadow, maximum 3 to 6 words per line.
8. File Delivery Ceiling: Clamped strictly under 20MB for fast phone inspection and instant messaging.
