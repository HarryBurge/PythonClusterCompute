#~ Imports
from sim_port import Port
import random

#~ Constants
TIMEOUT_TIMER= 10
HEADER_LENGTH= 20

LISTEN_PORT= '2000'
INTIAL_PORT= '2001'
GEN_PORT_MIN= '2002'
GEN_PORT_MAX= '2005'

#~ Node
class Node:
    '''
    Holds a simulation of a node on a network
    - Uses a semi event driven model (May be changed to follow exactly and use closures to activate)
    - Interupts:
        - Have 3 letter types which indicate which function (Shown by function)
        - Stage of function (-1 to clear action)
        - Timer countdown (-1 called when reaches 0)
        - Args are things to be passed to function
    '''

    def __init__(self, network, ip):
        
        self.ip= ip
        self.ports= {LISTEN_PORT:Port(LISTEN_PORT, network)}
        self.network= network

        # [{<type>, <stage>, <counter>, <args>}]
        self.interupts= []


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


    def next_new_port(self):
        for i in range(GEN_PORT_MIN, GEN_PORT_MAX+1):
            if (str(i) not in self.ports): return str(i)
        return False


    def estab_conn(self, tarip, stage= 0): # EST

        if (stage==0):
            self.ports[INTIAL_PORT]= Port(INTIAL_PORT, self.network)
            self.network.tcp(
                self.ip, INTIAL_PORT, 
                tarip, LISTEN_PORT, 
                self.encode_message(f'{self.ip}:{INTIAL_PORT}', 'INT')
            )
            self.interupts.append(
                {'type':'EST', 'stage':1, 'counter':TIMEOUT_TIMER, 'args':[tarip]}
            )
            return True

        elif (stage==1):
            if (self.ports[INTIAL_PORT].buffer==[]): return False
            self.interupts.append(
                {'type':'EST', 'stage':2, 'counter':1, 'args':[tarip]}
            )
            return True

        elif (stage==2):
            _, msg= self.decode_message(self.ports[INTIAL_PORT].pop())

            self.ports[INTIAL_PORT].targetip= tarip
            self.ports[INTIAL_PORT].targetport= msg[msg.index(':')+1:]

            self.network.tcp(self.ip, INTIAL_PORT, tarip, LISTEN_PORT, self.encode_message(f'Confirm', 'INT'))
            return True

        # Exit program
        elif (stage==-1):
            for portnum, port in self.ports.items():
                if ( (port.targetip==tarip or port.targetip==None) and portnum!=LISTEN_PORT ):
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
            type= type[-3:] # TODO: Delete

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

        if (INTIAL_PORT not in self.ports):
            tar= f'192.168.1.{random.randint(0, len(self.network.nodes)-1)}'
            if (self.ip!=tar):
                self.estab_conn(tar)


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
                type= type[-3:] # TODO: Delete

                if (type=='INT' and msg!='Confirm'):
                    self.interupts.append(
                        {'type':'REC', 'stage': 0, 'counter':1, 'args':[portnum, msg]}
                    )
                    port.pop()

                elif (type=='NWP'):
                    pass


        self.interupts= list(filter(None.__ne__, self.interupts))
        print(self.interupts)
        


