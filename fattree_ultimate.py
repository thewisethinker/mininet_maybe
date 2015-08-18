# By Nabajyoti Medhi, the SDN architect

# The following code will generate fat tree topology with any radix value
# Change the values of variables given to get your desired fat tree
# Refer to this paper for the architecture:  http://ccr.sigcomm.org/online/files/p63-alfares.pdf

#k-ary (radix) fattree:three layer topology (edge,aggregation,core)
#k pods,each consists of (k/2)^2 hosts and 
#two layers (edge/aggregate) each with k/2 k-port switches
#Each edge switch connects to k/2 hosts and k/2 aggregate switches 
#Each aggregate switch connects to k/2 edge and k/2 core switches 
#(k/2)^2 core switches: each connects to k pods supports k3/4 hosts!

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
#from mininet.link import TCLinK, Intf

class MyTopo(Topo):

    def __init__(self, enable_all = True):

        #core_switch_number = 4; #number of core switches
        #pod_number = 4;         #optional, number of pods, same as radix, so in many places we take radix only
        #agg_switch_number = 8;  #optional
        #edge_switch_number = 8; #optional
        #host_per_edge = 2;
        
	radix = 8;              #number of ports per switch

	#h1 = 10 #(Mbps) a host to access switch link capacity, remember in mininet 2.0.0 you can't
	       # exceed 1Gbps link capacity
	#h2 = (radix/2)*h1;
	#h3 = ((radix/2)**2)*h1;
	#link capacities for a non-blocking connection, specify according to the formula on the right for a non-blocking connection
	corelink = dict(cls=TCLink, bw=160) #(radix/2)^2 * H Mbps core switch to agg switch link
 	swlink = dict(cls=TCLink, bw=40) #(radix/2)*H Mbps edge switch to agg switch links
 	hostlink = dict(cls=TCLink, bw=10) #H Mbps for server links

	#net = Mininet(topo = None, build = False, ipBase = '10.0.0.0/8')

	#c0 = net.addController(name='Cena')

        Topo.__init__(self)

        coreswitches = []
        aggswitches = [] #aggregation switches
        edgeswitches = []
        #pods = [] 
        #pods_agg = []
        #pods_edge = [] 
        pods = [[] for i in range(radix)]        #2D list to store switches in the pod
        pods_agg = [[] for i in range(radix)]
        pods_edge = [[] for i in range(radix)]
        #pods.append([])
        #pods.append([])
        #pods_agg.append([])
        #pods_agg.append([])
        #pods_edge.append([])
        #pods_edge.append([])
	#net.build()
        #Declare core switches
	k1 = 0;
        for x in range(0, (radix/2)**2):
	    k1 = x + 1
            coreswitches.append(self.addSwitch("s" + str(k1), cls=OVSKernelSwitch))
        for x in range(0, radix):
            pods.append(x)
            pods_agg.append(x)
	k2 = 0;
	for x in range(0, radix):
	    for y in range(0, radix/2): 
		AS = self.addSwitch("s" + str(2) + str(x + 1) + str(y + 1), cls=OVSKernelSwitch)          #as-pod_id-edge_switch_id
		pods_agg[x].append(AS)
		ES = self.addSwitch("s" + str(3) + str(x + 1) + str(y + 1), cls=OVSKernelSwitch)
		pods_edge[x].append(ES)
		for z in range(0, radix/2):
		    self.addLink(ES, self.addHost("h" + str(x + 1) + str(y + 1) + str(z + 1)), **hostlink)   # h-----pod_id-edge_switch_id-host_id

	#connection between core switches and aggregation switches
	for x in range(0, len(coreswitches)/2):
	    for y in range(0, radix):
		for z in range(0, radix/4):
		    self.addLink(pods_agg[y][z], coreswitches[x], **corelink)
	for x in range(len(coreswitches)/2, len(coreswitches)):
	    for y in range(0, radix):
		for z in range(radix/4, radix/2):
		    self.addLink(pods_agg[y][z], coreswitches[x], **corelink)

	#connection between aggregation and edge switches
	for x in range(0, radix):
	    for y in range(0, radix/2):
		for z in range(0, radix/2):
		    self.addLink(pods_agg[x][y], pods_edge[x][z], **swlink)

	#net.stop()

topos = {'mytopo': (lambda: MyTopo())}
