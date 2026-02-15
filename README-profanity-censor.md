# Profanity Censor

Automatically detect and censor profanity in audio and video files using AI transcription.

## Features

- 🤖 **AI-Powered**: Uses Whisper AI to accurately detect spoken profanity with timestamps
- 🎵 **Audio Support**: Works with MP3, WAV, FLAC, M4A, AAC, OGG, and more
- 🎬 **Video Support**: Extracts audio, censors it, and merges back with video
- ⚡ **GPU Acceleration**: Optional CUDA support for 10-20x faster processing
- 🔊 **Smart Beeping**: Automatically overlays beep sounds at exact profanity timestamps
- 📄 **Log Generation**: Creates censorship logs with all detected profanities and timestamps
- 🎯 **Customizable**: Configure word lists, padding, and sensitivity

## Installation

### Prerequisites

- Python 3.8+
- ffmpeg (install with your package manager)
- NVIDIA GPU with CUDA (optional, for GPU acceleration)

### Install Dependencies

```bash
cd /home/ketan/automation-tools

# Install requirements
pip install -r requirements-censor.txt
```

### For GPU Support (Recommended)

If you have an NVIDIA GPU (RTX 3050 or better):

```bash
# faster-whisper includes cuda support automatically
pip install faster-whisper
```

## Quick Start

### Basic Usage

Censor an audio file:
```bash
python3 /home/ketan/automation-tools/profanity_censor.py path/to/audio.mp3
```

Censor a video file:
```bash
python3 /home/ketan/automation-tools/profanity_censor.py path/to/video.mp4
```

### The Output

By default, the script creates:
- A new folder: `inputfilename_censored/`
- Clean audio/video: `clean_inputfilename.ext`
- A log file: `censorship_log.json` with all detected profanities and timestamps

Example:
```
myaudio.mp3
└── myaudio_censored/
    ├── clean_myaudio.mp3
    └── censorship_log.json
```

## Advanced Usage

### Specify Output Directory

```bash
python3 /home/ketan/automation-tools/profanity_censor.py audio.mp3 -o ./clean_output/
```

### Use Different Whisper Models

Available models (larger = more accurate but slower):
- `tiny` - Fastest, least accurate
- `base` - Fast, good accuracy (default)
- `small` -Balanced speed/accuracy
- `medium` - Slower, very accurate
- `large` - Slowest, most accurate

```bash
# Use medium model for better accuracy
python3 /home/ketan/automation-tools/profanity_censor.py audio.mp3 --model medium

# Use tiny model for testing (fastest)
python3 /home/ketan/automation-tools/profanity_censor.py audio.mp3 --model tiny
```

### CPU vs GPU

Force CPU mode (slower but works without CUDA):
```bash
python3 /home/ketan/automation-tools/profanity_censor.py audio.mp3 --device cpu
```

### Adjust Padding (Safety Buffer)

Add more milliseconds around detected profanity (default: 100ms):
```bash
# Increase to 200ms for extra safety
python3 /home/ketan/automation-tools/profanity_censor.py audio.mp3 --padding 200

# Reduce to 50ms for minimal interruption
python3 /home/ketan/automation-tools/profanity_censor.py audio.mp3 --padding 50
```

### Only Detect (Don't Censor)

Just list detected profanities without censoring:
```bash
python3 /home/ketan/automation-tools/profanity_censor.py audio.mp3 --list-only
```

### Specify Language

For non-English content:
```bash
python3 /home/ketan/automation-tools/profanity_censor.py audio.mp3 --language es
```

## Customizing Profanity List

Edit `/home/ketan/automation-tools/profanity_list.txt`:

```
# Add one word per line
fuck
shit

# Comments start with #
# Common misspellings
fk
sh1t

# Add your specific words
custombadword
```

The script reloads the list on each run.

## Customizing Beep Sound

Replace `/home/ketan/automation-tools/beep.wav` to use a custom beep sound.

If no `beep.wav` exists, the script automatically generates a synthetic beep.

## Performance

### GPU (Recommended for RTX 3050)
- **tiny model**: ~0.1x real-time (10x faster than realtime)
- **base model**: ~0.2x real-time (5x faster than realtime)
- **small model**: ~0.4x real-time (2.5x faster than realtime)

### CPU Only
- **tiny model**: ~2x real-time
- **base model**: ~4x real-time
- **small model**: ~8x real-time

## Troubleshooting

### ffmpeg: command not found

Install ffmpeg:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Fedora/CentOS:**
```bash
sudo dnf install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

### CUDA/GPU Issues

If faster-whisper fails to load with CUDA:

```bash
# Use CPU instead
python3 /home/ketan/automation-tools/profanity_censor.py audio.mp3 --device cpu

# Or install regular whisper
pip install openai-whisper
```

### Out of Memory (OOM)

Use a smaller model:
```bash
python3 /home/ketan/automation-tools/profanity_censor.py audio.mp3 --model tiny
```

### No profanity detected

1. Check your audio quality (clear speech works best)
2. Verify profanity list contains the words used
3. Try a larger model: `--model small` or `--model medium`
4. Check language: `--language en`
5. Use `--list-only` to see what was detected

### Incorrect censoring

- Reduce padding: `--padding 50`
- Check the `censorship_log.json` for exact timestamps
- Adjust profanity list (remove false positives)

## Examples

### Batch Processing

Process multiple files:
```bash
for file in *.mp3; do
    python3 /home/ketan/automation-tools/profanity_censor.py "$file"
done
```

### Create Clean Music Playlist

```bash
mkdir clean_music
python3 /home/ketan/automation-tools/profanity_censor.py song1.mp3 -o clean_music/
python3 /home/ketan/automation-tools/profanity_censor.py song2.mp3 -o clean_music/
```

### Podcast Cleanup

```bash
python3 /home/ketan/automation-tools/profanity_censor.py podcast.mp3 --model medium --padding 150
```

## Log Format

The `censorship_log.json` file contains:

```json
{
  "original_file": "/path/to/file.mp3",
  "output_file": "/path/to/clean_file.mp3",
  "profanities_found": 3,
  "profanity_segments": [
    {
      "word": "shit",
      "start": 12.45,
      "end": 12.68
    }
  ]
}
```

## License

Free to use and modify. Built with:
- Whisper (OpenAI)
- faster-whisper (Guillaume B.
- pydub (Jiaaro)

## Support

For issues or questions:
1. Check Troubleshooting section above
2. Run with `--list-only` to verify detection
3. Test with `--model tiny` for speed
4. Check `censorship_log.json` for details

## Next Steps

Future enhancements:
- Real-time microphone censoring
- Live stream processing
- Web interface
- Video frame timestamp matching
- Custom beep patterns
- Multiple voice detection
- Confidence scoring
