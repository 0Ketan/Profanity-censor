#!/usr/bin/env python3
"""
AI-Powered Profanity Censor for Audio/Video
============================================
Version: 1.0.0
License: GPL-3.0
Author: KetanSon
GitHub: https://github.com/yourusername/profanity-censor

A powerful tool for automatically detecting and censoring profanity
in audio and video files using OpenAI Whisper AI.

Features:
- GPU-accelerated transcription (CUDA/RTX compatible)
- Multiple Whisper models (tiny→large)
- Audio/Video support (MP3, MP4, WAV, etc.)
- Timestamp-based precise censorship
- Custom profanity lists
- Batch processing

Usage:
    python3 profanity_censor.py audio.mp4
    python3 profanity_censor.py video.mp3 --model medium
    python3 profanity_censor.py podcast.mp4 --list-only

For more information, visit:
https://github.com/yourusername/profanity-censor
"""

__version__ = "1.0.0"
__author__ = "KetanSon"
__license__ = "GPL-3.0"
__github__ = "https://github.com/yourusername/profanity-censor"

import argparse
import os
import sys
import json
from pathlib import Path

# Audio processing
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import io

# Whisper imports
try:
    from faster_whisper import WhisperModel
except ImportError:
    print("Warning: faster_whisper not found. Install with: pip install faster-whisper")
    print("Falling back to regular whisper (slower)")
    try:
        import whisper
    except ImportError:
        print("Error: whisper not found. Install with: pip install openai-whisper")
        sys.exit(1)

class ProfanityCensor:
    def __init__(self, model_size="base", device="cuda", compute_type="float16"):
        """
        Initialize the profanity censor

        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
            device: 'cuda' for GPU, 'cpu' for CPU
            compute_type: Computation type ('float16', 'float32', 'int8')
        """
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.model = None
        self.profanity_words = set()
        self.beep_sound = None
        self.output_dir = None

        # Load model
        self._load_model()

        # Load profanity list
        self._load_profanity_list()

        # Generate or load beep sound
        self._load_beep_sound()

    def _load_model(self):
        """Load the Whisper model"""
        print(f"Loading Whisper model: {self.model_size}")
        try:
            # Try faster-whisper first
            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type
            )
            self.use_faster = True
            print(f"✓ Loaded faster-whisper model on {self.device}")
        except Exception as e:
            print(f"Failed to load faster-whisper: {e}")
            print("Trying regular whisper...")
            try:
                self.model = whisper.load_model(self.model_size)
                self.use_faster = False
                print(f"✓ Loaded whisper model on CPU")
            except Exception as e2:
                print(f"Failed to load any Whisper model: {e2}")
                sys.exit(1)

    def _load_profanity_list(self):
        """Load the list of profane words"""
        # Built-in profanity list (common English profanities)
        default_profanities = [
            # Strong profanity (will always be censored)
            "fuck", "shit", "bitch", "ass", "damn", "hell", "crap",
            "piss", "dick", "cock", "pussy", "bastard", "motherfucker",
            "fucker", "fucking", "shitty", "bullshit", "asshole",
            "goddamn", "goddam", "damnit", "dammit", "pissed",

            # Slurs and offensive terms (high priority)
            "nigger", "nigga", "faggot", "retard", "retarded",

            # Moderate (can be configured)
            "cunt", "wanker", "bollocks", "tosser", "prick",
            "slut", "whore", "ho", "skank", "douche", "douchebag",

            # Mild (optional)
            "frick", "freaking", "darn", "heck", "crap",

            # Variants with common substitutions
            "fk", "sh1t", "b1tch", "azz", "dam", "pusy",
            "biatch", "fu ck", "f uck", "fuc k"
        ]

        # Try to load from file
        profanity_file = Path(__file__).parent / "profanity_list.txt"
        if profanity_file.exists():
            print(f"Loading profanity list from: {profanity_file}")
            with open(profanity_file, 'r') as f:
                file_words = [line.strip().lower() for line in f if line.strip()]
                self.profanity_words.update(file_words)
        else:
            print("No profanity_list.txt found, using built-in list")
            self.profanity_words.update(default_profanities)

        print(f"✓ Loaded {len(self.profanity_words)} profanity words")

    def _load_beep_sound(self, duration_ms=500, frequency=1000):
        """
        Generate or load beep sound

        Args:
            duration_ms: Duration of beep in milliseconds
            frequency: Frequency of beep in Hz
        """
        # Try to load from file
        beep_file = Path(__file__).parent / "beep.wav"
        if beep_file.exists():
            print(f"Loading beep sound from: {beep_file}")
            self.beep_sound = AudioSegment.from_wav(beep_file)
        else:
            print("No beep.wav found, generating synthetic beep")
            # Generate beep using pydub
            self.beep_sound = self._generate_beep(duration_ms, frequency)

        print(f"✓ Beep sound loaded ({len(self.beep_sound)}ms)")

    def _generate_beep(self, duration_ms=500, frequency=1000):
        """Generate a beep sound"""
        sample_rate = 44100
        duration_sec = duration_ms / 1000.0

        # Generate sine wave
        t = np.linspace(0, duration_sec, int(sample_rate * duration_sec))
        wave = 0.5 * np.sin(2 * np.pi * frequency * t)

        # Convert to 16-bit integers
        audio_data = (wave * 32767).astype(np.int16)

        # Create AudioSegment
        return AudioSegment(
            audio_data.tobytes(),
            frame_rate=sample_rate,
            sample_width=2,
            channels=1
        )

    def transcribe_audio(self, audio_file, language="en"):
        """
        Transcribe audio and detect profanity with timestamps

        Args:
            audio_file: Path to audio file
            language: Language code (default: "en")

        Returns:
            List of profanity detections: [{'word': str, 'start': float, 'end': float}]
        """
        print(f"\n🔍 Transcribing audio: {audio_file}")

        try:
            # Load audio with pydub
            audio = AudioSegment.from_file(audio_file)
            print(f"✓ Audio loaded: {len(audio)}ms, {audio.frame_rate}Hz")

            # Transcribe based on model type
            if self.use_faster:
                return self._transcribe_faster(audio_file, language)
            else:
                return self._transcribe_whisper(audio_file, language)

        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return []

    def _transcribe_faster(self, audio_file, language="en"):
        """Transcribe using faster-whisper"""
        profanity_segments = []

        segments, info = self.model.transcribe(
            audio_file,
            language=language,
            word_timestamps=True,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500)
        )

        print(f"Detected language: {info.language} (probability: {info.language_probability:.2f})")

        for segment in segments:
            for word in segment.words:
                word_text = word.word.strip().lower()
                word_text_clean = ''.join(c for c in word_text if c.isalnum())

                # Check if word is profane
                if word_text_clean in self.profanity_words or word_text in self.profanity_words:
                    profanity_segments.append({
                        'word': word.word,
                        'start': word.start,
                        'end': word.end
                    })
                    print(f"🚫 Profanity detected: '{word.word}' at {word.start:.2f}s - {word.end:.2f}s")

        return profanity_segments

    def _transcribe_whisper(self, audio_file, language="en"):
        """Transcribe using regular whisper"""
        profanity_segments = []

        result = self.model.transcribe(
            audio_file,
            language=language,
            word_timestamps=True
        )

        print(f"Detected language: {result.get('language', 'unknown')}")

        if 'segments' in result:
            for segment in result['segments']:
                if 'words' in segment:
                    for word in segment['words']:
                        word_text = word.get('word', '').strip().lower()
                        word_text_clean = ''.join(c for c in word_text if c.isalnum())

                        start = word.get('start', 0)
                        end = word.get('end', 0)

                        if word_text_clean in self.profanity_words or word_text in self.profanity_words:
                            profanity_segments.append({
                                'word': word.get('word', ''),
                                'start': start,
                                'end': end
                            })
                            print(f"🚫 Profanity detected: '{word.get('word', '')}' at {start:.2f}s - {end:.2f}s")

        return profanity_segments

    def censor_audio(self, audio_file, profanity_segments, output_dir=None, safety_padding_ms=100):
        """
        Censor profanity in audio file

        Args:
            audio_file: Input audio file path
            profanity_segments: List of profanity detections
            output_dir: Output directory (default: same as input with '_censored' suffix)
            safety_padding_ms: Extra milliseconds to censor before/after each word
        """
        if not profanity_segments:
            print("\n✨ No profanity detected!")
            return None

        print(f"\n🔧 Censoring {len(profanity_segments)} profanity segments...")

        # Load audio
        audio = AudioSegment.from_file(audio_file)

        # Track current position in audio
        current_pos = 0
        censored_audio = AudioSegment.empty()

        # Sort profanity segments by start time
        profanity_segments.sort(key=lambda x: x['start'])

        for segment in profanity_segments:
            start_ms = int(segment['start'] * 1000) - safety_padding_ms
            end_ms = int(segment['end'] * 1000) + safety_padding_ms

            # Ensure times are within bounds
            start_ms = max(0, start_ms)
            end_ms = min(len(audio), end_ms)

            # Add audio before this profanity segment
            if start_ms > current_pos:
                censored_audio += audio[current_pos:start_ms]

            # Add beep for profanity segment
            segment_duration = end_ms - start_ms
            if segment_duration > 0:
                beep_to_add = self.beep_sound
                if len(beep_to_add) < segment_duration:
                    # Loop beep if it's shorter than the segment
                    loops = segment_duration // len(beep_to_add) + 1
                    beep_to_add = beep_to_add * loops
                beep_to_add = beep_to_add[:segment_duration]
                censored_audio += beep_to_add

            current_pos = end_ms
            print(f"  Censored '{segment['word']}' at {segment['start']:.2f}s")

        # Add remaining audio
        if current_pos < len(audio):
            censored_audio += audio[current_pos:]

        # Save censored audio
        if output_dir is None:
            audio_path = Path(audio_file)
            output_dir = audio_path.parent / f"{audio_path.stem}_censored"
        else:
            output_dir = Path(output_dir)

        # Create output directory
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"clean_{Path(audio_file).name}"

        # Export
        censored_audio.export(str(output_path), format=Path(audio_file).suffix[1:])

        print(f"\n✅ Censored audio saved to: {output_path}")
        print(f"   Duration: {len(censored_audio)}ms | Size: {output_path.stat().st_size / 1024:.2f} KB")

        # Save metadata
        metadata_path = output_dir / "censorship_log.json"
        with open(metadata_path, 'w') as f:
            json.dump({
                'original_file': str(audio_file),
                'output_file': str(output_path),
                'profanities_found': len(profanity_segments),
                'profanity_segments': profanity_segments
            }, f, indent=2)

        return str(output_path)

    def process_video(self, video_file, output_dir=None):
        """
        Process video file (extracts audio, censors it, then reattaches)

        Args:
            video_file: Path to video file
            output_dir: Output directory
        """
        print(f"\n🎬 Processing video: {video_file}")

        import tempfile
        import subprocess

        # Create temp directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Extract audio
            print("Extracting audio...")
            audio_path = temp_path / "temp_audio.mp3"
            subprocess.run([
                "ffmpeg", "-y",
                "-i", video_file,
                "-vn",
                "-acodec", "libmp3lame",
                "-ar", "44100",
                str(audio_path)
            ], capture_output=True, check=True)

            # Transcribe and detect profanity
            profanity_segments = self.transcribe_audio(str(audio_path))

            if not profanity_segments:
                print("No profanity detected, skipping censorship")
                return None

            # Censor audio
            censored_audio_path = self.censor_audio(
                str(audio_path),
                profanity_segments,
                str(temp_path)
            )

            if not censored_audio_path:
                return None

            # Merge censored audio back with video
            if output_dir is None:
                video_path = Path(video_file)
                output_dir = video_path.parent / f"{video_path.stem}_censored"
            else:
                output_dir = Path(output_dir)

            output_dir.mkdir(exist_ok=True)
            output_video_path = output_dir / f"clean_{Path(video_file).name}"

            print("Merging censored audio with video...")
            subprocess.run([
                "ffmpeg", "-y",
                "-i", video_file,
                "-i", censored_audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-shortest",
                str(output_video_path)
            ], capture_output=True, check=True)

            # Save metadata
            metadata_path = output_dir / "censorship_log.json"
            with open(metadata_path, 'w') as f:
                json.dump({
                    'original_file': str(video_file),
                    'output_file': str(output_video_path),
                    'profanities_found': len(profanity_segments),
                    'profanity_segments': profanity_segments
                }, f, indent=2)

            print(f"\n✅ Censored video saved to: {output_video_path}")
            return str(output_video_path)


def main():
    parser = argparse.ArgumentParser(
        description="Profanity Censor - Automatically censor profanity in audio/video",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Censor an audio file
  python profanity_censor.py audio.mp3

  # Censor a video file
  python profanity_censor.py video.mp4

  # Use specific output directory
  python profanity_censor.py audio.mp3 -o ./clean_output/

  # Use different model
  python profanity_censor.py audio.mp3 --model medium

  # Increase padding around profanity
  python profanity_censor.py audio.mp3 --padding 200
        """
    )

    parser.add_argument("input_file", help="Audio or video file to censor")
    parser.add_argument("-o", "--output", help="Output directory (default: input_censored/)")
    parser.add_argument("-m", "--model", default="base", help="Whisper model size (tiny, base, small, medium, large)")
    parser.add_argument("-d", "--device", default="cuda", help="Device (cuda, cpu)")
    parser.add_argument("-p", "--padding", type=int, default=100, help="Safety padding in milliseconds (default: 100)")
    parser.add_argument("-l", "--language", default="en", help="Audio language code (default: en)")
    parser.add_argument("--list-only", action="store_true", help="Only list profanity, don't censor")
    parser.add_argument("--profanity-file", help="Custom profanity list file")

    args = parser.parse_args()

    # Check if input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: Input file not found: {args.input_file}")
        sys.exit(1)

    # Check ffmpeg
    try:
        import subprocess
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except:
        print("Error: ffmpeg not found. Please install ffmpeg.")
        sys.exit(1)

    # Initialize censor
    print(f"\n🚀 Profanity Censor Starting")
    print(f"   Model: {args.model} | Device: {args.device}")
    print("=" * 50)

    censor = ProfanityCensor(
        model_size=args.model,
        device=args.device
    )

    # Process file
    file_ext = Path(args.input_file).suffix.lower()

    if file_ext in ['.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg']:
        # Audio file
        profanity_segments = censor.transcribe_audio(args.input_file, args.language)

        if args.list_only:
            if profanity_segments:
                print(f"\n🚫 Found {len(profanity_segments)} profanities (list-only mode)")
            else:
                print("\n✨ No profanity detected")
            return

        if profanity_segments:
            censor.censor_audio(args.input_file, profanity_segments, args.output, args.padding)
        else:
            print("\n✨ No profanity detected, nothing to censor")

    elif file_ext in ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm']:
        # Video file
        if args.list_only:
            print("Note: For video files, using a temporary audio extraction...")

        result = censor.process_video(args.input_file, args.output)

        if not result and not args.list_only:
            print("\n✨ No profanity detected, nothing to censor")

    else:
        print(f"Error: Unsupported file format: {file_ext}")
        print("Supported: .mp3, .wav, .mp4, .mkv, .avi, .mov, and more")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("✅ Processing complete!")


if __name__ == "__main__":
    main()
