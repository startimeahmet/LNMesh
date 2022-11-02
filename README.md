# LNMesh

## Introduction
In this workshop, we implement a local Lightning Network (LN) cluster of several nodes which may continue to operate and process transactions offline for a period if internet access is lost. 

This implementation was done using several Raspberry Pi 4 model B units, system details as follows:
- System - Raspberry Pi OS
- Architecture: 64-bit OS
- Kernel Version: 5.15
- Debian Version: 11 (bullseye)

Two types of local networks were used during testing (click for individual details):
1. [IP-over-Bluetooth Low Energy (BLE) network](BLE_star)        (Star topology, inflexible)
2. [Ad-hoc Wi-Fi mesh network](WIFI_mesh)                         (Mesh topology, flexible)


## IP-over-BLE Setup

### Introduction
IP-over-BLE was tested as a Proof-of-Concept (PoC), and has several limitations compared to Wi-Fi mesh, including Inflexibility of topology, Shorter range, and Lower bandwidth/data rate, with the only noteworthy advantage being that BLE is much more energy efficient compared to Wi-Fi. Nevertheless, it could be handy for facilitating short-range, peer-to-peer transactions if a strong use case were identified.

IP-over-BLE has no officially recognized network standard, however this feature can be easily implemented by leveraging [BlueZ](https://github.com/bluez/bluez), which is the bluetooth stack implemented in Linux. Linux kernels 3.4 and later include Bluez 5.0 or later, and in particular version `5.55-3.1+rpt1` was used for our testing.
To simplify BlueZ implementation of IP-over-BLE, we additionally used the [bluez-tools](https://github.com/khvzak/bluez-tools) package (tested with version `2.0-20170911.0.7cb788c-4`) which easily implements bluetooth network access.

### Required packages
- Bluez:        `$ sudo apt-get install bluez`
- Bluez-tools:  `$ sudo apt-get install bluez-tools`


### Description
Bluetooth uses Time-Division Multiple Access (TDMA) for channel access, as opposed to Wi-Fi which uses CSMA. This means that in a bluetooth network, one node is designated as the master, and this node polls the other (slave) nodes for communications to occur. This is the reason for the inflexible topology, which is essentially a star with the master node in the center.

Additionally, for IP-over-BLE, the master node acts as a DHCP server to issue IP addresses to connecting bluetooth peers.


### Topology
![BLE Topology](BLE_topology.png)


### Instructions
It is *strongly* recommended to set the bluetooth hostname on each device before attempting to configure anything. Otherwise you will end up with several bluetooth devices all named __raspberrypi__ and no idea which is which when trying to discover & peer.
To set the bluetooth hostname, create the `/etc/machine-info` file with the following content, replacing <device-name> with your desired bluetooth name:
```
PRETTY_HOSTNAME=<device-name>
```


#### To configure the Master node:
1. Create the bridge interface file (ex. pan0) at `/etc/systemd/network/pan0.netdev` with the following content:
```
[NetDev]
Name=pan0
Kind=bridge
```

2. Create the network settings file at `/etc/systemd/network/pan0.network` with the following content:
```
[Match]
Name=pan0

[Network]
Address=172.30.1.1/24
DHCPServer=yes
```
__N.B.__ - If connected devices should not use the BLE channel to accessing external network, add the `EmitRouter=no` line in the above file.

3. Register the bluetooth agent service by creating the following file at `/etc/systemd/system/bt-agent.service`:
```
[Unit]
Description=Bluetooth Auth Agent

[Service]
ExecStart=/usr/bin/bt-agent -c NoInputNoOutput
Type=simple

[Install]
WantedBy=multi-user.target
```

4. Register the bluetooth network access service by creating the following file at `/etc/systemd/system/bt-network.service`:
```
[Unit]
Description=Bluetooth NAP PAN
After=pan0.network

[Service]
ExecStart=/usr/bin/bt-network -s nap pan0
Type=simple

[Install]
WantedBy=multi-user.target
```

5. Enable & start the required services:
```
$ sudo systemctl enable --now systemd-networkd
$ sudo systemctl enable --now bt-agent
$ sudo systemctl enable --now bt-network
```


#### To configure Slave nodes:
No configuration is required; simply enable bluetooth, discover & peer with the master, and run the following command:
`bt-network -c <bluetooth name or address of Master> nap`

___
[Home](../blob/main)
