#!/bin/bash
# Demo Script for Profanity Censor
# This script demonstrates the key features

echo "🎬 Profanity Censor - Feature Demo"
echo "================================"
echo ""

# Check if demo files exist
if [ ! -f "demo_audio.mp3" ]; then
    echo "⚠️  Demo files not found. Creating synthetic demo..."
    echo ""
    echo "To see full demo:"
    echo "1. Place demo_audio.mp3 in this folder"
    echo "2. Run: ./run_demo.sh"
    echo ""
    echo "Or test with your own file:"
    echo "cd .. && python3 profanity_censor.py examples/your_audio.mp3"
    exit 1
fi

echo "Running 5 demonstrations:"
echo ""

# Demo 1: Basic censorship
echo "1️⃣  Basic Censorship"
echo "   Command: python3 profanity_censor.py demo_audio.mp3"
python3 profanity_censor.py demo_audio.mp3 --list-only | head -10
echo ""

# Demo 2: Different models
echo "2️⃣  Model Comparison (list-only mode)"
echo "   Testing with different Whisper models..."
for model in tiny base small; do
    echo "   Model: $model"
    time python3 profanity_censor.py demo_audio.mp3 --model $model --list-only > /dev/null 2>&1
    echo ""
done

# Demo 3: Different padding
echo "3️⃣  Padding Comparison"
echo "   --padding 50 (minimal)"
python3 profanity_censor.py demo_audio.mp3 --padding 50 --list-only 2>&1 | grep -E "(Censored|profanity)" | head -3
echo "   --padding 200 (generous)"
python3 profanity_censor.py demo_audio.mp3 --padding 200 --list-only 2>&1 | grep -E "(Censored|profanity)" | head -3
echo ""

# Demo 4: Video processing
echo "4️⃣  Video Processing"
echo "   Command: python3 profanity_censor.py demo_video.mp4"
if [ -f "demo_video.mp4" ]; then
    python3 profanity_censor.py demo_video.mp4 --list-only | head -5
else
    echo "   ⚠️  demo_video.mp4 not found"
    echo "   Skipping video demo"
fi
echo ""

# Demo 5: Batch processing
echo "5️⃣  Batch Processing"
echo "   Create multiple outputs:"
echo "   for file in *.mp3; do"
echo "     python3 profanity_censor.py \"\$file\" -o ./clean/"
echo "   done"
echo ""

echo "✅ Demo Complete!"
echo ""
echo "📊 Results available in:"
echo "   - demo_audio_censored/clean_demo_audio.mp3"
echo "   - demo_audio_censored/censorship_log.json"
echo ""
echo "📖 Full documentation: README.md"
