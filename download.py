import argparse
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Tuple
import requests


def download_video(url: str, filepath: str) -> None:
    try:
        # Create subdirectory if not exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with requests.get(url, stream=True) as r:
            r.raise_for_status()

            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        print(f"Downloaded {filepath}")
    except Exception as e:
        print(f"Failed to download {filepath}: {str(e)}")


def generate_urls(base_url: str, actions: Dict[str, int]) -> List[Tuple[str, str]]:
    urls: List[Tuple[str, str]] = []

    for action, count in actions.items():
        for i in range(1, count + 1):
            num = f"{i:02d}"
            url = base_url.replace("{ACTION}", action).replace("{NUM}", num)
            filename = f"{action}_{num}.mp4"
            filepath = os.path.join(action.lower(), filename)

            urls.append((url, filepath))

    return urls


def main() -> None:
    parser = argparse.ArgumentParser(description='Golcam video downloader')

    parser.add_argument('--base_url', type=str,
                        default="https://www.golcam.com/GOLCAM/Temporanei/Olimpia1/OLI1SAX25Y25-{ACTION}-{NUM}.mp4",
                        help='Base URL pattern with {ACTION} and {NUM} placeholders')
    parser.add_argument('--actions', type=str, default="AZIONE:50,GOL:15",
                        help='Comma-separated list of action:count pairs')
    parser.add_argument('--threads', type=int, default=5,
                        help='Number of concurrent downloads')
    parser.add_argument('--output_dir', type=str, default="clips",
                        help='Output directory for downloaded clips')

    args = parser.parse_args()

    action_dict: Dict[str, int] = {}
    for pair in args.actions.split(','):
        action, count = pair.split(':')
        action_dict[action] = int(count)

    urls = generate_urls(args.base_url, action_dict)

    os.makedirs(args.output_dir, exist_ok=True)

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        for url, filename in urls:
            executor.submit(download_video, url, f"{args.output_dir}/{filename}")


if __name__ == "__main__":
    main()
