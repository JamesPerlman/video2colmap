import argparse
import os
from pathlib import Path

import run_all
import utils

# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="Input video file path")
parser.add_argument("-o", "--output", required=True, help="Output folder path for colmap project")

# Get argument values
args = parser.parse_args()
input_video_path = Path(args.input)
output_folder_path = Path(args.output)

run_all.execute(input_video_path, output_folder_path)
