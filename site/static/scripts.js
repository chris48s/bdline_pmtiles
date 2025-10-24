function getBaseUrl() {
  const url = window.location;
  const trimmedPath = url.pathname.replace(/\/[^/]*$/, '/');
  return `${url.origin}${trimmedPath}`;
}

function objectToTable(obj) {
  let html = '<table class="striped">';
  for (const [key, value] of Object.entries(obj)) {
    html += `<tr><td>${key}</td><td>${value}</td></tr>`;
  }
  html += "</table>";
  return html;
}

function renderMap(layer) {
  const protocol = new pmtiles.Protocol();
  maplibregl.addProtocol("pmtiles", protocol.tile);
  const PMTILES_URL = getBaseUrl() + "pmtiles/" + layer + ".pmtiles.gz";
  const p = new pmtiles.PMTiles(PMTILES_URL);
  protocol.add(p);

  const style = {
    version: 8,
    sources: {
      tiles: {
        type: "vector",
        url: `pmtiles://${PMTILES_URL}`,
      },
      os: {
        type: "raster",
        tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
        tileSize: 256,
        attribution:
          '© <a href="https://openstreetmap.org/copyright">OpenStreetMap</a>',
      },
    },
    layers: [
      {
        id: "os-baselayer",
        type: "raster",
        source: "os",
        minzoom: 0,
        maxzoom: 19,
      },
      {
        id: "tiles-fill",
        type: "fill",
        source: "tiles",
        "source-layer": layer,
        paint: {
          "fill-color": "#007CAD",
          "fill-opacity": 0.5,
        },
      },
      {
        id: "tiles-line",
        type: "line",
        source: "tiles",
        "source-layer": layer,
        paint: {
          "line-color": "#007CADFF",
          "line-width": 2,
        },
      },
    ],
  };

  p.getMetadata().then(function (data) {
    const map = new maplibregl.Map({
      container: "map",
      zoom: data.vector_layers[0].maxzoom,
      style: style,
    });

    map.on("load", function () {
      const boundsArray = data.antimeridian_adjusted_bounds
        .split(",")
        .map((coord) => parseFloat(coord));
      map.fitBounds(
        [
          [boundsArray[0], boundsArray[1]],
          [boundsArray[2], boundsArray[3]],
        ],
        { linear: false, duration: 0, padding: 50 },
      );
    });

    map.on("click", "tiles-fill", (e) => {
      const coordinates = e.lngLat;
      const description = objectToTable(e.features[0].properties);
      new maplibregl.Popup({
        closeButton: true,
        closeOnClick: true,
        maxWidth: "800px;",
      })
        .setLngLat(coordinates)
        .setHTML(description)
        .addTo(map);
    });

    map.on("mouseenter", "tiles-fill", () => {
      map.getCanvas().style.cursor = "pointer";
    });

    map.on("mouseleave", "tiles-fill", () => {
      map.getCanvas().style.cursor = "";
    });

    map.addControl(new maplibregl.NavigationControl(), "top-right");
  });
}
