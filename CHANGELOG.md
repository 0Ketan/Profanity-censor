# Changelog

All notable changes to the Profanity Censor project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-02-15

### 🎉 Added
- Initial release of AI-Powered Profanity Censor
- Audio/video processing with timestamp-based censorship
- GPU acceleration with CUDA (RTX 3050 compatible)
- Multiple Whisper models (tiny, base, small, medium, large)
- Support for 100+ languages
- Custom profanity word lists
- Custom beep sounds
- Batch processing capability
- Detailed JSON logging
- Console progress reporting
- Video: MP4, MKV, AVI, MOV, WMV, FLV, WebM
- Audio: MP3, WAV, FLAC, M4A, AAC, OGG, and more
- Real-time preview with `--list-only` flag
- Adjustable padding around profanity
- Configurable output directories
- Comprehensive documentation

### 📚 Documentation
- Added README.md with badges and professional layout
- Added CONTRIBUTING.md for contributors
- Added INSTALLATION.md with platform-specific instructions
- Added TROUBLESHOOTING.md with common issues and solutions
- Added QUICKSTART-censor.md for quick start guide
- Added examples directory
- Added GitHub Actions CI/CD pipeline

### 🔧 Technical
- Python 3.8+ support
- Uses faster-whisper for GPU acceleration (10-20x speedup)
- Uses pydub for audio manipulation
- FFmpeg integration for video processing
- Clean architecture with modular components
- Error handling and graceful degradation
- Memory-efficient processing

### 🧪 Testing
- Tested on RTX 3050 (6GB)
- Tested on Linux (Fedora)
- Tested with Python 3.14
- Verified with multiple video formats
- Verified with multiple audio formats
- Batch processing tested

### 📊 Performance
- Base model: ~5x realtime on RTX 3050
- Small model: ~2.5x realtime on RTX 3050
- Medium model: ~1.5x realtime on RTX 3050
- Tiny model: ~10x realtime on RTX 3050

### 🚀 Optimization
- GPU-accelerated transcription
- Efficient memory management
- Streaming audio processing
- Parallel video/audio extraction
- Optimized beep overlay

### 🎯 Use Cases Supported
✅ Content creators
✅ Podcasters
✅ Educators
✅ Musicians (radio edits)
✅ Businesses
✅ Live streamers

### 📦 Distribution
- PyPI-ready with pyproject.toml
- GitHub Actions CI/CD
- Docker support (planned)
- conda-forge ready (planned)

## 🗺️ Roadmap

### [1.1.0] - Coming Soon
- Real-time microphone censorship
- Web interface with upload button
- Batch processing GUI
- Confidence scoring and threshold adjustment
- Custom beep patterns
- Multiple voice detection
- Whisper model fine-tuning support

### [2.0.0] - Future
- Live streaming support (RTMP)
- Cloud API service
- Mobile app (Android/iOS)
- Chrome extension
- Adobe Premiere plugin
- Davinci Resolve plugin

---

<p align="center">
  <b>Version 1.0.0 - Production Ready! 🎉</b>
</p>
