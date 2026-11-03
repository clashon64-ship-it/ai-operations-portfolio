# Brother Derrick & Keymon Penn | Shared Brain Exchange Hub

## Executive Purpose

This repository hub acts as the asynchronous, autonomous Shared Brain between Keymon Penn (Penn Enterprises LLC) and Brother Derrick (Derrick McCullough). 

It allows Keymon to dispatch tasks, video briefs, skills, and blueprints directly into Derrick's orbit, and empowers Derrick's AI agent to pull them in, execute them, and return finished deliverables autonomously.

## Hub Architecture

```text
shared-brains/derrick/
├── INBOX_FROM_KEYMON/     (Where Keymon deposits new blueprints, tasks, and briefs)
├── OUTBOX_TO_KEYMON/      (Where Derrick's agent deposits rendered videos & receipts)
├── SHARED_MEMORY/         (Persistent shared rules, brand preferences, and templates)
├── DISPATCH_MANIFEST.json (The master catalog tracking all task statuses and IDs)
├── sync_derrick_shared_brain.py (Derrick's agent sync and pull engine)
└── README.md
```

## How Keymon Dispatches to Derrick

Keymon (or his AI partner JP) runs:
```bash
python3 engineering/scripts/dispatch_to_derrick.py \
  --file /path/to/asset.md \
  --title "Client Automation Video SOW" \
  --category "VIDEO_PRODUCTION" \
  --priority "HIGH" \
  --notes "Assemble 9:16 vertical walkthrough using our master preferences"
```
The asset is copied to `INBOX_FROM_KEYMON/`, cataloged in `DISPATCH_MANIFEST.json`, and pushed to GitHub automatically.

## How Derrick's Agent Pulls & Executes

Whenever Derrick tells his agent:
> *"Check what Keymon sent me"* or *"Pull from our shared brain"*

His agent executes:
```bash
python3 sync_derrick_shared_brain.py --pull
```
His agent immediately sees all newly staged tasks, reads the instructions, and begins execution.

## How Derrick's Agent Returns Deliverables

When Derrick's agent finishes a video or deliverable, it runs:
```bash
python3 sync_derrick_shared_brain.py \
  --submit /path/to/rendered_video.mp4 \
  --task-id TASK_DERRICK_001 \
  --notes "Rendered 9:16 vertical, dialogue at -14 LUFS, size 14.2MB"
```
The deliverable is pushed to `OUTBOX_TO_KEYMON/` on GitHub, where Keymon's system receives an instant receipt.
