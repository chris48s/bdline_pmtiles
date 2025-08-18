import re
import shutil
import urllib.request
import zipfile
from pathlib import Path

WORKING_DIR = Path("./working")


def get_boundaryline_urls():
    # TODO: scrape https://parlvid.mysociety.org/os/
    # for releases we haven't already seen
    return [
        "https://parlvid.mysociety.org/os/boundary-line/bdline_gb-2025-05.zip",
        "https://parlvid.mysociety.org/os/boundary-line/bdline_gb-2024-10.zip",
    ]


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


def main():
    clear_working_dir()
    boundaryline_urls = get_boundaryline_urls()
    for boundaryline_url in boundaryline_urls:
        zipfile = download(boundaryline_url)
        unzip(zipfile)
    print("done")


if __name__ == "__main__":
    main()
