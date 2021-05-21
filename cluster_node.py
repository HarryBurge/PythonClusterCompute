from sim_port import Port

import random

class Node:

    def __init__(self, network, ip):
        
        self.network = network
        self.ip = ip
        self.ports = {"20000" : Port(self, 20000)}


    def __str__(self):
        line = ""
        for k,d in self.ports.items():
            line += k + "=" + str(d)
        return line


    def connect_to_node(self, tarip):
        timeoutdelay = 10000

        # Initilise first connection
        for i in range(timeoutdelay):
            self.ports["20001"] = Port(self, 20001)

            try:
                self.network.connect_ip_port(self.ip, "20001", tarip, "20000")
                print("connected")
                break

            except ConnectionRefusedError:
                self.ports.pop("20001")
        
        else:
            return False

        return True


    def run(self):
        
        while True:
            temp= int(self.ip.split(".")[-1])
            target = [i for i in range(10)][:temp] + [i for i in range(10)][temp+1:]
            if self.connect_to_node(f"192.168.0.{random.choice(target)}") != False:
                return