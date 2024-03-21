#!/bin/bash
set -ex
export DISPLAY=:1

sudo killall nr-uesoftmodem nr-softmodem iperf3 || true
