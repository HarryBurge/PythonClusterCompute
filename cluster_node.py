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
    ip: str
    ports: dict
    network: object
    interupts: list

    def __init__(self, network: object, ip: str) -> None:
        
        self.ip= ip
        self.network= network

        self.ports= {LISTEN_PORT:Port(LISTEN_PORT, network)}
        self.interupts= []


    def __str__(self) -> str:
        return f'{self.ip}:{[d.__str__() for k,d in self.ports.items()]}'


    #~ Func
    def encode_message(self, msg: str, type: str = 'GEN') -> str:
        types= ['GEN', 'INT']
        if (type in types):
            return f'{len(msg)+len(type)+1:{HEADER_LENGTH}}{type};'+msg

        raise ValueError(
            f'type={type} passed, however, only {types} options are supported'
        )


    def decode_message(self, msg: str) -> (str, str):
        if (msg.find(';')!=-1):
            return msg[:msg.index(';')], msg[msg.index(';')+1:]
        
        raise ValueError(
            f'msg={msg} passed, doesn\'t contain a \';\' which is required'
        )


    def next_new_port(self) -> str:
        for i in range(int(GEN_PORT_MIN), int(GEN_PORT_MAX)+1):
            if (str(i) not in self.ports): return str(i)
        
        raise IndexError(
            f'Port limit exceded, no new ports can be created'
        )


    def estab_conn( # EST
        self, tarip: str, tarport: str, selport: str, stage: int = 0
    ) -> bool:

        # Create port to connect to target ip and port
        # and send message pointing back to our ip and port
        if (stage==0):
            self.ports[selport]= Port(selport, self.network)
            self.network.tcp(
                self.ip, selport, tarip, tarport, 
                self.encode_message(f'{self.ip}:{selport}', 'INT')
            )

            self.interupts.append({
                'type':'EST', 'stage':1, 'counter':TIMEOUT_TIMER, 
                'args':[tarip, tarport, selport]
            })

            return True

        # Wait until target has locked in port
        # then messaged back its ip and port
        elif (stage==1):
            if (self.ports[selport].is_empty()): return False

            _, msg= self.decode_message(self.ports[selport].pop())

            self.ports[selport].targetip= tarip
            self.ports[selport].targetport= msg[msg.index(':')+1:]

            self.network.tcp(
                self.ip, selport, tarip, tarport, 
                self.encode_message(f'Confirm', 'INT')
            )

            return True

        # Exit stratergy
        elif (stage==-1):
            for portnum, port in self.ports.items():
                if ( 
                    (port.targetip==tarip or port.targetip==None) \
                    and portnum!=tarport
                ):
                    del self.ports[portnum]
                    return True

            return False


    def rec_estab_conn( # REC
        self, selport: str, msg: str, stage: int= 0
    ) -> bool:

        # Reserve port and set its target to the port passed, then
        # send message back
        if (stage==0):
            tarip, tarport= None, None
            if (msg.find(':')!=-1):
                tarip, tarport= msg.split(':')[0], msg.split(':')[1]

            self.ports[selport].targetip= tarip
            self.ports[selport].targetport= tarport
            self.ports[selport].buffer= []

            self.network.tcp(
                self.ip, selport, tarip, tarport,
                self.encode_message(f'{self.ip}:{selport}', 'INT')
            )

            self.interupts.append({
                'type':'REC', 'stage':1, 'counter':TIMEOUT_TIMER, 
                'args':[selport, msg]
            })

            return True

        # Wait for comfimation message
        elif (stage==1):
            if (not self.ports[selport].is_empty()):
                type, tmsg= self.decode_message(self.ports[selport].read())
                type= type[-3:] # TODO: Delete

                if (type=='INT' and tmsg=='Confirm'):
                    self.ports[selport].pop()
                    return True

            return False

        # Exit stratergy
        elif (stage==-1):
            self.ports[selport].targetip= None
            self.ports[selport].targetport= None
            self.ports[selport].buffer= []
            
            return True
    
    
    def new_port_switch( # NWP
        self
    ):
        pass


    def send_message(self, ip: str, msg: str, type: str) -> bool:
        for portnum, port in self.ports.items():
            if (
                port.targetip==ip and 
                self.network.tcp(
                    self.ip, portnum, port.targetport, port.targetport,
                    self.encode_message(msg, type)
                )
            ):
                return True

        return False
    #~


    #~ Control
    def handle_interupts(self) -> None:
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
                result= self.rec_estab_conn(
                    *inter['args'], stage= inter['stage']
                )

                if (inter['counter']==0): 
                    self.rec_estab_conn(*inter['args'], stage= -1)
                    self.interupts[ind]= None
                elif (result):
                    self.interupts[ind]= None
                else: 
                    inter['counter']-= 1

        self.interupts= list(filter(None.__ne__, self.interupts))


    def handle_incoming_messages(self) -> None:
        for portnum, port in self.ports.items():

            if (not port.is_empty()):
                type, msg= self.decode_message(port.read())
                type= type[-3:] # TODO: Delete

                if (type=='INT' and msg!='Confirm'):
                    self.interupts.append(
                        {'type':'REC', 'stage': 0, 'counter':1, 'args':[portnum, msg]}
                    )
                    port.pop()
    #~

    def step(self) -> None:

        try:
            newPort= self.next_new_port()

            if (newPort and INTIAL_PORT not in self.ports):
                tar= f'192.168.1.{random.randint(0, len(self.network.nodes)-1)}'
                if (self.ip!=tar):
                    self.estab_conn(tar, LISTEN_PORT, INTIAL_PORT)

            elif (newPort and INTIAL_PORT in self.ports):
                self.send_message(self.ports[INTIAL_PORT].targetip, f'[{self.ip}]:[{newPort}]', 'NWP')
                    
                


        except IndexError:
            # No general ports avaliable
            pass
        
        self.handle_interupts()
        print(self.interupts)
        self.handle_incoming_messages()
        


