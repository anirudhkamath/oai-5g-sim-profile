set -ex
export DISPLAY=:1

sudo killall nr-uesoftmodem nr-softmodem iperf3 oai-watchdog.sh || true

# Build OAI 5G RAN (USRP radio head.)
sudo chown -R $USER:$GROUP /opt/openairinterface5g/
cd /opt/openairinterface5g/
source oaienv
cd cmake_targets
./build_oai -c -C -I --ninja
./build_oai -c -C --gNB -w USRP --build-lib all --ninja

sudo bash -c "touch ~/gnb_logs"  # expect an experiment ID passed as an argument to the sh script.
# xterm -e bash -c "cd /opt/openairinterface5g/cmake_targets; sudo ./ran_build/build/nr-softmodem --sa -O /local/repository/etc/gnb.conf -d  > ~/gnb_logs 2>&1 &" &