from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel,info
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import CPULimitedHost
import time
import os

if '_main'==name_:
	net = Mininet(link=TCLink)
	#add host
	ha= net.addHost('ha')
	hb= net.addHost('hb')
	#add router
	r1= net.addHost('r1')
	r2= net.addHost('r2')
	r3= net.addHost('r3')
	r4= net.addHost('r4')

	bandwith1={'bw':1}
	bandwith2={'bw':0.5}

	#add link host ke router
	net.addLink(ha, r1, cls=TCLink, **bandwith1)
	net.addLink(ha, r2, cls=TCLink, **bandwith1)
	net.addLink(hb, r3, cls=TCLink, **bandwith1)
	net.addLink(hb, r4, cls=TCLink, **bandwith1)

	#add link router ke router

	net.addLink(r1, r3, cls=TCLink, **bandwith2)
	net.addLink(r1, r4, cls=TCLink, **bandwith1)
	net.addLink(r2, r3, cls=TCLink, **bandwith1)
	net.addLink(r2, r4, cls=TCLink, **bandwith2)

	net.build()

	#interface

	ha.cmd("ifconfig ha-eth0 0")
	ha.cmd("ifconfig ha-eth1 0")

	hb.cmd("ifconfig hb-eth0 0")
	hb.cmd("ifconfig hb-eth1 0")

	r1.cmd("ifconfig r1-eth0 0")
	r1.cmd("ifconfig r1-eth1 0")
	r1.cmd("ifconfig r1-eth2 0")
	
	r2.cmd("ifconfig r2-eth0 0")
	r2.cmd("ifconfig r2-eth1 0")
	r2.cmd("ifconfig r2-eth2 0")
	
	r3.cmd("ifconfig r3-eth0 0")
	r3.cmd("ifconfig r3-eth1 0")
	r3.cmd("ifconfig r3-eth2 0")
	
	r4.cmd("ifconfig r4-eth0 0")
	r4.cmd("ifconfig r4-eth1 0")
	r4.cmd("ifconfig r4-eth2 0")

	

	ha.cmd("ifconfig ha-eth0 192.168.0.2 netmask 255.255.255.0")
	ha.cmd("ifconfig ha-eth1 192.168.1.2 netmask 255.255.255.0")

	hb.cmd("ifconfig hb-eth0 192.168.2.2 netmask 255.255.255.0")
	hb.cmd("ifconfig hb-eth1 192.168.3.2 netmask 255.255.255.0")

	r1.cmd("ifconfig r1-eth0 192.168.0.1 netmask 255.255.255.0") 
	r1.cmd("ifconfig r1-eth1 192.168.100.1 netmask 255.255.255.252")
	r1.cmd("ifconfig r1-eth2 192.168.100.5 netmask 255.255.255.252")
	
	r2.cmd("ifconfig r2-eth0 192.168.1.1 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth1 192.168.100.9 netmask 255.255.255.252")
	r2.cmd("ifconfig r2-eth2 192.168.100.13 netmask 255.255.255.252") 

	r3.cmd("ifconfig r3-eth0 192.168.2.1 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth1 192.168.100.2 netmask 255.255.255.252")
	r3.cmd("ifconfig r3-eth2 192.168.100.10 netmask 255.255.255.252")

	r4.cmd("ifconfig r4-eth0 192.168.3.1 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth1 192.168.100.6 netmask 255.255.255.252")
	r4.cmd("ifconfig r4-eth2 192.168.100.14 netmask 255.255.255.252") 
	#config router
	r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r3.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r4.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	
	#clo2
	#Routing antar host
	#Ha
	ha.cmd('ip rule add from 192.168.0.2 table 1')
	ha.cmd('ip rule add from 192.168.1.2 table 2')
	ha.cmd('ip route add 192.168.0.0/24 dev ha-eth0 scope link table 1')
	ha.cmd('ip route add default via 192.168.0.1 dev ha-eth0 table 1')
	ha.cmd('ip route add 192.168.1.0/24 dev ha-eth1 scope link table 2')
	ha.cmd('ip route add default via 192.168.1.1 dev ha-eth1 table 2')
	ha.cmd('ip route add default scope global nexthop via 192.168.0.1 dev ha-eth0')
	#Hb
	hb.cmd('ip rule add from 192.168.2.2 table 1')
	hb.cmd('ip rule add from 192.168.3.2 table 2')
	hb.cmd('ip route add 192.168.2.0/24 dev hb-eth0 scope link table 1')
	hb.cmd('ip route add default via 192.168.2.1 dev hb-eth0 table 1')
	hb.cmd('ip route add 192.168.3.0/24 dev hb-eth1 scope link table 2')
	hb.cmd('ip route add default via 192.168.3.1 dev hb-eth1 table 2')
	hb.cmd('ip route add default scope global nexthop via 192.168.2.1 dev hb-eth0')

	#Routing antar router
	#R1
	r1.cmd("route add -net 192.168.1.0/24 gw 192.168.100.6")
	r1.cmd("route add -net 192.168.100.8/30 gw 192.168.100.2")
	r1.cmd("route add -net 192.168.100.12/30 gw 192.168.100.6")
	r1.cmd("route add -net 192.168.2.0/24 gw 192.168.100.2")
	r1.cmd("route add -net 192.168.3.0/24 gw 192.168.100.6")

	#R2
	r2.cmd("route add -net 192.168.0.0/24 gw 192.168.100.10")
	r2.cmd("route add -net 192.168.100.0/30 gw 192.168.100.10")
	r2.cmd("route add -net 192.168.2.0/24 gw 192.168.100.10")
	r2.cmd("route add -net 192.168.3.0/24 gw 192.168.100.14")
	r2.cmd("route add -net 192.168.100.4/30 gw 192.168.100.14")

	#R3
	r3.cmd("route add -net 192.168.0.0/24 gw 192.168.100.1")
	r3.cmd("route add -net 192.168.1.0/24 gw 192.168.100.9")
	r3.cmd("route add -net 192.168.3.0/24 gw 192.168.100.9")
	r3.cmd("route add -net 192.168.100.4/30 gw 192.168.100.1")
	r3.cmd("route add -net 192.168.100.12/30 gw 192.168.100.9")
	
	#R4
	r4.cmd("route add -net 192.168.1.0/24 gw 192.168.100.13")
	r4.cmd("route add -net 192.168.0.0/24 gw 192.168.100.5")
	r4.cmd("route add -net 192.168.100.0/30 gw 192.168.100.5")
	r4.cmd("route add -net 192.168.100.8/30 gw 192.168.100.13")
	r4.cmd("route add -net 192.168.2.0/24 gw 192.168.100.5")
	
	CLI(net)
	net.stop()