# litemate
Continuous colorimeter for cinematography

first version of litemate was initially coded as a python script for resolve
further development will be made in a completely different way as an OpenFX plugin coded in C

# dependencies

 - cupy - cuda 13 - install command: py -3.12 -m pip install cupy-cuda13x
 - PyTorch 2.11 - install command: py -3.12 -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu130
 - TorchCodec 0.11 - cuda 12, PyTorch 2.11 - install command: conda install -c conda-forge torchcodec=*=*cuda*" - documentation: https://meta-pytorch.org/torchcodec/stable/index.html
 