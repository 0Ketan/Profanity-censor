#!/bin/bash
# Basic Profanity Censor Demo
# Requires: sample.mp3 or sample.mp4 in this directory

echo "🎬 Profanity Censor Demo"
echo "========================="

# Check if sample file exists
if [ -f "sample.mp3" ]; then
    echo "Found sample.mp3, processing..."
    python3 ../profanity_censor.py sample.mp3 --model tiny --list-only
elif [ -f "sample.mp4" ]; then
    echo "Found sample.mp4, processing..."
    python3 ../profanity_censor.py sample.mp4 --model tiny --list-only
else
    echo "⚠️  No sample.mp3 or sample.mp4 found!"
    echo ""
    echo "To run this demo:"
    echo "1. Place an audio/video file in this directory"
    echo "2. Name it 'sample.mp3' or 'sample.mp4'"
    echo "3. Run: ./basic_demo.sh"
    echo ""
    echo "Or test directly:"
    echo "python3 ../profanity_censor.py yourfile.mp3 --list-only"
fi
