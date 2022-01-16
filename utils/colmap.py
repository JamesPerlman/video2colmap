from enum import Enum
import os
from pathlib import Path

# Register camera / extract features

def register_camera(
    db_path: Path,
    images_path: Path,
    force_redo: bool = False
):
    print("*************************************************")
    print("* Registering camera and extracting features... *")
    print("*************************************************")

    if os.path.isfile(db_path):
        if force_redo:
            db_path.unlink()
        else:
            print("DB file already exists. Skipping...")
            return
    
    os.system(f" \
        colmap feature_extractor \
            --SiftExtraction.upright 1 \
            --ImageReader.camera_model OPENCV \
            --ImageReader.single_camera 1 \
            --database_path \"{db_path}\" \
            --image_path \"{images_path}\" \
    ")

    print("Camera registered and features extracted.")

# Match features

def match_features(
    db_path: Path,
):
    print("************************************************")
    print("* Matching features (using sequential_matcher) *")
    print("************************************************")

    os.system(f" \
        colmap sequential_matcher \
            --database_path {db_path} \
    ")

    print("Features matched.")

# Reconstruct scene (sparse)
def reconstruct_scene(
    db_path: Path,
    images_path: Path,
    project_path: Path,
    force_redo: bool = False
):
    print("************************")
    print("* Reconstructing scene *")
    print("************************")

    output_path = project_path / "sparse"
    cameras_path = output_path / "0/cameras.bin"
    if force_redo is False and cameras_path.exists():
        print("Scene reconstruction already exists. Skipping...")
        return

    output_path.mkdir(exist_ok=True)

    os.system(f" \
        colmap mapper \
            --Mapper.ba_refine_principal_point 1 \
            --Mapper.filter_max_reproj_error 2 \
            --Mapper.tri_complete_max_reproj_error 2 \
            --Mapper.min_num_matches 32 \
            --database_path {db_path} \
            --image_path {images_path} \
            --output_path {output_path} \
    ")

    print("Scene reconstructed.")
