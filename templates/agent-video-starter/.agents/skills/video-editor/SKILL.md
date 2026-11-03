# Autonomous Video Editor Agent Skill

## Executive Summary
This skill empowers Derrick's AI agent to autonomously assemble, edit, and export broadcast quality short form vertical videos (9:16 - 1080x1920 @ 30/60fps CFR) using Python, FFmpeg, and deterministic brand presets.

## Core Rules & Invariants
1. Pacing & Pattern Interrupt Rule: Never allow the video frame to remain static for longer than 3.0 seconds. Alternate between A-Roll punch-ins (1.12x scale ease), B-Roll overlays, and graphic callouts.
2. Safe Zone Clearance: Do not place captions, faces, or branding in the top 250px, bottom 380px, or right 140px margins of the 9:16 mobile canvas.
3. Audio Loudness Standards: Dialogue vocals normalized to -14 LUFS (true peak -1.5 dB). Duck background music to -22 dB while speech is active.
4. Silence Snapping: Purge dead air and pauses exceeding 0.45 seconds to maintain high velocity social pacing.
5. Mobile Size Ceiling: Clamp output MP4 under 20MB for immediate mobile streaming and messaging.

## Execution Runbook
• Step 1: Detect newest recording in `01_RAW_FOOTAGE/A_ROLL/`.
• Step 2: Read selected configuration from `config/` (default: `video_preferences.json`).
• Step 3: Run `video_agent_engine.py` to assemble the video with audio normalization and cropping.
• Step 4: Verify that output file size is under 20MB and resolution matches 1080x1920 CFR.
• Step 5: Output a concise completion receipt with the exported file path and duration.
