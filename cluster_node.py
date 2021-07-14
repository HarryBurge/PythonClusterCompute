#~ Imports
from sim_port import Port
import random

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
        self.temp= 1


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
            _, msg= self.decode_message(self.ports['2001'].pop())

            self.ports['2001'].targetip= tarip
            self.ports['2001'].targetport= msg[msg.index(':')+1:]

            self.network.tcp(self.ip, '2001', tarip, '2000', self.encode_message(f'Confirm', 'INT'))
            return True

        # Exit program
        elif (stage==-1):
            for portnum, port in self.ports.items():
                if (port.targetip==tarip or port.targetip==None):
                    del self.ports[portnum]
                    return True
            return False


    def rec_estab_conn(self, selport, msg, stage= 0): # REC

        tarip, tarport= None, None

        try:
            tarip, tarport= msg.split(':')[0], msg.split(':')[1]
        except IndexError:
            pass

        if (stage==0):
            self.ports[selport].targetip= tarip
            self.ports[selport].targetport= tarport
            self.ports[selport].buffer= []
            self.network.tcp(
                self.ip, selport,
                tarip, tarport,
                self.encode_message(f'{self.ip}:{selport}', 'INT')
            )
            self.interupts.append(
                {'type':'REC', 'stage':1, 'counter':TIMEOUT_TIMER, 'args':[selport, msg]}
            )
            return True

        elif (stage==1):
            if (self.ports[selport].buffer!=[]):
                self.interupts.append(
                    {'type':'REC', 'stage':2, 'counter':TIMEOUT_TIMER, 'args':[selport, msg]}
                )
                return True
            return False

        elif (stage==2):
            type, tmsg= self.decode_message(self.ports[selport].read())
            type= type[-3:] # To be deleted, gets rid of other header infomation

            if (type=='INT' and tmsg=='Confirm'):
                self.ports[selport].pop()
                return True
            return False

        # Exit program
        elif (stage==-1):
            self.ports[selport].targetip= None
            self.ports[selport].targetport= None
            self.ports[selport].buffer= []
            return True


    def step(self):
        tar= f'192.168.1.{random.randint(0, 2)}'
        if (self.ip!=tar):
            self.estab_conn(tar)
            self.temp-=1

        for ind, inter in enumerate(self.interupts):

            if (inter['type']=='EST'):

                result= self.estab_conn(*inter['args'], stage= inter['stage'])

                if (inter['counter']==0): 
                    self.estab_conn(*inter['args'], stage= -1)
                    self.interupts[ind]= None
                elif (result):
                    self.interupts[ind]= None
                else: 
                    inter['counter']-= 1

            elif (inter['type']=='REC'):

                result= self.rec_estab_conn(*inter['args'], stage= inter['stage'])

                if (inter['counter']==0): 
                    self.rec_estab_conn(*inter['args'], stage= -1)
                    self.interupts[ind]= None
                elif (result):
                    self.interupts[ind]= None
                else: 
                    inter['counter']-= 1

        for portnum, port in self.ports.items():

            if (port.buffer!=[]):
                type, msg= self.decode_message(port.read())
                type= type[-3:] # To be deleted, gets rid of other header infomation

                if (type=='INT' and msg!='Confirm'):
                    self.interupts.append(
                        {'type':'REC', 'stage': 0, 'counter':1, 'args':[portnum, msg]}
                    )
                    port.pop()


        self.interupts= list(filter(None.__ne__, self.interupts))
        print(self.interupts)
        


