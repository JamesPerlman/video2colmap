import os
from pathlib import Path
import re
import subprocess as sp

def get_fps(input_video_path: Path) -> str:
    return sp.getoutput(f" \
        ffprobe -v 0 \
            -of csv=p=0 \
            -select_streams v:0 \
            -show_entries stream=r_frame_rate \
        \"{input_video_path}\" \
    ")

def get_frame_count(input_video_path: Path) -> int:
    frames_str = sp.getoutput(f" \
        ffprobe -v error \
            -select_streams v:0 \
            -count_frames \
            -show_entries stream=nb_read_frames \
            -print_format default=nokey=1:noprint_wrappers=1 \
            {input_video_path} \
        ")
    return int(frames_str)

def extract_frames(
    input_video_path: Path,
    output_frames_path: Path,
    force_redo: bool = False,
):
    if force_redo is False:
        files_in_output_dir = [file for file in os.listdir(output_frames_path) if bool(re.search("\.png$", file))]
        num_frames_in_video = get_frame_count(input_video_path)
        if len(files_in_output_dir) == num_frames_in_video:
            print("Frames have already been extracted.  Skipping...")
            return

    input_video_fps = get_fps(input_video_path)
    print(input_video_path)
    print(output_frames_path)
    os.system(f" \
        ffmpeg \
            -i \"{input_video_path}\" \
            -r \"{input_video_fps}\" \
            -vf \"mpdecimate,setpts=N/FRAME_RATE/TB\" \
            \"{output_frames_path}/%06d.png\" \
    ")
