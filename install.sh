#!/bin/bash

git clone https://github.com/sp5wwp/gr-m17
cd gr-m17
mkdir build && cd build
cmake -B ../
# For Ubuntu 20.04
# cmake -B build -DGR_PYTHON_DIR=/usr/local/lib/python3.8/dist-packages
cd ..
make -C build
sudo make -C build install
sudo ldconfig