# LNMesh

## Introduction
In this workshop, we implement a local Lightning Network (LN) cluster of several nodes which may continue to operate and process transactions offline for a period if internet access is lost. 


## System Info
This implementation was done using several Raspberry Pi 4 model B units, system details as follows:
- System - Raspberry Pi OS
- Architecture: 64-bit OS
- Kernel Version: 5.15
- Debian Version: 11 (bullseye)

Two types of local networks were used during testing (click for individual details):
1. [IP-over-Bluetooth Low Energy (BLE) network](BLE_star)        (Star topology, inflexible)
2. [Ad-hoc Wi-Fi mesh network](WIFI_mesh)                         (Mesh topology, flexible)


## Installing LN & establishing channels




___
Home - [BLE Star](BLE_star) - [Wi-Fi Mesh](WIFI_mesh)
