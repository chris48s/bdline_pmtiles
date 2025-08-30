import argparse
import re
import shutil
import urllib.request
import zipfile
from pathlib import Path

WORKING_DIR = Path("./working")


def clear_working_dir():
    if WORKING_DIR.exists():
        shutil.rmtree(WORKING_DIR)
    WORKING_DIR.mkdir(parents=True, exist_ok=True)


def download(url):
    match = re.search(
        r"^https:\/\/parlvid.mysociety.org\/os\/boundary-line\/([^/]+\.zip)$", url
    )
    filename = match.group(1)
    filepath = WORKING_DIR / filename
    print(f"downloading {url} to {filepath} ...")
    urllib.request.urlretrieve(url, filepath)
    return filepath


def unzip(zf):
    directory = WORKING_DIR / Path(zf).stem
    directory.mkdir(parents=True, exist_ok=True)
    print(f"extracting {zf} to {directory} ...")
    with zipfile.ZipFile(zf, "r") as zip_ref:
        zip_ref.extractall(directory)
    return directory


def main(boundaryline_url):
    clear_working_dir()
    zipfile = download(boundaryline_url)
    unzip(zipfile)
    print("done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch boundary line data")
    parser.add_argument(
        "url",
        type=str,
        help="e.g: https://parlvid.mysociety.org/os/boundary-line/bdline_gb-2024-10.zip",
    )
    args = parser.parse_args()

    main(args.url)
