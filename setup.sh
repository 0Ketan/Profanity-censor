#!/bin/bash
# Quick Setup Script for Profanity Censor
# This script helps you get started quickly

echo "🎬 Profanity Censor - Quick Setup"
echo "================================"
echo ""

# Check Python
echo "📋 Checking requirements..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✅ Python $PYTHON_VERSION found"

# Check ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ ffmpeg not found"
    echo "   Install with: sudo apt install ffmpeg  # Linux"
    echo "   Or: brew install ffmpeg                # macOS"
    exit 1
fi
echo "✅ ffmpeg found"

# Check GPU
python3 -c "from faster_whisper import WhisperModel; model = WhisperModel('tiny', device='cuda'); print('✅ GPU available')" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ GPU detected (CUDA) - Will use GPU acceleration"
else
    echo "ℹ️  GPU not detected - Will use CPU (slower but works)"
fi

# Install dependencies
echo ""
echo "📦 Installing Python packages..."
pip3 install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Download sample file (optional)
echo ""
read -p "Download sample audio for testing? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "📥 Downloading sample..."
    if [ ! -f "examples/sample.mp3" ]; then
        mkdir -p examples
        curl -L -o examples/sample.mp3 https://www.soundjay.com/misc/sounds-765.wav 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "✅ Sample downloaded to examples/sample.mp3"
        else
            echo "❌ Failed to download sample"
        fi
    else
        echo "⚠️  Sample already exists"
    fi
fi

# Run test
echo ""
echo "🧪 Testing installation..."
python3 profanity_censor.py --help > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Installation successful!"
    echo ""
    echo "🚀 Quick start:"
    echo "   python3 profanity_censor.py examples/sample.mp3"
    echo ""
    echo "📖 Read more:"
    echo "   cat README.md          # Project overview"
    echo "   cat QUICKSTART-censor.md # Quick guide"
    echo "   cat docs/INSTALLATION.md # Detailed setup"
    echo ""
else
    echo "❌ Installation failed"
    exit 1
fi

echo "🎉 You're ready to censor!"
echo ""
echo "Pro tip: To use custom video/audio:"
echo "   python3 profanity_censor.py /path/to/your_audio.mp4"
echo ""
echo "Happy censoring! 🤖"
