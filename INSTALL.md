# INSTALL Guide for Real-Time Censor

## Step 1: Install System Dependencies (Fedora)

Run these commands in your terminal:

```bash
# Install PortAudio development headers
sudo dnf install -y \
    portaudio-devel \
    alsa-lib-devel \
    python3-devel \
    gcc \
    gcc-c++ \
    make
```

## Step 2: Install PyAudio (requires system PortAudio)

```bash
# Install PyAudio
pip3 install --user pyaudio
```

## Step 3: Install Other Python Packages

```bash
pip3 install --user \
    opencv-python \
    numpy \
    pydub \
    faster-whisper
```

## Step 4: Run Realtime Censor

```bash
cd /home/ketan/profanity-censor
python3 realtime_censor.py --model base
```

Press **Ctrl+C** to stop recording.

## Troubleshooting

If you get "ModuleNotFoundError":
- Make sure you ran `sudo dnf install portaudio-devel` first
- Try: `pip3 install --user --no-cache-dir pyaudio`

If you get "No device":
- Make sure your microphone is connected
- Run: `arecord -l` to list devices
