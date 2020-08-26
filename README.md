# gr-m17
GNU Radio M17 protocol implementation

Requires gnuradio 3.8.2

## Building and Installing

```
git clone https://github.com/sp5wwp/gr-m17
cd gr-m17
cmake -B build
# For Ubuntu 20.04
# cmake -B build -DGR_PYTHON_DIR=/usr/local/lib/python3.8/dist-packages
make -C build
sudo make -C build install
sudo ldconfig
```

## Open example hierarchy

```
gnuradio-companion examples/codec2_exp.grc
```
