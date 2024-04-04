#!/bin/bash
set -ex
export DISPLAY=:1

sudo killall nr-uesoftmodem nr-softmodem iperf3 oai-watchdog.sh || true

sudo bash -c "touch ~/ue_logs"
# Build OAI 5G RAN (USRP radio head.)
sudo chown -R $USER:$GROUP /opt/openairinterface5g/
cd /opt/openairinterface5g/
source oaienv
cd cmake_targets
./build_oai -c -C -I --ninja
./build_oai -c -C --nrUE -w USRP --build-lib all --ninja

# xterm -e bash -c "cd /opt/openairinterface5g/cmake_targets; sudo ./ran_build/build/nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3619200000 --sa --nokrnmod -O /local/repository/etc/ue.conf -d > ~/ue_logs 2>&1 " &

# how to introduce AWGN noise??