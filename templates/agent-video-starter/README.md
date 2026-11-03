# Autonomous Video Editor Agent Starter Kit
**Architected by Penn Enterprises LLC**

An open source, plug and play operational blueprint to equip AI coding agents (Antigravity, Cursor, Claude Code, VS Code) with autonomous video editing capabilities.

## Executive Overview

Content creators spend 10 to 15 hours every week performing repetitive editing tasks: trimming dead air, scaling video into 9:16 mobile formats, adjusting audio levels, and organizing media files. 

This starter kit solves that problem by giving your AI agent the exact skill instructions, directory intake bins, configuration schemas, and Python rendering engines required to assemble polished videos autonomously.

## Directory Structure

```text
agent-video-starter/
├── 01_RAW_FOOTAGE/
│   ├── A_ROLL/          (Drop your primary talking head takes here)
│   └── B_ROLL/          (Drop screen recordings, demo clips, or b-roll here)
├── 02_AUDIO/
│   ├── DIALOGUE/        (Clean audio tracks or lavalier recordings)
│   ├── MUSIC/           (Background music beds and lo-fi tracks)
│   └── SFX/             (Whooshes, transition risers, and impact hits)
├── 03_ASSETS/
│   ├── LOGOS/           (Transparent brand marks and badges)
│   └── OVERLAYS/        (Screenshots, proof artifacts, lower thirds)
├── 04_EXPORTS/          (Final rendered MP4 ready for publishing)
├── config/
│   └── video_preferences.json
├── SKILL.md             (The instruction set for your AI agent)
├── video_agent_engine.py(Autonomous FFmpeg rendering engine)
└── README.md
```

## Quickstart in 3 Steps

### Step 1: Install Requirements
Ensure FFmpeg is installed on your machine:
```bash
# On macOS via Homebrew:
brew install ffmpeg

# On Ubuntu / Debian:
sudo apt update && sudo apt install -y ffmpeg
```

### Step 2: Drop Your Footage
Place your raw video take into `01_RAW_FOOTAGE/A_ROLL/take_01.mp4`.

### Step 3: Run the Autonomous Engine
Execute the engine directly, or ask your AI agent to run it:
```bash
python3 video_agent_engine.py
```
The script auto detects the newest video in `01_RAW_FOOTAGE/A_ROLL/`, crops it to vertical 1080x1920 (9:16), normalizes speech audio to -14 LUFS, and outputs a compliant file to `04_EXPORTS/take_01_edited.mp4` clamped strictly under 20MB.

## Directing Your AI Agent

If you use an agentic IDE like Antigravity, Cursor, or Claude Code, your agent can handle the entire workflow. 

Simply tell your agent:
> "Read SKILL.md and edit my latest take in 01_RAW_FOOTAGE/A_ROLL using our video_preferences.json."

The agent will autonomously:
1. Scan the intake directory for your newest take.
2. Read your brand preferences (colors, fonts, loudness).
3. Execute `video_agent_engine.py` with custom parameters.
4. Verify the output resolution and file size.
5. Report the completed export path directly in your chat.

## The Two Production Pathways

• **Pathway A: Programmatic Headless Rendering (Python and FFmpeg)**
Best for 100 percent hands off bulk processing, split screen walkthroughs, and instant social clips. The agent processes everything headlessly with zero human intervention.

• **Pathway B: CapCut Desktop Draft Integration**
Best for high status speaking videos where you want kinetic caption animations and auto captions. The agent organizes the project bins and rough cuts, allowing you to open CapCut Desktop and apply animated text presets in 1 click.

## Customizing Your Brand (`video_preferences.json`)

You can edit `video_preferences.json` to customize:
• **Creator Name & Title:** Displayed on lower third cards.
• **Brand Colors:** Base text color, active highlight color, and card borders.
• **Silence Snapping Threshold:** Default 0.45 seconds to purge pauses.
• **Audio Loudness Floor:** Default -14 LUFS dialogue and -22 dB background music ducking.
• **Export Size Ceiling:** Default 20.0 MB for instant mobile streaming.

## The 8 Point Video Quality Gate

Before any video is marked complete, the agent verifies:
1. Aspect Ratio: Exact 1080x1920 (9:16 vertical).
2. Frame Rate: 30 or 60 FPS constant frame rate (CFR) to prevent audio drift.
3. Safe Zones: Captions and focal points placed between Y=250px and Y=1540px.
4. Vocal Loudness: Mastered to -14 LUFS (peak between -1.0 and -2.0 dB).
5. Background Music Balance: Ducked to -22 dB while speech is active.
6. Pacing Interrupts: Visual cut, scale punch, or graphic card every 2.5 to 3.5 seconds.
7. Subtitle Readability: High contrast font with stroke or shadow, 3 to 6 words per line.
8. Mobile Ceiling: File size strictly under 20MB for fast phone streaming.

---
*Created by Keymon Penn | Solutions Architect & AI Operating Partner at Penn Enterprises LLC.*
