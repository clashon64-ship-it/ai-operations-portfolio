#!/usr/bin/env python3
"""
Brother Derrick Shared Brain Synchronization Engine
Enables Derrick's AI agent to pull new tasks and blueprints from Keymon,
and submit completed deliverables back to the shared repository.
"""

import os
import sys
import json
import shutil
import argparse
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INBOX_DIR = BASE_DIR / "INBOX_FROM_KEYMON"
OUTBOX_DIR = BASE_DIR / "OUTBOX_TO_KEYMON"
MANIFEST_FILE = BASE_DIR / "DISPATCH_MANIFEST.json"

def pull_shared_brain():
    print("🔄 Pulling latest dispatches from Keymon via Git...")
    subprocess.run(["git", "pull"], cwd=str(BASE_DIR.parents[1]), check=True)
    
    if not MANIFEST_FILE.exists():
        print("❌ No manifest file found.")
        return

    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    items = manifest.get("dispatched_items", [])
    print(f"\n📦 Shared Brain Dispatches from Keymon (Total: {len(items)}):")
    print("=" * 60)
    for item in items:
        status_badge = "🟢" if item.get("status") == "AVAILABLE_FOR_PULL" else "⚪"
        print(f"{status_badge} [{item.get('item_id')}] {item.get('title')}")
        print(f"   Priority: {item.get('priority')} | Category: {item.get('category')}")
        print(f"   File: INBOX_FROM_KEYMON/{item.get('target_file')}")
        print(f"   Instructions: {item.get('notes')}")
        print("-" * 60)

def submit_deliverable(file_path: Path, task_id: str, notes: str):
    if not file_path.exists():
        raise FileNotFoundError(f"Deliverable file not found: {file_path}")

    OUTBOX_DIR.mkdir(parents=True, exist_ok=True)
    dest_path = OUTBOX_DIR / file_path.name
    shutil.copy2(file_path, dest_path)
    print(f"✅ Staged deliverable in OUTBOX_TO_KEYMON/{file_path.name}")

    # Update manifest status if task_id matches
    if MANIFEST_FILE.exists():
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        for item in manifest.get("dispatched_items", []):
            if item.get("item_id") == task_id:
                item["status"] = "COMPLETED_BY_DERRICK"
                item["deliverable_file"] = file_path.name
                item["completed_notes"] = notes
        with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

    # Git push return
    portfolio_dir = BASE_DIR.parents[1]
    subprocess.run(["git", "-C", str(portfolio_dir), "add", "shared-brains/derrick"], check=True)
    commit_msg = f"feat(shared-brain): derrick completed {task_id} - {file_path.name}"
    subprocess.run(["git", "-C", str(portfolio_dir), "commit", "-m", commit_msg], check=True)
    subprocess.run(["git", "-C", str(portfolio_dir), "push"], check=True)
    print(f"🚀 Deliverable pushed to GitHub! Keymon's system has received your submission.")

def main():
    parser = argparse.ArgumentParser(description="Brother Derrick Shared Brain Sync")
    parser.add_argument("--pull", action="store_true", help="Pull newest tasks and blueprints from Keymon")
    parser.add_argument("--submit", type=str, help="Path to deliverable file to submit back to Keymon")
    parser.add_argument("--task-id", type=str, default="", help="Task ID corresponding to the deliverable")
    parser.add_argument("--notes", type=str, default="", help="Notes on completion")
    args = parser.parse_args()

    if args.pull:
        pull_shared_brain()
    elif args.submit:
        submit_deliverable(Path(args.submit), args.task_id, args.notes)
    else:
        pull_shared_brain()

if __name__ == "__main__":
    main()
