import os
from pathlib import Path

def extract_features(
    db_path: Path,
    images_path: Path,
    force_redo: bool = False
):
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