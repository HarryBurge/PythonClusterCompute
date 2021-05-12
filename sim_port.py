class Port:

    def __init__(self, node, port_num):
        self.node = node
        self.buffer = []
        self.port_num = port_num
        self.target = None

    def __str__(self):
        line=""

        if self.target==None:
            line += "Listening\n"
        else:
            line += f"Connected to {self.target.node.ip}:{self.target.port_num}\n"

        for i in self.buffer:
            line += i + "\n"

        return line

        

    def set_target(self, target):
        self.target = target

    def send_message(self, message):
        self.target.recieve_message(message)

    def recieve_message(self, message):
        self.buffer.append(message)