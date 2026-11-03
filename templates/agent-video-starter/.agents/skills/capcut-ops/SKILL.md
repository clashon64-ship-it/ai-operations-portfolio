# CapCut Desktop Autonomous Project Scaffolding Skill

## Executive Summary
This skill enables Derrick's AI agent to autonomously synthesize and scaffold multi track CapCut Desktop projects on macOS directly inside `~/Movies/CapCut/User Data/Projects/com.lveditor.draft/`. 

By generating native JSON draft definitions (`draft_info.json`, `draft_meta_info.json`, and `root_meta_info.json`), the agent prepares a fully binned, cut, and audio ducked timeline so Derrick can open CapCut and apply kinetic auto-captions or stickers with zero manual scrubbing.

## Multi-Track Timeline Architecture
```text
Track 4 [AUDIO]      ──► Background Music (Ducked to -22 dB during speech)
Track 3 [TEXT]       ──► Kinetic Captions & Highlight Overlays (Flag: 1, Centered Y: -0.42)
Track 2 [OVERLAY]    ──► Graphic Lower Thirds, Brand Badges & Callouts (Flag: 2)
Track 1 [B-ROLL]     ──► Supplementary Footage & B-Roll Cutaways (Flag: 2, Pattern Interrupts)
Track 0 [A-ROLL]     ──► Main Primary Footage / Talking Head (Flag: 0, 1080x1920)
```

## Track Flag Semantics
• `flag: 0`: Base timeline track (snaps to clips, primary continuous audio and video source).
• `flag: 1`: Text and subtitle overlay track.
• `flag: 2`: Video overlay / Picture in Picture (PIP) track. Allows free placement and custom scaling.

## Execution Runbook
• Step 1: Ingest primary take from `01_RAW_FOOTAGE/A_ROLL/` and B-Roll from `01_RAW_FOOTAGE/B_ROLL/`.
• Step 2: Run `python3 scaffold_capcut_project.py --project-name "Derrick_Take_01"`.
• Step 3: Open CapCut Desktop on Mac. Project appears automatically on the home screen.
• Step 4: Click Text ➔ Auto Captions ➔ Generate to create kinetic subtitle tracks.
• Step 5: Export high resolution 1080x1920 30fps MP4.
