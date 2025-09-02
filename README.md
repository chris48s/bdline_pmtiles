# bdline_pmtiles

[![Run tests](https://github.com/chris48s/bdline_pmtiles/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/chris48s/bdline_pmtiles/actions/workflows/test.yml)

```bash
sudo apt install gdal-bin
sudo apt install gcc g++ make libsqlite3-dev zlib1g-dev

./scripts/build_tippecanoe.sh
python ./scripts/fetch_data.py https://parlvid.mysociety.org/os/boundary-line/bdline_gb-2024-10.zip
python ./scripts/convert.py
python ./scripts/write_staticsite.py "October 2024"

npx http-server@latest .
# http://127.0.0.1:8080/site/
```
