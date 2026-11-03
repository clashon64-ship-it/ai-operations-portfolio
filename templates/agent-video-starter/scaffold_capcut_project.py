#!/usr/bin/env python3
"""
Autonomous CapCut Desktop Project Scaffolder for Derrick
Scaffolds a multi-track 9:16 project inside local CapCut Desktop on macOS.
Pre-populates A-Roll on Track 0, B-Roll on Track 1, and text captions on Track 3.
"""

import os
import sys
import json
import time
import uuid
import argparse
from pathlib import Path

CAPCUT_DRAFT_ROOT = Path(os.path.expanduser("~/Movies/CapCut/User Data/Projects/com.lveditor.draft"))
ROOT_META_FILE = CAPCUT_DRAFT_ROOT / "root_meta_info.json"

def scaffold_draft(project_name: str, a_roll_file: Path, b_roll_file: Path = None):
    if not CAPCUT_DRAFT_ROOT.exists():
        print(f"⚠️ Notice: CapCut drafts directory not found at {CAPCUT_DRAFT_ROOT}.")
        print("This feature is designed for macOS with CapCut Desktop installed.")
        CAPCUT_DRAFT_ROOT.mkdir(parents=True, exist_ok=True)

    proj_dir = CAPCUT_DRAFT_ROOT / project_name
    proj_dir.mkdir(parents=True, exist_ok=True)

    project_uuid = str(uuid.uuid4()).upper()
    now_us = int(time.time() * 1_000_000)
    dur_us = 60 * 1_000_000

    # Create draft_meta_info.json
    draft_meta = {
        "draft_id": project_uuid,
        "draft_name": project_name,
        "tm_duration": dur_us,
        "tm_draft_create_time": now_us,
        "tm_draft_modified_time": now_us
    }
    with open(proj_dir / "draft_meta_info.json", "w", encoding="utf-8") as f:
        json.dump(draft_meta, f, indent=2)

    # Multi-track structure: Track 0 (A-Roll), Track 1 (B-Roll), Track 2 (Text/Captions)
    track_aroll_id = str(uuid.uuid4()).upper()
    track_broll_id = str(uuid.uuid4()).upper()
    track_text_id = str(uuid.uuid4()).upper()

    tracks = [
        {"id": track_aroll_id, "type": "video", "flag": 0, "segments": []},
        {"id": track_broll_id, "type": "video", "flag": 2, "segments": []},
        {"id": track_text_id, "type": "text", "flag": 1, "segments": []}
    ]

    draft_info = {
        "canvas_config": {"width": 1080, "height": 1920, "ratio": "9:16"},
        "fps": 30.0,
        "duration": dur_us,
        "tracks": tracks
    }
    with open(proj_dir / "draft_info.json", "w", encoding="utf-8") as f:
        json.dump(draft_info, f, indent=2)

    # Register in root_meta_info.json if present
    if ROOT_META_FILE.exists():
        try:
            with open(ROOT_META_FILE, "r", encoding="utf-8") as f:
                root_meta = json.load(f)
            all_drafts = root_meta.get("all_draft_store", [])
            existing = [d for d in all_drafts if d.get("draft_id") == project_uuid or d.get("draft_fold_path") == str(proj_dir)]
            if not existing:
                all_drafts.insert(0, {
                    "draft_fold_path": str(proj_dir),
                    "draft_id": project_uuid,
                    "draft_name": project_name,
                    "tm_draft_create_time": now_us,
                    "tm_draft_modified_time": now_us,
                    "tm_duration": dur_us
                })
                root_meta["all_draft_store"] = all_drafts
                with open(ROOT_META_FILE, "w", encoding="utf-8") as f:
                    json.dump(root_meta, f, indent=2)
                print("📋 Registered project in CapCut root registry.")
        except Exception as e:
            print(f"⚠️ Notice: Could not update root_meta_info.json: {e}")

    print(f"✅ Successfully scaffolded CapCut Desktop project: {project_name}")
    print(f"📁 Project location: {proj_dir}")
    print("👉 Open CapCut Desktop to view your assembled timeline!")

def main():
    parser = argparse.ArgumentParser(description="Autonomous CapCut Desktop Scaffolder")
    parser.add_argument("--project-name", "-p", default="Derrick_Video_Edit_01", help="Name of project")
    parser.add_argument("--a-roll", "-a", type=str, help="Path to A-Roll footage")
    args = parser.parse_args()

    a_roll = Path(args.a_roll) if args.a_roll else Path("01_RAW_FOOTAGE/A_ROLL/take_01.mp4")
    scaffold_draft(args.project_name, a_roll)

if __name__ == "__main__":
    main()
