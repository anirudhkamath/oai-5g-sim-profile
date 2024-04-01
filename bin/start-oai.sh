set -ex
export DISPLAY=:1

sudo killall nr-uesoftmodem nr-softmodem iperf3 oai-watchdog.sh || true

xterm -e bash -c "cd /opt/openairinterface5g/cmake_targets; sudo RFSIMULATOR=server ./ran_build/build/nr-softmodem --rfsim --sa -O /local/repository/etc/gnb.conf -d" &