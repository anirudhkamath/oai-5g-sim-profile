set -ex
COMMIT_HASH=$1
BINDIR=`dirname $0`
ETCDIR=/local/repository/etc
source $BINDIR/common.sh

sudo apt-get update && sudo apt-get install -y \
  cmake \
  make \
  gcc \
  g++ \
  pkg-config \
  libfftw3-dev \
  libmbedtls-dev \
  libsctp-dev \
  libyaml-cpp-dev \
  libgtest-dev

cd $SRCDIR
git clone $SRS_PROJECT_REPO
cd srsRAN_Project
git checkout $COMMIT_HASH
git apply $ETCDIR/srsran.patch
mkdir build
cd build
cmake ../
make -j $(nproc)
