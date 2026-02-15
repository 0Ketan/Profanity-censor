#!/bin/bash
# Batch Processing Example
# Process all MP3 files in the current directory

echo "🎬 Batch Processing Demo"
echo "========================"
echo "Processing all MP3 files in current directory..."
echo ""

# Ensure we're in the examples directory
cd "$(dirname "$0")"

# Check for MP3 files
mp3_files=(*.mp3)

if [ ${#mp3_files[@]} -eq 0 ] || [ "${mp3_files[0]}" = "*.mp3" ]; then
    echo "No MP3 files found!"
    echo "Place some MP3 files in the examples/ directory first."
    exit 1
fi

# Process each file
count=0
for file in *.mp3; do
    if [ -f "$file" ]; then
        echo "Processing: $file"
        python3 ../profanity_censor.py "$file" --model tiny
        ((count++))
        echo "---"
    fi
done

echo ""
echo "✅ Finished processing $count files!"
echo "Converted versions are in respective directories."
