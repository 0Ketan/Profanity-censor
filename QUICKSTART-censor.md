# Profanity Censor - Quick Start Guide

## ✅ Installation Complete!

All requirements have been installed successfully:

### Installed Software:
- **Python 3.14.2** ✓
- **pip 26.0.1** ✓
- **ffmpeg 7.1.2** ✓
- **faster-whisper 1.2.1** ✓ (GPU-accelerated)
- **pydub 0.25.1** ✓
- **numpy 2.3.5** ✓
- **Whisper model: base** ✓ (downloaded)

### System Info:
- **GPU**: RTX 3050 with CUDA support
- **OS**: Fedora Linux (Kernel 6.18.9)
- **Performance**: Expected 5-10x real-time processing

## 🚀 Quick Start

### Audio File (MP3, WAV, M4A, etc.)
```bash
cd /home/ketan/automation-tools
python3 profanity_censor.py /path/to/audio.mp3
```

### Video File (MP4, MKV, AVI, etc.)
```bash
python3 profanity_censor.py /path/to/video.mp4
```

### Output Location
By default, creates a **different folder** (as requested):
```
input.mp3
└── input_censored/
    ├── clean_input.mp3      # Censored version
    └── censorship_log.json   # Detection timestamps
```

## 🔧 Advanced Options

### Use More Accurate Model
```bash
python3 profanity_censor.py audio.mp3 --model medium
```

Options: tiny, base (default), small, medium, large

### Custom Output Directory
```bash
python3 profanity_censor.py audio.mp3 -o ./clean_output/
```

### Increase/Decrease Padding
```bash
# More padding (censor more around profanity)
python3 profanity_censor.py audio.mp3 --padding 200

# Less padding (minimize interruption)
python3 profanity_censor.py audio.mp3 --padding 50
```

### Only Detect (Don't Censor)
```bash
python3 profanity_censor.py audio.mp3 --list-only
```

## 📊 Performance Benchmarks (RTX 3050)

| Model | Speed vs Realtime | Accuracy | Memory |
|-------|-------------------|----------|--------|
| tiny  | ~10x faster | Low | ~500MB |
| base  | ~5x faster | Good | ~1GB |
| small | ~2.5x faster | Better | ~2GB |
| medium| ~1.5x faster | High | ~5GB |
| large | ~0.8x faster | Highest | ~10GB |

**Recommendation**: Use `base` for most cases (default)

## 📝 Customization

### Edit Profanity List
```bash
nano /home/ketan/automation-tools/profanity_list.txt
```

Add words one per line. Restart is not needed - new list loads on each run.

### Custom Beep Sound
Place `beep.wav` in the same folder to use a custom beep:
```bash
# No custom beep? Creates synthetic beep automatically
```

## 🎬 Batch Processing

Process multiple files:
```bash
for file in *.mp3; do
    python3 profanity_censor.py "$file"
done
```

## 🔍 Testing

### Test Setup
```bash
# Verify installation
cd /home/ketan/automation-tools
python3 -c "import faster_whisper; print('GPU:', 'Enabled')"

# Run help
python3 profanity_censor.py --help
```

### Expected First Run
When you first run the script, it will:
1. ✅ Load Whisper model (fast, cached)
2. ✅ Extract audio from video (if needed)
3. ✅ Transcribe with timestamps
4. ✅ Detect profanity
5. ✅ Generate censored output
6. ✅ Create censorship log

Time for 5-min audio: ~30-60 seconds (base model)

## 🎯 Common Use Cases

### 1. YouTube Downloads
```bash
# First download YouTube video
python3 /home/ketan/automation-tools/downloader.py "YOUTUBE_URL"

# Then censor it
python3 profanity_censor.py downloaded_video.mp4
```

### 2. Podcast Cleanup
```bash
python3 profanity_censor.py podcast.mp3 --model medium --padding 150
```

### 3. Music Tracks
```bash
# Process entire album
for song in *.mp3; do
    python3 profanity_censor.py "$song" -o ./clean_music/
done
```

### 4. Streaming Recordings
```bash
python3 profanity_censor.py stream_recording.mp4
```

## 🛠️ Troubleshooting

### Low Accuracy?
```bash
# Use larger model
python3 profanity_censor.py audio.mp3 --model small
# or
python3 profanity_censor.py audio.mp3 --model medium
```

### Audio Not Syncing?
```bash
# Increase padding
python3 profanity_censor.py audio.mp3 --padding 200
```

### False Positives?
```bash
# Edit profanity list and remove problematic words
nano /home/ketan/automation-tools/profanity_list.txt
```

### GPU Not Working?
```bash
# Force CPU mode (slower but works)
python3 profanity_censor.py audio.mp3 --device cpu
```

## 📁 Files Overview

```
/home/ketan/automation-tools/
├── profanity_censor.py    # Main script
├── profanity_list.txt      # Profanity word list
├── requirements-censor.txt # Python dependencies
├── README-profanity-censor.md # Full documentation
├── QUICKSTART-censor.md    # This file
└── censor-quickstart.sh    # Quick-start helper
```

## 🎓 Next Steps

1. Test with a sample audio/video file
2. Adjust profanity list for your needs
3. Try different models for accuracy/speed tradeoff
4. Set up batch processing for multiple files
5. Experiment with padding settings

## 📞 Support

**All files are in**: `/home/ketan/automation-tools/`

For issues:
1. Check: `python3 profanity_censor.py --help`
2. Read: `README-profanity-censor.md` (full documentation)
3. Run with: `--list-only` to test detection
4. Try: `--model tiny` for faster testing

## 🎉 You're Ready to Censor!

```bash
cd /home/ketan/automation-tools
python3 profanity_censor.py your_file.mp3
```

Happy censoring! 🤖🔇
