# Sharpest-Frame Extractor

This Python script scans one or more video files and, for each time interval you specify (default 1 second), finds and saves the single sharpest frame to disk.

---

## Features

- **Automatic focus measure** using the variance of the Laplacian operator
- **Interval-based**: pick the best frame every _n_ seconds
- **Batch mode**: process multiple videos in parallel
- **Output**: choose JPEG or PNG
- **Flat-mode**: optionally save all frames into one directory without per-video subfolders

---

## Requirements

- Python 3.6 or newer
- [OpenCV Python bindings](https://pypi.org/project/opencv-python/)

Install via:

```bash
pip install -r requirements.txt
```

---

## Usage

```bash
./sharpest_frame_extractor.py [VIDEO ...] [--interval N] [--output DIR] [--format {jpg,png}] [--no-subdir]
```

### Arguments

- **VIDEO**
  One or more paths to input video files.

### Options

- `--interval N`
  Time interval (in seconds) between sharp-frame selections.
  **Default:** `1.0`

- `--output DIR`
  Base directory for saving frames.
  **Default:** `sharpest_frames`

- `--format {jpg,png}`
  Output image format.
  **Default:** `jpg`

- `--no-subdir`
  Save all frames directly into the output directory, without creating per-video subfolders.

---

## Examples

1. **Default behavior** (per-video folders, JPEG):

   ```bash
   ./sharpest_frame_extractor.py cam1.mp4 cam2.mp4
   ```

   Creates:
   ```
   sharpest_frames/
   ├─ cam1/
   │  ├─ cam1_0000.jpg
   │  ├─ cam1_0001.jpg
   │  └─ …
   └─ cam2/
      ├─ cam2_0000.jpg
      ├─ cam2_0001.jpg
      └─ …
   ```

2. **Custom interval & PNG**:

   ```bash
   ./sharpest_frame_extractor.py footage.mp4 --interval 2.5 --format png --output best_pngs
   ```

3. **Flat mode** (no subfolders):

   ```bash
   ./sharpest_frame_extractor.py cam1.mp4 cam2.mp4 --no-subdir --output flat_frames
   ```

   Creates:
   ```
   flat_frames/
   ├─ cam1_0000.jpg
   ├─ cam1_0001.jpg
   ├─ cam2_0000.jpg
   ├─ cam2_0001.jpg
   └─ …
   ```

---

## License

MIT License
