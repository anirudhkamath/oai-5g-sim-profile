#!/bin/bash
set -ex
export DISPLAY=:1

sudo killall nr-uesoftmodem nr-softmodem iperf3 oai-watchdog.sh || true

xterm -e bash -c "cd /opt/openairinterface5g/cmake_targets; sudo sudo RFSIMULATOR=<<enter IP of RAN...>> ./ran_build/build/nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3619200000 --rfsim --sa --nokrnmod -O /local/repository/etc/ue.conf -d" &