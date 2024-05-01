set -ex
UHD_VERSION=$1
BINDIR=`dirname $0`
source $BINDIR/common.sh

# install deps
sudo apt-get update && sudo apt-get install -y \
  autoconf \
  automake \
  build-essential \
  ccache \
  cmake \
  cpufrequtils \
  doxygen \
  ethtool \
  g++ \
  git \
  inetutils-tools \
  libboost-all-dev \
  libncurses5 \
  libncurses5-dev \
  libusb-1.0-0 \
  libusb-1.0-0-dev \
  libusb-dev \
  python3-dev \
  python3-mako \
  python3-numpy \
  python3-requests \
  python3-scipy \
  python3-setuptools \
  python3-ruamel.yaml

cd $SRCDIR
git clone $UHD_REPO uhd
cd uhd/host
git checkout $UHD_VERSION
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr ../
make -j$(nproc)
sudo make install
sudo ldconfig
sudo uhd_images_downloader
