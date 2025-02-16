# Golcam Video Downloader

A configurable Python script for bulk downloading football videos from specific matches on 
[golcam](https://www.golcam.com/).
Concurrent downloads and custom ranges for different action types are supported.

## Features

- Customizable base URL pattern with `{ACTION}` and `{NUM}` placeholders
- Multiple thread support for concurrent downloads
- Configurable actions/ranges via command line
- Automatic organization into customizable output directory
  - divided into subfolders by action type, for example:
    ```text
    clips/
    ├── azione/
    │ ├── AZIONE_01.mp4
    │ ├── AZIONE_02.mp4
    │ └── ...
    └── gol/
      ├── GOL_01.mp4
      ├── GOL_02.mp4
      └── ...
    ```
- Error handling and progress reporting

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Default configuration (AZIONE 1-50 + GOL 1-15)
python downloader.py

# Custom output directory
python downloader.py --output_dir "downloads"

# Custom thread count
python downloader.py --threads 10

# Custom actions/ranges
python downloader.py --actions "AZIONE:20,GAL:5"

# Custom base URL
python downloader.py --base_url "https://www.golcam.com/GOLCAM/Temporanei/Olimpia1/OLI1SAX25Y25-{ACTION}-{NUM}.mp4"
```

## Notes
- Written in Python 3.12
- `requirements.txt` contains necessary dependencies
- Failed downloads are reported in the console and skipped