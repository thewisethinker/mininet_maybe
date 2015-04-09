# By Nabajyoti Medhi, the SDN architect

# The following code will generate fat tree topology with any radix value
# Change the values of variables given to get your desired fat tree
# Refer to this paper for the architecture:  http://ccr.sigcomm.org/online/files/p63-alfares.pdf


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

        core_switch_number = 4; #number of core switches
        pod_number = 4;         #number of pods, same as radix, so in many places we take pod_number only
        agg_switch_number = 8;  #optional
        edge_switch_number = 8; #optional
        host_per_edge = 2;
        radix = 4;              #number of ports per switch

	#net = Mininet(topo = None, build = False, ipBase = '10.0.0.0/8')

	#c0 = net.addController(name='Cena')

        Topo.__init__(self)

        coreswitches = []
        aggswitches = [] #aggregation switches
        edgeswitches = []
        #pods = [] 
        #pods_agg = []
        #pods_edge = [] 
        pods = [[] for i in range(pod_number)]        #2D list to store switches in the pod
        pods_agg = [[] for i in range(pod_number)]
        pods_edge = [[] for i in range(pod_number)]
        #pods.append([])
        #pods.append([])
        #pods_agg.append([])
        #pods_agg.append([])
        #pods_edge.append([])
        #pods_edge.append([])
	#net.build()
        #Declare core switches
        for x in range(0, core_switch_number):
            coreswitches.append(self.addSwitch("cs" + str(x + 1), cls=OVSKernelSwitch))
	    #net.get("cs" + str(x + 1)).start([Cena])
        for x in range(0, pod_number):
            pods.append(x)
            pods_agg.append(x)

	for x in range(0, pod_number):
	    for y in range(0, radix/2):
		AS = self.addSwitch("as" + str(x + 1) + str(y + 1), cls=OVSKernelSwitch)          #as-pod_id-edge_switch_id
		pods_agg[x].append(AS)
		ES = self.addSwitch("es" + str(x + 1) + str(y + 1), cls=OVSKernelSwitch)
		pods_edge[x].append(ES)
		for z in range(0, radix/2):
		    self.addLink(ES, self.addHost("h-" + str(x + 1) + str(y + 1) + str(z + 1)))   # h-pod_id-edge_switch_id-host_id

	#connection between core switches and aggregation switches
	for x in range(0, len(coreswitches)/2):
	    for y in range(0, radix/4):
		self.addLink(pods_agg[x][y], coreswitches[x])
	for x in range(len(coreswitches)/2, len(coreswitches)):
	    for y in range(radix/4, radix/2):
		self.addLink(pods_agg[x][y], coreswitches[x])

	#connection between aggregation and edge switches
	for x in range(0, pod_number):
	    for y in range(0, radix/2):
		for z in range(0, radix/2):
		    self.addLink(pods_agg[x][y], pods_edge[x][z])

	#net.stop()

topos = {'mytopo': (lambda: MyTopo())}
