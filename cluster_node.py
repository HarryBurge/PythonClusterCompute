#~ Imports
from sim_port import Port

#~ Constants
TIMEOUT_TIMER= 10000
HEADER_LENGTH= 20

#~ Node
class Node:

    def __init__(self, network, ip):
        
        self.ip= ip
        self.ports= {'2000':Port(2000, network)}
        self.interupts= {}

        self.network= network


    def __str__(self):
        line= f'{self.ip}:['
        for k,d in self.ports.items():
            line+= d.__str__() + ','
        return line+']'


    def encode_message(self, msg, type='GEN'):
        if (type in ['GEN', 'INT']):
            return f'{len(msg)+len(type)+1:{HEADER_LENGTH}}{type};'+msg
        return False


    def decode_message(self, msg):
        return msg[:msg.index(';')], msg[msg.index(';')+1:]


    def estab_conn(self, tarip):
        self.ports['2001']= Port('2001', self.network)
        self.network.tcp(self.ip, '2001', tarip, '2000', self.encode_message(f'{self.ip}:2001', 'INT'))

        for i in range(TIMEOUT_TIMER):
            if (self.ports['2001'].buffer!=[]):
                break
        else:
            return False

        type, msg= self.decode_message(self.ports['2001'].read())
        tarport= msg[msg.index(':')+1:]

        self.ports['2001'].targetip= tarip
        self.ports['2001'].targetport= tarport

        self.network.tcp(self.ip, '2001', tarip, '2000', self.encode_message(f'Confirm', 'INT'))


    def rec_estab_conn(self):
        pass


    def step(self):
        self.estab_conn('192.168.1.0')


