#!/bin/bash
# ==============================================================================
# Penn Enterprises LLC : 1-Click AI Video Studio for Friends & Family
# Double-click this file from your Mac Finder or Desktop to edit videos automatically!
# ==============================================================================

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=================================================================="
echo "          PENN ENTERPRISES | 1-CLICK AI VIDEO STUDIO              "
echo "=================================================================="
echo "Welcome! This tool automatically edits your video takes in 1 click."
echo "It trims dead air, crops to 9:16 vertical, and balances your audio."
echo "=================================================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is needed on this Mac. Please install Python to continue."
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if FFmpeg is available
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️ FFmpeg not found. Attempting to install via Homebrew..."
    if command -v brew &> /dev/null; then
        brew install ffmpeg
    else
        echo "❌ Please install FFmpeg (brew install ffmpeg) to continue."
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

echo "🎬 Looking for newest take in 01_RAW_FOOTAGE/A_ROLL/..."
python3 video_agent_engine.py

EXIT_CODE=$?
echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "=================================================================="
    echo "✨ SUCCESS! Your finished video is ready in: 04_EXPORTS/"
    echo "=================================================================="
    open "04_EXPORTS"
else
    echo "⚠️ Could not find a video take in 01_RAW_FOOTAGE/A_ROLL/."
    echo "Drop your phone video into 01_RAW_FOOTAGE/A_ROLL/ and run this again!"
fi

echo ""
read -p "Press Enter to close this window..."
