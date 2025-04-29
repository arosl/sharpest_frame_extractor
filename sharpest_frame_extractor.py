#!/usr/bin/env python3
import cv2
import os
import argparse
from concurrent.futures import ThreadPoolExecutor

def variance_of_laplacian(image):
    """Compute the Laplacian variance of an image (focus measure)."""
    return cv2.Laplacian(image, cv2.CV_64F).var()

def save_frame(frame, path, image_format="jpg"):
    """Save a frame to disk in specified format."""
    ext = image_format.lower()
    filename = f"{path}.{ext}"
    cv2.imwrite(filename, frame)

def get_video_properties(video_path):
    """Open video and retrieve basic properties."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video file: {video_path}")
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps else 0
    return cap, fps, frame_count, duration

def extract_best_frames(cap, fps, interval_sec):
    """
    Generator that yields the sharpest frame for each interval.
    Yields (interval_index, frame).
    """
    best_frame = None
    best_focus = -1
    prev_interval = 0
    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            if best_frame is not None:
                yield prev_interval, best_frame
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        focus = variance_of_laplacian(gray)
        time_in_sec = frame_index / fps if fps else 0
        interval_idx = int(time_in_sec // interval_sec)

        if interval_idx != prev_interval:
            if best_frame is not None:
                yield prev_interval, best_frame
            prev_interval = interval_idx
            best_frame = frame
            best_focus = focus
        else:
            if focus > best_focus:
                best_focus = focus
                best_frame = frame

        frame_index += 1

def process_video(video_path, output_folder, interval_sec=1.0, image_format="jpg", no_subdir=False):  # noqa: C901
    """Process a single video: extract and save the sharpest frame per interval."""
    # Ensure base output folder exists
    os.makedirs(output_folder, exist_ok=True)

    try:
        cap, fps, frame_count, duration = get_video_properties(video_path)
    except IOError as e:
        print(f"Warning: {e}")
        return

    base_name = os.path.splitext(os.path.basename(video_path))[0]
    print(f"Processing {video_path}: FPS={fps:.2f}, Frames={frame_count}, Duration={duration:.2f}s")

    # Determine where to save frames for this video
    if no_subdir:
        save_dir = output_folder
    else:
        save_dir = os.path.join(output_folder, base_name)
    os.makedirs(save_dir, exist_ok=True)

    # Extract and save best frames
    for interval_idx, frame in extract_best_frames(cap, fps, interval_sec):
        save_path = os.path.join(save_dir, f"{base_name}_{interval_idx:04d}")
        save_frame(frame, save_path, image_format)

    cap.release()
    print(f"Finished processing {video_path}")

def process_videos_concurrently(video_paths, output_base_folder, interval_sec=1.0, image_format="jpg", no_subdir=False):
    """Process multiple videos concurrently."""
    with ThreadPoolExecutor() as executor:
        for video_path in video_paths:
            executor.submit(
                process_video,
                video_path,
                output_base_folder,
                interval_sec,
                image_format,
                no_subdir
            )

def main():
    parser = argparse.ArgumentParser(
        description="Extract sharpest frames from videos at specified intervals."
    )
    parser.add_argument(
        "videos", nargs="+", help="Path(s) to video file(s)"
    )
    parser.add_argument(
        "--interval", type=float, default=1.0,
        help="Interval in seconds between sharp-frame selections (default: 1s)"
    )
    parser.add_argument(
        "--output", type=str, default="sharpest_frames",
        help="Base output directory (default: sharpest_frames)"
    )
    parser.add_argument(
        "--format", type=str, default="jpg", choices=["jpg", "png"],
        help="Image format to save (jpg or png)"
    )
    parser.add_argument(
        "--no-subdir", action="store_true",
        help="Do not create per-video subdirectories; save all frames directly into output directory"
    )

    args = parser.parse_args()
    process_videos_concurrently(
        args.videos,
        args.output,
        args.interval,
        args.format,
        args.no_subdir
    )

if __name__ == "__main__":
    main()
