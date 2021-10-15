#~ Imports
import numpy as np

from Node import compute_manager, network_manager, reporting_manager

#~ Consts

#~ Node
class Node:

    network_m: network_manager.NetworkManager
    compute_m: compute_manager.ComputeManager
    reporting_m: reporting_manager.ReportingManager
    interupts: list # 2D List, first axis being priority in desending order

    def __init__(self, ip: str, dns: object) -> None:
        self.network_m= network_manager.NetworkManager(ip, dns)
        self.compute_m= compute_manager.ComputeManager()
        self.reporting_m= reporting_manager.ReportingManager()
        self.interupts= [[]]*5




def run(nodes, ind, dns) -> None:

    # Repeat until making valid connection
    self= nodes.get(ind)
    while True:
        temp= f'192.168.1.{np.random.randint(0,29)}'
        self.network_m.connect_to_node(temp, dns)

        if self.network_m.is_connected_to(temp):
            break
    nodes.set(ind, self)

    # Control loop
    while True:
        self= nodes.get(ind)
        self.network_m.message_handler(dns)
        self.network_m.info_to_connected_nodes()
        nodes.set(ind, self)