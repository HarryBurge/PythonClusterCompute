from sim_port import Port

import random

class Node:

    def __init__(self, network, ip):
        
        self.network = network
        self.ip = ip
        self.ports = {}


    def __str__(self):
        line = ""
        for k,d in self.ports.items():
            line += k + "=" + str(d)
        return line


    def run1(self):
        self.ports["22"] = Port(self, "22")

    def run2(self):
        try:
            self.network.connect_ip_port(self, "27", f"192.168.0.{random.randint(0,10)}", "22")
        except ConnectionRefusedError:
            del self.ports["22"]