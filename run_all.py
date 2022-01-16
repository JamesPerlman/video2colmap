import utils

def execute(
    input_video_path: str,
    output_folder_path: str,
):
    # Extract frames
    frames_folder_path = output_folder_path / "images"
    frames_folder_path.mkdir(parents=True, exist_ok=True)
    utils.ffmpeg.extract_frames(input_video_path, frames_folder_path)

    # COLMAP
    colmap_db_path = output_folder_path / "database.db"

    utils.colmap.register_camera(colmap_db_path, frames_folder_path)

    utils.colmap.match_features(colmap_db_path)

    utils.colmap.reconstruct_scene(colmap_db_path, frames_folder_path, output_folder_path)
