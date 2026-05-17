import argparse
from pathlib import Path

index_template = """
<!DOCTYPE html>
  <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
      <title>BoundaryLine {suffix}</title>
    </head>
    <body>
      <main class="container">
        <h1>BoundaryLine {suffix}</h1>
        {menu}
      </main>
    </body>
  </html>
"""

detail_template = """
<!DOCTYPE html>
  <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
      <link rel="stylesheet" href="https://unpkg.com/maplibre-gl@5.6.2/dist/maplibre-gl.css" />
      <script src="https://unpkg.com/maplibre-gl@5.6.2/dist/maplibre-gl.js"></script>
      <script src="https://unpkg.com/pmtiles@3.2.0/dist/pmtiles.js"></script>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
      <title>BoundaryLine {suffix}: {layer}</title>
    </head>
    <body>
      <main class="container">
        <h1>BoundaryLine {suffix}: {layer}</h1>
        <div id="map" style="height: 600px;"></div>
        {menu}
        <script src="static/scripts.js"></script>
        <script>
          document.addEventListener("DOMContentLoaded", renderMap("{layer}"));
        </script>
        <style>
          button.maplibregl-ctrl-zoom-in {{
            margin-bottom: 0px;
            border-radius: 0px;
          }}
          button.maplibregl-ctrl-zoom-out {{
            margin-bottom: 0px;
            border-radius: 0px;
          }}
          button.maplibregl-ctrl-compass {{
            margin-bottom: 0px;
            border-radius: 0px;
          }}
          button.maplibregl-popup-close-button {{
            margin-bottom: 0px;
            padding: 0.25rem 0.5rem;
          }}
          .maplibregl-popup-content td {{
            padding: 0.25rem;
          }}
        </style>
      </main>
    </body>
  </html>
"""


def get_menu(layers):
    menu_str = "<aside><nav><ul>"
    menu_str = menu_str + '<li><a href="index.html">Home</a></li>'
    for layer in layers:
        menu_str = menu_str + f'<li><a href="{layer}.html">{layer}</a></li>'
    menu_str = menu_str + "</ul></nav></aside>"
    return menu_str


def main(suffix):
    site_dir = Path("site")
    for html_file in site_dir.glob("*.html"):
        html_file.unlink()

    tiles_dir = site_dir / "pmtiles"
    files = list(tiles_dir.glob("*.pmtiles"))
    layers = sorted([f.stem for f in files])
    menu = get_menu(layers)
    for layer in layers:
        print(f"writing {layer}.html ...")
        (Path("site") / f"{layer}.html").write_text(
            detail_template.format(layer=layer, menu=menu, suffix=suffix)
        )

    print("writing index.html ...")
    (Path("site") / "index.html").write_text(
        index_template.format(menu=menu, suffix=suffix)
    )
    print("done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Write static site to display PMTiles")
    parser.add_argument(
        "suffix",
        type=str,
        help='e.g: "October 2024"',
    )
    args = parser.parse_args()

    main(args.suffix)
