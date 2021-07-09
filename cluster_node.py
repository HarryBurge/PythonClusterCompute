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

        # [{<type>, <stage>, <counter>, <args>}]
        self.interupts= []

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


    def estab_conn(self, tarip, stage= 0): # EST

        if (stage==0):
            self.ports['2001']= Port('2001', self.network)
            self.network.tcp(
                self.ip, '2001', 
                tarip, '2000', 
                self.encode_message(f'{self.ip}:2001', 'INT')
            )
            self.interupts.append(
                {'type':'EST', 'stage':1, 'counter':TIMEOUT_TIMER, 'args':[tarip]}
            )
            return True

        elif (stage==1):
            if (self.ports['2001'].buffer==[]): return False
            self.interupts.append(
                {'type':'EST', 'stage':2, 'counter':1, 'args':[tarip]}
            )
            return True

        elif (stage==2):
            _, msg= self.decode_message(self.ports['2001'].read())

            self.ports['2001'].targetip= tarip
            self.ports['2001'].targetport= msg[msg.index(':')+1:]

            self.network.tcp(self.ip, '2001', tarip, '2000', self.encode_message(f'Confirm', 'INT'))
            return True


    def rec_estab_conn(self, selport, msg, stage= 0): # REC

        tarip, tarport= msg.split(':')[0], msg.split(':')[1]

        if (stage==0):
            self.ports[selport].targetip= tarip
            self.ports[selport].targetport= tarport
            self.network.tcp(
                self.ip, selport,
                tarip, tarport,
                self.encode_message(f'{self.ip}:{selport}', 'INT')
            )
            return True

        elif (stage==1):
            if (self.ports[selport].buffer!=[]): return True
            return False

        elif (stage==2):
            if (msg=='Confirm'): return True
            return False


    def step(self):
        self.estab_conn('192.168.1.0')

        #TODO: keep building out control logid

        for ind, inter in enumerate(self.interupts):

            if (inter['type']=='EST'):

                result= self.estab_conn(*inter['args'], stage= inter['stage'])

                if (result or inter['counter']==0): self.interupts[ind]= None 
                else: inter['counter']-=1

        self.interupts.remove(None)
        


