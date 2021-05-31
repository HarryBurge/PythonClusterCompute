from sim_port import Port

import random
import time

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


    def connect_recv_check(self): 
        for k,d in self.ports.items():
            temp= d.read_buffer()

            if temp != False:
                tarip= temp.split(":")[0].replace("[","").replace("]","")
                tarport= temp.split(":")[1].replace("[","").replace("]","")

                # Pick our port we want perminant connection on
                myport= None

                for i in range(2, 51):
                    if str(20000+i) not in self.ports.keys():
                        myport= str(20000+i)
                        self.ports[myport] = Port(self, myport)
                        break

                if myport != None:
                    timeoutdelay = 10000

                    # Initilise first connection
                    for i in range(timeoutdelay):
                        self.ports[myport] = Port(self, myport)

                        try:
                            self.network.connect_ip_port(self.ip, str(myport), tarip, tarport)
                            break

                        except ConnectionRefusedError:
                            self.ports.pop(str(myport))
                    
                    else:
                        return False


                    self.send_message_to_node([tarip], f"[{self.ip}]:[{myport}]")

                    # Reopen starter ports
                    self.ports["20000"].target= None


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
            if str(20000+i) not in self.ports.keys():
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
                break

        else:
            return False

        # Reopen starter ports
        self.ports["20000"].target= None
        self.ports.pop("20001")
        
        return True

    
    def send_message_to_node(self, tarips, msg):

        for ip in tarips:
            for pnum, port in self.ports.items():

                if port.target != None and port.target.node.ip==ip:
                    port.send_message(msg)



    def run(self):

        connected= False

        while True:

            time.sleep(0.2)

            if not connected:
                temp= int(self.ip.split(".")[-1])
                target = [i for i in range(10)][:temp] + [i for i in range(10)][temp+1:]
                if self.connect_to_node(f"192.168.0.{random.choice(target)}") != False:
                    connected= True

            self.connect_recv_check()


            