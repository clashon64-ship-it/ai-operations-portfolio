# Autonomous Video Editor Agent Skill

## Executive Summary
This skill empowers an AI agent to act as an autonomous video editor for short form mobile content (9:16 vertical, 1080x1920). 
The agent reads raw footage, trims pauses, enforces brand typography, layers B-Roll, balances audio loudness, and delivers production ready video files.

## Core Rules & Invariants
1. Pacing & Pattern Interrupt Rule: Never leave the visual frame unchanged for longer than 3.0 seconds. Alternate between A-Roll punch-ins (1.12x scale ease), B-Roll overlays, and graphic callouts.
2. Safe Zone Clearance: Do not place captions, faces, or branding in the top 250px, bottom 380px, or right 140px margins of the 9:16 canvas.
3. Audio Loudness Standards: Dialogue vocals normalized to -14 LUFS (true peak -1.5 dB). Duck background music to -22 dB while speech is active.
4. Silence Snapping: Purge dead air and pauses exceeding 0.45 seconds to maintain high velocity social pacing.
5. Mobile Size Ceiling: Clamp output MP4 under 20MB for immediate mobile streaming and messaging.

## Execution Runbook
• Step 1: Detect new footage in `01_RAW_FOOTAGE/A_ROLL/`.
• Step 2: Read `video_preferences.json` to load brand colors, fonts, and timing parameters.
• Step 3: Run `video_agent_engine.py` to assemble the video with audio normalization and cropping.
• Step 4: Verify that output file size is under 20MB and resolution matches 1080x1920 CFR.
• Step 5: Output a concise completion receipt with the exported file path and duration.
