#!/bin/bash
sudo sysctl -w net.core.wmem_max=33554432
sudo sysctl -w net.core.rmem_max=33554432

SDR_IFACE=$(ifconfig | grep -B1 192.168.30 | grep -o "^\w*")
sudo ifconfig $SDR_IFACE mtu 9000
