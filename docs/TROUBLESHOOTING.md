# Troubleshooting Guide

## Quick Fixes for Common Issues

---

## 🐛 "ModuleNotFoundError: No module named 'XYZ'"

**Problem:** Missing Python package

**Solution:**
```bash
pip install -r requirements.txt
```

**Common missing packages:**
```bash
pip install faster-whisper pydub numpy
```

---

## 🐛 "ffmpeg: command not found"

**Problem:** ffmpeg is not installed or not in PATH

**Solution:**

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
- Download from: https://ffmpeg.org/download.html
- Add to PATH

**Verify:**
```bash
ffmpeg -version
```

---

## 🐛 "CUDA failed or CUDA not available"

**Problem:** GPU acceleration not working

**Solution 1 - Force CPU:**
```bash
python3 profanity_censor.py audio.mp3 --device cpu
```

**Solution 2 - Check CUDA:**
```bash
python3 -c "import torch; print(torch.cuda.is_available())"
```

If this prints `False`, your GPU isn't configured correctly. Use CPU mode instead.

---

## 🐛 "torch.cuda.OutOfMemoryError"

**Problem:** GPU ran out of memory

**Solution:**
```bash
# Use smaller model
python3 profanity_censor.py audio.mp3 --model tiny
# or
python3 profanity_censor.py audio.mp3 --model base
```

You can also try:
```bash
# Clear GPU memory
nvidia-smi --gpu-reset # Requires sudo
```

---

## 🐛 "ValueError: Model not found"

**Problem:** Whisper model failed to download

**Solution:**
```bash
# Manually download model
python3 -c "from faster_whisper import WhisperModel; WhisperModel('base', device='cuda')"
```

For slow internet, use smaller model:
```bash
python3 profanity_censor.py audio.mp3 --model tiny
```

---

## 🐛 "No profanity detected"

**Problem:** Script didn't find profanity

**Solution 1 - Check Audio:**
```bash
# Verify audio has clear speech
ffplay audio.mp3  # or vlc, mpv, etc.
```

**Solution 2 - Try a different model:**
```bash
# Use larger model for better accuracy
python3 profanity_censor.py audio.mp3 --model small
```

**Solution 3 - Increase sensitivity:**
```bash
# Lower confidence threshold
# (coming in next version)
```

**Solution 4 - Check profanity list:**
```bash
cat profanity_list.txt
```

Add your words if missing.

---

## 🐛 "Incorrect timestamps" or "Wrong words censored"

**Problem:** Beep is at wrong location or censors wrong word

**Solution 1 - Adjust padding:**
```bash
# Increase padding around profanity
python3 profanity_censor.py audio.mp3 --padding 200
```

**Solution 2 - Check detection:**
```bash
# See what was detected first
python3 profanity_censor.py audio.mp3 --list-only
```

**Solution 3 - Review log:**
```bash
cat input_censored/censorship_log.json
```

---

## 🐛 Audio is garbled or robotic

**Problem:** Output audio quality is poor

**Solution:**

**1. Use lossless intermediate format:**
```bash
python3 profanity_censor.py audio.wav --model base
```

**2. Adjust beep volume:**
Edit `profanity_censor.py` and change:
```python
# Line ~200
beep_to_add = beep_to_add - 3  # Lower volume by 3dB
```

---

## 🐛 "Permission denied"

**Problem:** Cannot write output files

**Solution:**
```bash
# Check permissions
ls -la

# Change ownership
sudo chown $USER:$USER -R profanity-censor/

# Make script executable
chmod +x profanity_censor.py
```

---

## 🐛 Video output has no audio

**Problem:** Censored video lost audio track

**Solution:**
Verify ffmpeg can read both streams:
```bash
ffmpeg -i input.mp4 -i input_censored/clean_audio.mp3 \
  -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4
```

If this works, check `profanity_censor.py` line ~300 for merge command.

---

## 🐛 Very slow processing

**Problem:** Processing is much slower than expected

**Solution:**

**1. Check device:**
```bash
# Verify GPU is being used
python3 -c "from faster_whisper import WhisperModel; model = WhisperModel('base'); print('Using GPU:', model.device)"
```

**2. Use smaller model:**
```bash
python3 profanity_censor.py audio.mp3 --model tiny
```

**3. CPU only (if GPU is problematic):**
```bash
python3 profanity_censor.py audio.mp3 --device cpu
```

---

## 🐛 Python version issues

**Problem:** Newer Python versions (3.14+) have audioop issues

**Solution:**
Already fixed in requirements.txt, but if you see:
```
ModuleNotFoundError: No module named 'audioop'
```

Install:
```bash
pip install audioop-lts
```

---

## 🐛 "unable to load librairy opus"

**Problem:** Missing opus codec

**Solution:**
```bash
# Ubuntu/Debian
sudo apt install libopus0 opus-tools

# Fedora
sudo dnf install opus-tools
```

---

## 🐛 "No such file or directory"

**Problem:** Input file not found

**Solution:**
```bash
# Use absolute path
python3 profanity_censor.py /full/path/to/audio.mp4

# Or relative path from project directory
cd /home/ketan/profanity-censor
python3 profanity_censor.py examples/sample.mp4
```

---

## 🐛 Batch processing fails mid-way

**Problem:** Processing multiple files stops after first error

**Solution:**
```bash
# Add error handling
for file in *.mp4; do
  echo "Processing: $file"
  python3 profanity_censor.py "$file" 2>&1 || echo "Failed: $file"
done
```

---

## 📞 Still Need Help?

If you're still having issues:

1. **Create an Issue**: https://github.com/KetanSon/profanity-censor/issues
2. **Include:**
   - Error message
   - Python version: `python3 --version`
   - ffmpeg version: `ffmpeg -version`
   - GPU info: `nvidia-smi` (if applicable)
   - Command you ran
   - Sample file size/format

We're here to help! 🙏

---

<p align="center">
  <i>Common issues usually have simple solutions! Don't give up! 💪</i>
</p>
