#!/bin/bash

# Check if the user has provided source and destination folders
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <source_folder> <destination_folder>"
    exit 1
fi

# Assign source and destination folders to variables
src_folder="$1"
dst_folder="$2"


# Reset the SECONDS variable
SECONDS=0

# Function to perform conversion
convert_to_webp() {
    src_file="$1"
    src_folder="$2"
    dst_folder="$3"

    # Create the corresponding sub-folder structure in the destination folder
    sub_folder=$(dirname "${src_file#$src_folder}")
    mkdir -p "$dst_folder/$sub_folder"

    # Construct the destination file path with webp extension
    dst_file="$dst_folder/${src_file#$src_folder}"
    dst_file="${dst_file%.png}.webp"

    # Convert the png file to webp with quality 85
    convert "$src_file" -background none -quality 85 "$dst_file"

    # echo "Converted $src_file to $dst_file"
}

# Export the function for parallel
export -f convert_to_webp

# Find all png files in the source folder recursively and convert them in parallel
find "$src_folder" -type f -name '*.png' | parallel --eta --jobs "$(nproc)" convert_to_webp {} "$src_folder" "$dst_folder"

echo "Compression completed!"

# Print the elapsed time
elapsed_time=$SECONDS
echo "Total elapsed time: $((elapsed_time / 60)) minutes and $((elapsed_time % 60)) seconds"

# Copy the tilemapresource.xml file to the new destination
cp "$src_folder/tilemapresource.xml" "$dst_folder"

# Replace the text "png" with "webp" in the tilemapresource.xml file
sed -i 's/png/webp/g' "$dst_folder/tilemapresource.xml"
