import argparse
import os
from pathlib import Path

import utils

# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="Input video file path")
parser.add_argument("-o", "--output", required=True, help="Output folder path for colmap project")

# Get argument values
args = parser.parse_args()
input_video_path = Path(args.input)
output_folder_path = Path(args.output)

# Extract frames
frames_folder_path = output_folder_path / "images"
frames_folder_path.mkdir(parents=True, exist_ok=True)
utils.ffmpeg.extract_frames(input_video_path, frames_folder_path)

# Run COLMAP
colmap_db_path = output_folder_path / "database.db"
utils.colmap.extract_features(colmap_db_path, frames_folder_path)
