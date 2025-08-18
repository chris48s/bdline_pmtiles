#!/bin/bash
set -euo pipefail

git clone https://github.com/felt/tippecanoe.git
cd tippecanoe
git checkout 2.79.0
make -j
