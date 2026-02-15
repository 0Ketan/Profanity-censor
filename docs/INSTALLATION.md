# Installation Guide

## Installing Profanity Censor

## 📋 Prerequisites

- **Python**: 3.8 or higher
- **ffmpeg**: Latest version
- **GPU** (Optional): NVIDIA GPU with CUDA support for 10-20x speedup

---

## 🐧 Linux Installation

### Step 1: Install ffmpeg

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Fedora/RHEL:**
```bash
sudo dnf install ffmpeg
```

**Arch Linux:**
```bash
sudo pacman -S ffmpeg
```

Verify ffmpeg:
```bash
ffmpeg -version
```

### Step 2: Install Python Dependencies

```bash
# Clone the repository
git clone https://github.com/KetanSon/profanity-censor.git
cd profanity-censor

# Install Python packages
pip install -r requirements.txt
```

### Step 3: Verify GPU Setup (Optional)

If you have an NVIDIA GPU:

```bash
# Check if CUDA is available
python3 -c "import torch; print(torch.cuda.is_available())"

# Expected output: True
```

If CUDA is not available, the script will automatically fall back to CPU.

---

## 🍎 macOS Installation

### Step 1: Install ffmpeg

```bash
# Using Homebrew
brew install ffmpeg

# Or using MacPorts
sudo port install ffmpeg
```

### Step 2: Install Python Dependencies

```bash
git clone https://github.com/KetanSon/profanity-censor.git
cd profanity-censor
pip3 install -r requirements.txt
```

Note: GPU acceleration is not available on macOS (uses CPU by default).

---

## 🪟 Windows Installation

### Step 1: Install ffmpeg

1. Download ffmpeg from: https://ffmpeg.org/download.html
2. Extract the archive
3. Add the `bin` folder to your system PATH

Verify in Command Prompt:
```cmd
ffmpeg -version
```

### Step 2: Install Python Dependencies

```cmd
git clone https://github.com/KetanSon/profanity-censor.git
cd profanity-censor
pip install -r requirements.txt
```

---

## 🐳 Docker Installation

### Using Docker (No Local Installation Needed)

```bash
# Build the image
docker build -t profanity-censor .

# Run with input file
docker run -v $(pwd):/data profanity-censor /data/video.mp4
```

See [DOCKER.md](DOCKER.md) for detailed Docker instructions.

---

## 🧪 Testing Your Installation

Run the test script:

```bash
cd /home/ketan/profanity-censor

# Test with sample file
python3 profanity_censor.py examples/sample.mp4 --list-only

# Expected output:
# 🔍 Transcribing audio: examples/sample.mp4
# ✓ Video loaded: 12000ms
```

Check if everything works:

```bash
# Verify GPU is being used
python3 -c "from faster_whisper import WhisperModel; model = WhisperModel('base', device='cuda'); print('GPU Ready!')"

# Should show: GPU Ready!
```

---

## 📦 Requirements

### Hardware

**Minimum:**
- CPU: 4 cores
- RAM: 8GB
- Storage: 2GB free space

**Recommended:**
- GPU: NVIDIA with CUDA support (RTX 3050 or better)
- RAM: 16GB
- Storage: 10GB free space

### Software

- Python: 3.8, 3.9, 3.10, 3.11, 3.12, 3.14
- ffmpeg: 5.0 or higher
- pip: Latest version

---

## 🔧 Environment Variables

Optional environment variables:

```bash
# Set CUDA device (if multiple GPUs)
export CUDA_VISIBLE_DEVICES=0

# Set Python path (if needed)
export PYTHONPATH="/path/to/profanity-censor:$PYTHONPATH"

# Set cache directory for models
export HF_HOME="/path/to/cache"
```

---

## 📚 Next Steps

- Read the [Quick Start Guide](../QUICKSTART-censor.md)
- Check out [Examples](../examples/)
- Read the full [README](../README.md)

---

## 🆘 Need Help?

- Create an [Issue](https://github.com/KetanSon/profanity-censor/issues)
- Check [FAQ.md](FAQ.md)
- Join Discussions

---

<p align="center">
  Installation successful? <b>Happy Censoring! 🎉</b>
</p>
