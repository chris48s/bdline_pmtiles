import subprocess
from pathlib import Path

WORKING_DIR = Path("./working")


def shp_to_geojson(directory):
    print(f"converting shapefiles in {directory} to GeoJSON...")
    geojson_dir = directory / "geojson"
    geojson_dir.mkdir(parents=True, exist_ok=True)
    shp_files = list((directory / "Data/GB").glob("*.shp"))
    for shp_file in shp_files:
        filename = shp_file.stem
        geojson_path = geojson_dir / f"{filename}.geojson"
        subprocess.run(
            [
                "ogr2ogr",
                "-f",
                "GeoJSON",
                "-s_srs",
                "EPSG:27700",
                "-t_srs",
                "EPSG:4326",
                str(geojson_path),
                str(shp_file),
            ],
            check=True,
        )
    return geojson_dir


def geojson_to_pmtiles(directory):
    print(f"converting GeoJSON in {directory} to PMTiles...")
    pmtiles_dir = directory.parent / "pmtiles"
    pmtiles_dir.mkdir(parents=True, exist_ok=True)
    geojson_files = list(directory.glob("*.geojson"))
    for geojson_file in geojson_files:
        filename = geojson_file.stem
        pmtiles_path = pmtiles_dir / f"{filename}.pmtiles"
        subprocess.run(
            ["./tippecanoe/tippecanoe", "-o", str(pmtiles_path), str(geojson_file)],
            check=True,
        )
    return pmtiles_dir


def main():
    dirs = [node for node in WORKING_DIR.iterdir() if node.is_dir()]

    for shp_dir in dirs:
        geojson_dir = shp_to_geojson(shp_dir)
        # TODO: pmtiles_dir = geojson_to_pmtiles(geojson_dir)
        _ = geojson_to_pmtiles(geojson_dir)
        # TODO: copy to output dir
    print("done")


if __name__ == "__main__":
    main()
