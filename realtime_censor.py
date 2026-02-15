#!/usr/bin/env python3
"""
Real-Time Profanity Censor
Records video/audio and censors profanities as they're detected
"""

import argparse
import cv2
import numpy as np
import pyaudio
import wave
import threading
import time
import sys
from pathlib import Path
from datetime import datetime
import asyncio

# Import our profanity censor
from profanity_censor import ProfanityCensor

# Global state variables
audio_buffer = []
buffer_lock = threading.Lock()
profanity_segments = []
recording_active = False

class RealTimeCensor:
    def __init__(self, model_size="base", device="cuda"):
        """
        Initialize real-time censor

        Args:
            model_size: Whisper model size
            device: cuda or cpu
        """
        self.model_size = model_size
        self.device = device
        self.censor = ProfanityCensor(model_size=model_size, device=device)
        self.audio_chunk_duration = 30.0  # seconds per chunk
        self.sample_rate = 16000
        self.channels = 1
        self.chunk_size = 1024
        self.output_dir = Path("recordings")
        self.output_dir.mkdir(exist_ok=True)

        # Cache beep sound
        from pydub.generators import Sine
        self.beep_sound = Sine(1000).to_audio_segment(duration=500)  # 1kHz tone, 500ms

    def start_recording(self, duration_seconds=None):
        """
        Start recording video with synchronized audio

        Args:
            duration_seconds: Total recording length (None = record until stopped)
        """
        global recording_active, profanity_segments
        recording_active = True
        profanity_segments = []

        # Files for raw recordings
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.raw_video = self.output_dir / f"raw_{timestamp}.mp4"
        self.raw_audio = self.output_dir / f"raw_{timestamp}.wav"
        self.censored_video = self.output_dir / f"censored_{timestamp}.mp4"
        self.final_video = self.output_dir / f"final_{timestamp}.mp4"  # Video WITH audio

        # Start audio recording thread
        audio_thread = threading.Thread(target=self._record_audio, args=(duration_seconds,))
        audio_thread.start()

        # Start video recording
        self._record_video(duration_seconds)

        # Wait for audio to complete
        audio_thread.join()

        # Generate final censored video
        self._generate_final_video()

        # Combine video with audio
        self._combine_audio_video()

        # Clean up raw files (optional)
        # self.raw_video.unlink()
        # self.raw_audio.unlink()

        print("✅ Recording complete!")
        print(f"\n📹 Files saved:")
        print(f"   • censored_*.mp4 - Video with visual indicators only (no sound)")
        print(f"   • final_*.mp4      - Video with visual indicators + audio (watch this!)")

    def _record_audio(self, duration_seconds):
        """Record audio in chunks and process each chunk"""
        global recording_active
        p = pyaudio.PyAudio()

        # Open audio stream
        stream = p.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

        print("🔊 Recording audio...")

        # Open WAV file for full recording
        full_wf = wave.open(str(self.raw_audio), 'wb')
        full_wf.setnchannels(self.channels)
        full_wf.setsampwidth(2)  # 16-bit
        full_wf.setframerate(self.sample_rate)

        chunk_frames = []
        chunk_start_time = 0

        # WARM-UP: Discard first few audio reads to ensure PyAudio is ready
        # This prevents initial silent/quiet frames at the beginning
        print("   Warming up audio stream...")
        warm_up_frames = 5
        for _ in range(warm_up_frames):
            try:
                stream.read(self.chunk_size)
            except Exception as e:
                print(f"   Warning during warm-up: {e}")

        print("   ✓ Audio stream ready, recording started")

        while recording_active:
            # Read audio chunk
            data = stream.read(self.chunk_size)
            chunk_frames.append(data)

            # Write to full recording
            full_wf.writeframes(data)

            # Check if we've collected enough for a full chunk
            elapsed = len(chunk_frames) * self.chunk_size / self.sample_rate

            if elapsed >= self.audio_chunk_duration:
                # Process this chunk
                self._process_audio_chunk(chunk_frames, chunk_start_time)

                # Reset for next chunk
                chunk_frames = []
                chunk_start_time += self.audio_chunk_duration

            # Check duration limit
            if duration_seconds and chunk_start_time >= duration_seconds:
                break

        # Process final partial chunk
        if chunk_frames:
            self._process_audio_chunk(chunk_frames, chunk_start_time)

        # Close full recording
        full_wf.close()

        stream.stop_stream()
        stream.close()
        p.terminate()

    def _process_audio_chunk(self, frames, start_time):
        """Process one audio chunk for profanity"""
        global profanity_segments

        print(f"  Processing chunk from {start_time:.1f}s...")

        # Save chunk to temp file
        chunk_file = self.output_dir / f"chunk_{start_time:.0f}.wav"

        with wave.open(str(chunk_file), 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(frames))

        # Transcribe chunk
        segments = self.censor.transcribe_audio(str(chunk_file), language="en")

        # Adjust timestamps and add to global list
        for segment in segments:
            segment['start'] += start_time
            segment['end'] += start_time
            profanity_segments.append(segment)
            print(f"    🚫 Detected: '{segment['word']}' at {segment['start']:.2f}s")

        # Clean up temp file
        chunk_file.unlink()

    def _record_video(self, duration_seconds):
        """Record video frames"""
        global recording_active
        cap = cv2.VideoCapture(0)  # Default webcam

        fps = 30
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Prepare video writer
        self.raw_video = self.output_dir / f"raw_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(self.raw_video), fourcc, fps, (width, height))

        print("🎥 Recording video... Press 'q' to stop early")

        start_time = time.time()

        while recording_active:
            ret, frame = cap.read()
            if ret:
                out.write(frame)

                # Display frame
                cv2.imshow('Recording (press Q to stop)', frame)

                # Check for stop key
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # Check duration
            elapsed = time.time() - start_time
            if duration_seconds and elapsed >= duration_seconds:
                break

        # Stop recording
        recording_active = False
        cap.release()
        out.release()
        cv2.destroyAllWindows()

    def _generate_final_video(self):
        """Generate final censored video by overlaying beeps"""
        print("🎬 Generating final censored video...")

        # Load the raw video
        cap = cv2.VideoCapture(str(self.raw_video))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Prepare output video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(self.censored_video), fourcc, fps, (width, height))

        # Process each frame
        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Check if this frame has profanity
            current_time = frame_idx / fps
            frame_has_profanity = any(seg['start'] <= current_time <= seg['end'] for seg in profanity_segments)

            # Add visual indicator
            if frame_has_profanity:
                cv2.circle(frame, (50, 50), 20, (0, 0, 255), -1)  # Red dot
                cv2.putText(frame, "🔇", (width - 100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            out.write(frame)
            frame_idx += 1

            if frame_idx % 60 == 0:
                print(f"  Progress: {frame_idx}/{total_frames} frames...")

        cap.release()
        out.release()

        print(f"✅ Censored video created (visual only, no sound): {self.censored_video}")

    def _combine_audio_video(self):
        """Combine censored video with beep-censored audio using ffmpeg"""
        print("\n🔊 Processing audio censorship (adding beeps)...")

        import subprocess
        from pydub import AudioSegment
        from pydub.generators import Sine

        # Check if raw audio exists
        if not self.raw_audio.exists():
            print(f"❌ ERROR: Audio file not found: {self.raw_audio}")
            print("   Cannot create final video without audio!")
            return

        # Check if censored video exists
        if not self.censored_video.exists():
            print(f"❌ ERROR: Censored video not found: {self.censored_video}")
            print("   Cannot combine audio with missing video!")
            return

        # Generate beep sound
        beep = Sine(1000).to_audio_segment(duration=500)  # 1kHz tone, 500ms

        # Load the original audio
        try:
            audio = AudioSegment.from_wav(str(self.raw_audio))
            sample_rate = audio.frame_rate
            channels = audio.channels

            print(f"  ✓ Loaded audio: {len(audio)}ms, {sample_rate}Hz, {channels} channels")
            print(f"  Found {len(profanity_segments)} profanity segments to censor...")

            if len(profanity_segments) == 0:
                print("  ℹ️ No profanity detected, copying original audio")
                censored_audio = audio
            else:
                # Create beep-censored audio
                censored_audio = AudioSegment.empty()
                last_end_ms = 0

                # Sort profanity segments
                sorted_segments = sorted(profanity_segments, key=lambda x: x['start'])

                print(f"  Processing {len(sorted_segments)} segments...")

                # Build beep-censored audio
                for i, segment in enumerate(sorted_segments):
                    start_ms = int(float(segment['start']) * 1000)
                    end_ms = int(float(segment['end']) * 1000)

                    # Preserve audio before this profanity
                    censored_audio += audio[last_end_ms:start_ms]

                    # Add beep (adjust duration to match profanity length)
                    profanity_duration = end_ms - start_ms
                    censored_audio += beep[:profanity_duration]
                    print(f"    [{i+1}/{len(sorted_segments)}] {segment['word']} at {segment['start']:.2f}s")

                    last_end_ms = end_ms

                # Add remaining audio after last profanity
                censored_audio += audio[last_end_ms:]

            # Export beep-censored audio
            censored_audio_path = self.output_dir / f"censored_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            censored_audio.export(str(censored_audio_path), format='wav')

            print(f"  ✓ Created censored audio: {censored_audio_path}")

        except Exception as e:
            print(f"❌ ERROR: Failed to create censored audio: {e}")
            print(f"   This might mean:")
            print(f"   - Audio format is not supported")
            print(f"   - pydub couldn't read the audio file")
            print(f"   - Audio is corrupted or empty")
            print(f"   Will attempt to use original audio instead.")
            censored_audio_path = self.raw_audio

        # Use ffmpeg to combine video and beep-censored audio
        print("\n  Combining video + beep-censored audio...")
        print(f"   Video: {self.censored_video}")
        print(f"   Audio: {censored_audio_path}")
        print(f"   Output: {self.final_video}")

        cmd = [
            'ffmpeg', '-y',
            '-i', str(self.censored_video),      # Input video (with visual indicators)
            '-i', str(censored_audio_path),      # Input audio (beep-censored)
            '-c:v', 'copy',                       # Copy video codec (no re-encoding)
            '-c:a', 'aac',                        # Use AAC audio codec
            '-b:a', '192k',                       # Audio bitrate
            '-async', '1',                        # Sync audio to video
            '-vsync', '1',                        # Ensure video sync
            '-shortest',                          # Use shortest stream duration
            '-fflags', '+genpts',                 # Generate missing PTS
            '-af', 'aresample=async=1',           # Resample audio for sync
            '-strict', 'experimental',            # Allow experimental codecs if needed
            str(self.final_video)                 # Output video with beep-censored audio
        ]

        try:
            print("  Running ffmpeg...")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            print(f"  ✓ ffmpeg completed successfully")
            print(f"\n✅ Video with beep-censored audio saved:")
            print(f"   {self.final_video}")

            # Verify file exists and has content
            if self.final_video.exists() and self.final_video.stat().st_size > 0:
                file_size_mb = self.final_video.stat().st_size / (1024 * 1024)
                print(f"   File size: {file_size_mb:.2f} MB")
            else:
                print(f"❌ WARNING: Output file not created or empty!")

            # Clean up temp censored audio file
            if censored_audio_path != self.raw_audio and censored_audio_path.exists():
                censored_audio_path.unlink()
                print(f"  Cleaned up temp file")

        except subprocess.CalledProcessError as e:
            print(f"\n❌ ERROR: ffmpeg failed to combine audio and video!")
            print(f"\n  Error details:")
            print(f"  - Return code: {e.returncode}")
            if e.stderr:
                print(f"  - Error output:\n{e.stderr}")
            print(f"\n  Troubleshooting steps:")
            print(f"  1. Check ffmpeg is installed: ffmpeg -version")
            print(f"  2. Check input files exist and are valid")
            print(f"  3. Try running ffmpeg manually with the same command")
            print(f"  4. Check video and audio codecs are compatible")

        except Exception as e:
            print(f"  ⚠️  Unexpected error: {e}")
            print(f"   Your censored video is available (without sound): {self.censored_video}")
            # Fallback: copy video as final
            self.final_video = self.censored_video

    def display_summary(self):
        """Display detected profanities"""
        print("\n" + "="*60)
        print("📊 Processing Summary")
        print("="*60)
        print(f"Total profanities detected: {len(profanity_segments)}")
        print()

        for i, seg in enumerate(profanity_segments[:5]):  # Show first 5
            print(f"  {i+1}. '{seg['word']}' at {seg['start']:.2f}s")

        if len(profanity_segments) > 5:
            print(f"  ... and {len(profanity_segments) - 5} more")

        print("\n")


def main():
    parser = argparse.ArgumentParser(description="Real-Time Profanity Censor")
    parser.add_argument(
        "--duration", "-d",
        type=int,
        help="Recording duration in seconds"
    )
    parser.add_argument(
        "--model", "-m",
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size"
    )
    parser.add_argument(
        "--device",
        default="cuda",
        choices=["cuda", "cpu"],
        help="Processing device"
    )

    args = parser.parse_args()

    print("🎬 Real-Time Profanity Censor v1.0.0")
    print("="*60)
    print(f"Model: {args.model} | Device: {args.device}")
    print("="*60)
    print()

    # Initialize censor
    censor = RealTimeCensor(model_size=args.model, device=args.device)

    try:
        censor.start_recording(duration_seconds=args.duration)
    except KeyboardInterrupt:
        global recording_active
        recording_active = False
        print("\n\n⏹️  Recording stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    # Display summary
    censor.display_summary()


if __name__ == "__main__":
    main()
