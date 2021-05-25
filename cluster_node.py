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
                break

            except ConnectionRefusedError:
                self.ports.pop("20001")
        
        else:
            return False

        # Pick our port we want perminant connection on
        myport= None

        for i in range(2, 51):
            if str(20000+i) in self.ports:
                myport= str(20000+i)
                self.ports[myport] = Port(self, myport)
                break

        # Send where we are listening
        if myport!= None:
            self.send_message_to_node([tarip], f"[{self.ip}]:[{myport}]")
        else:
            return False

        # Listen on port until confimation
        for i in range(timeoutdelay):

            temp= self.ports[myport].read_buffer()

            if temp != False and temp.split(":")[0]==f"[{tarip}]":
                # Reopen starter ports
                self.ports["20000"].target= None
                self.ports.pop("20001")
                break

        else:
            return False

        return True

    
    def send_message_to_node(self, tarips, msg):

        for ip in tarips:
            for pnum, port in self.ports.items():

                if port.target.ip==ip:
                    port.send_message(msg)



    def run(self):
        
        # while True:
        temp= int(self.ip.split(".")[-1])
        target = [i for i in range(10)][:temp] + [i for i in range(10)][temp+1:]
        if self.connect_to_node(f"192.168.0.{random.choice(target)}") != False:
            return