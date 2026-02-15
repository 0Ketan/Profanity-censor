#!/bin/bash
# Quick-start script for Profanity Censor
# Usage: ./censor-quickstart.sh <audio_file>

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CENSOR_SCRIPT="$SCRIPT_DIR/profanity_censor.py"

if [ $# -eq 0 ]; then
    echo "Profanity Censor - Quick Start"
    echo ""
    echo "Usage: $0 <audio_or_video_file>"
    echo ""
    echo "Examples:"
    echo "  $0 podcast.mp3"
    echo "  $0 video.mp4"
    echo "  $0 music.wav"
    echo ""
    echo "Output:"
    echo "  Creates a folder: <filename>_censored/"
    echo "  With clean_audio.<ext> and censorship_log.json"
    echo ""
    echo "For more options, run directly:"
    echo "  python3 $CENSOR_SCRIPT --help"
    exit 1
fi

FILE="$1"

if [ ! -f "$FILE" ]; then
    echo "Error: File not found: $FILE"
    exit 1
fi

echo "🚀 Starting Profanity Censor..."
echo "   File: $FILE"
echo "   Model: base"
echo "   Device: cuda (GPU) or cpu"
echo "=========================="

python3 "$CENSOR_SCRIPT" "$FILE"

echo ""
echo "✅ Done! Check the output folder."
