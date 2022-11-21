#  <img src="BATMAN.svg" width="60" height="auto" alt="B.A.T.M.A.N. icon"> Ad-hoc Wi-Fi Mesh Network

## Introduction
Wi-Fi typically operates in one of 2 modes: Infrastructure mode or Ad-hoc mode. 

In infrastructure mode, the edge of the network can be considered a star topology, with the Access Point (AP) as the center of the star, and associated wireless clients at the outer vertices. In this topology, if 2 clients wish to communicate with each other, the traffic is relayed through the AP to the destination in a maximum of 2 hops (provided that they are associated with the same AP). This is very similar to the BLE star topology discussed previously, with the BLE master node being similar to the wireless AP&ast;. For a closed environment, as the central node is aware of all nodes, no routing protocol is needed; nodes simply send their traffic through the AP, who then forwards it to its destination. A significant drawback of this however is that communication range is limited and centered around the AP. 

In ad-hoc mode, each node can communicate directly with any other in-range node, and traffic can be relayed through these nodes (one or more times) to communicate with out-of-range nodes. This is not an out-of-the-box solution though, as a routing protocol is needed to correctly establish a forwarding structure for the overall network. To accomplish this, the [Better Approach to Mobile Ad-hoc Networking (B.A.T.M.A.N.)](http://www.open-mesh.org) protocol was used, which has been included in the official Linux kernel since 2.6.38. Additionally, we use a utility called `batctl` to manage the mesh network.

&ast; - <i>There are other technical discrepancies between the operation of Wi-Fi and BLE, however they will not be discussed in detail here; for our project it is helpful to recognize the similaritie in topology between Bluetooth and Wi-Fi Infrastructure mode.</i>

## Required packages

- Batctl: `sudo apt-get install batctl` 

<i>N.B.</i> - The rc-local service is used to enable the mesh network at boot time. This service is no longer included on Ubuntu 16.10 and later, but there are numerous online guides showing how to manually create it &#40;[example](https://marsown.com/wordpress/how-to-enable-etc-rc-local-with-systemd-on-ubuntu-20-04/)&#41;. Alternatively, you could create your own service instead of using rc-local &#40;[example](https://marsown.com/wordpress/how-to-enable-etc-rc-local-with-systemd-on-ubuntu-20-04/)&#41;. 

## Description

In our mesh topology, we designate one node as an internet gateway, DHCP server, and DNS server for the rest of the network. This internet access could be provided by any secondary network interface on the device; ethernet, addtional wireless radios, etc., but it is not possible to use the same wlan interface that is being used for the mesh network to connect to another SSID with internet access.

Batctl identifies the nodes by their MAC addresses, which can get somewhat confusing to interpret as we create a separate interface for the mesh network that is tied t


## Topology
<img src="WIFI_topology.png" width="600" height="auto"> 
Nodes can communicate directly with all other node(s) within range, indirectly with out of range nodes via node(s) in range

## Instructions

<i>N.B.</i> - Instructions adapted from [binnes](https://github.com/binnes/WiFiMeshRaspberryPi)



### To configure the Gateway node:


### To configure other nodes:


## Known Issues & Workarounds:


___
[Home](/../../) - [BLE Star](../BLE_star) - Wi-Fi Mesh
