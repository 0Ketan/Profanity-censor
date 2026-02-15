<div align="center">

# 🤖 AI-Powered Profanity Censor

**Automatically detect and censor profanity in audio/video using AI transcription**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![GPU](https://img.shields.io/badge/GPU-CUDA-green.svg)](https://developer.nvidia.com/cuda)
[![Whisper AI](https://img.shields.io/badge/Powered%20by-Whisper%20AI-orange.svg)](https://openai.com/research/whisper)
[![License: GPL](https://img.shields.io/badge/License-GPL-yellow.svg)](https://opensource.org/licenses/GPL-3.0)
[![Made with Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red.svg)]()

</div>

<p align="center">
  <img src="assets/demo-preview.png" alt="Demo" width="600"/>
</p>

---

## 📺 Demo

https://github.com/user-attachments/assets/demo-video.mp4

*Watch the AI automatically detect and censor profanity in real-time*

---

## 🚀 Features

### 🤖 AI-Powered Detection
- Uses **OpenAI Whisper** for industry-leading speech recognition
- GPU-accelerated with **CUDA** (10-20x faster than CPU)
- Supports **100+ languages**

### 🎵 Media Support
- ✅ **Audio**: MP3, WAV, FLAC, M4A, AAC, OGG, and more
- ✅ **Video**: MP4, MKV, AVI, MOV, WMV, FLV, WebM

### ⚡ Smart Censoring
- **Precise timestamps** - censors at exact word locations
- **Adjustable padding** - add buffer before/after profanity
- **Visual logs** - see exactly what was censored and when
- **Non-destructive** - original file never modified

### 🔧 Fully Customizable
- Custom profanity word lists
- Custom beep sounds
- Multiple AI models (tiny → large)
- Adjustable sensitivity

---

## 📊 Performance

| Model | Speed (RTX 3050) | Accuracy | Memory |
|-------|-----------------|----------|--------|
| tiny | ~10x realtime | ⭐⭐ | 500MB |
| **base** | **~5x realtime** | ⭐⭐⭐ | 1GB |
| small | ~2.5x realtime | ⭐⭐⭐⭐ | 2GB |
| medium | ~1.5x realtime | ⭐⭐⭐⭐⭐ | 5GB |
| large | ~0.8x realtime | ⭐⭐⭐⭐⭐⭐ | 10GB |

**On RTX 3050**: 10-minute video processes in **2 minutes (base model)**

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- ffmpeg
- NVIDIA GPU with CUDA (optional, for 10-20x speedup)

### Quick Install

```bash
# 1. Clone the repository
git clone https://github.com/KetanSon/profanity-censor.git
cd profanity-censor

# 2. Install Python dependencies
pip install -r requirements-censor.txt

# 3. Verify installation
python3 profanity_censor.py --help
```

### For GPU Users (Recommended)

**Everything is already configured!** Just run:
```bash
pip install faster-whisper
```

That's it! The script auto-detects your GPU and uses CUDA acceleration.

---

## 🎬 Quick Start

### 1. Censor an Audio File

```bash
python3 profanity_censor.py podcast.mp3
```

Creates: `podcast_censored/clean_podcast.mp3`

### 2. Censor a Video File

```bash
python3 profanity_censor.py tutorial.mp4
```

Creates: `tutorial_censored/clean_tutorial.mp4`

### 3. Use a More Accurate Model

```bash
python3 profanity_censor.py video.mp4 --model medium
```

### 4. Batch Process Multiple Files

```bash
for file in *.mp4; do
    python3 profanity_censor.py "$file"
done
```

---

## 🔧 Advanced Usage

### Command Line Options

```bash
python3 profanity_censor.py [OPTIONS] INPUT_FILE

Options:
  -o, --output OUTPUT    Output directory (default: input_censored/)
  -m, --model MODEL      AI model: tiny, base, small, medium, large
  -d, --device DEVICE    cuda (GPU) or cpu
  -p, --padding PADDING  Safety buffer in ms (default: 100)
  -l, --language LANG    Audio language (default: en)
  --list-only           Only detect, don't censor
  --profanity-file FILE Custom profanity list
```

### Examples

```bash
# Censor Spanish audio
python3 profanity_censor.py audio.mp3 --language es

# Increase padding around profanity
python3 profanity_censor.py video.mp4 --padding 200

# Use CPU instead of GPU
python3 profanity_censor.py podcast.mp3 --device cpu

# Test detection without censoring
python3 profanity_censor.py audio.mp3 --list-only
```

---

## 📊 Example Output

### Censorship Log

The script generates a detailed JSON log:

```json
{
  "original_file": "/home/user/podcast.mp3",
  "output_file": "/home/user/podcast_censored/clean_podcast.mp3",
  "profanities_found": 4,
  "profanity_segments": [
    {
      "word": " fuck",
      "start": 12.45,
      "end": 12.68
    },
    {
      "word": " shit",
      "start": 45.21,
      "end": 45.39
    }
  ]
}
```

### Console Output

```bash
🔍 Transcribing audio: podcast.mp3
✓ Audio loaded: 600000ms, 44100Hz
✓ Loaded faster-whisper model on cuda

🚫 Profanity detected: ' fuck' at 12.45s - 12.68s
🚫 Profanity detected: ' shit' at 45.21s - 45.39s

🔧 Censoring 2 profanity segments...
  Censored ' fuck' at 12.45s
  Censored ' shit' at 45.21s

✅ Censored audio saved to: podcast_censored/clean_podcast.mp3
   Duration: 600000ms | Size: 4.5 MB
```

---

## 🎨 Customization

### Custom Profanity List

Edit `profanity_list.txt`:

```bash
# Add one word per line
fuck
shit
damn
# Variants
sh1t
fk
```

### Custom Beep Sound

Add a custom `beep.wav` file to the project root to use it instead of the generated beep.

### Custom Output Location

```bash
python3 profanity_censor.py audio.mp3 -o ./clean-output/
```

---

## 🎯 Use Cases

### Content Creators
✅ Clean up YouTube videos before publishing
✅ Create family-friendly versions of content
✅ Batch process entire video libraries

### Podcasters
✅ Automatically censor live recordings
✅ Generate clean versions for all platforms
✅ Maintain brand safety

### Educators
✅ Clean up educational videos
✅ Make content appropriate for classrooms
✅ Batch process course materials

### Musicians
✅ Create radio edits of songs
✅ Clean up explicit content for streaming
✅ Process entire albums

### Businesses
✅ Clean training videos
✅ Maintain professional standards
✅ Brand safety compliance

---

## 🔍 Troubleshooting

### GPU Not Detected?
```bash
python3 profanity_censor.py audio.mp3 --device cpu
```

### Low Accuracy?
```bash
# Use larger model
python3 profanity_censor.py audio.mp3 --model medium
```

### Running Out of Memory?
```bash
# Use smaller model
python3 profanity_censor.py audio.mp3 --model tiny
```

### False Positives?
Edit `profanity_list.txt` and remove problematic words

Full troubleshooting guide: [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

## 📈 Roadmap

- [x] Audio/video processing
- [x] GPU acceleration
- [x] Batch processing
- [x] Custom word lists
- [ ] Real-time microphone censoring (WIP)
- [ ] Live streaming support
- [ ] Web interface
- [ ] Multiple language support
- [ ] Confidence scoring
- [ ] Custom beep patterns

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📝 License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - Speech recognition
- [faster-whisper](https://github.com/guillaumekln/faster-whisper) - GPU acceleration
- [pydub](https://github.com/jiaaro/pydub) - Audio processing
- FFmpeg team - Video/audio framework

---

## 📧 Contact

- 📱 **LinkedIn**: [Your Name](https://linkedin.com/in/yourname)
- 🐦 **Twitter**: [@yourhandle](https://twitter.com/yourhandle)
- 📧 **Email**: bketan178@gmail.com

---

<p align="center">
  <i>Made with ❤️ for creators who want clean content</i>
</p>

<div align="center">

⭐ **Star this repo if you find it useful!** ⭐

</div>
