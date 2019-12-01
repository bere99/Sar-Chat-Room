#!/usr/bin/env python3

from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet import reactor

MAX_USERS = 100
MAX_MSG_LENGTH = 255
MAX_USER_LENGTH = 16
PORT = 8000

ER_COM_NOT_FOUND=-0
ER_MAX_USERS=-1
ER_FORBID_CHARS=-2
ER_LONG_NME=-3
ER_REP_NME=-4
ER_LONG_MSG=-5
ER_OTHER=-7

class ChatProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = None

    def connectionMade(self):
        if len(self.factory.users)==MAX_USERS:
        	self.sendLine(ER_MAX_USERS.encode())
        	#Cerrar conexion tcp
        mensaje="FTR0 0 0 0"
        self.sendline(mensaje.encode())
        mensaje="USR"+" ".join(self.factory.users)
        self.sendLine(users.encode())

        	

    def connectionLost(self, reason):
        for name in self.factory.users:
            if users[name]==self.transport.getPeer():
                usName=name
                self.factory.users.pop(usName,None)
                break
        toSend="OUT{}".format(usName)
        for name in self.factory.users:
            self.factory.users[name].sendLine(toSend.encode())
                

    def lineReceived(self, line):
        line=line.decode()
        command=line[:3]
        message=line[3:]

        if command==("NME"):
        	if len(message>MAX_USER_LENGTH):    #Username too long
        		self.sendline(ER_LONG_NME.encode())
            elif len(self.factory.users)==MAX_USERS:    #Full server
                self.sendLine(ER_MAX_USERS.encode())
        	elif message in self.factory.users:         #Repeated Username
                self.sendLine(ER_REP_NME.encode())
            elif " " in message:                        #Forbidden character espace
                self.sendLine(ER_FORBID_CHARS.encode()) 
            else:                                          #Alright
                self.sendLine("+".encode())
                msgNewUs=("INN{}".format(message))
                for name in self.factory.users:
                    self.factory.users[name].sendLine(msgNewUs.encode())
                self.factory.users[message]=self.transport.getPeer()
        elif command==("MSG"):
            if len(message)>MAX_MSG_LENGTH
                self.sendLine(ER_LONG_MSG.encode())
            #Error de en cualquier otro caso
            else:
                #Get the username out of the Address
                address=self.transport.getPeer()
                for name in self.factory.users:
                    if self.factory.users[name]==address:
                        sendUser=name
                        break
                self.sendLine("+".encode)
                toSend="MSG{} {}".format(sendUser,message)
                for name in self.factory.users:
                    if name!=sendUser:
                        self.factory.users[name].sendLine(toSend.encode())
        else:
            self.sendLine(ER_COM_NOT_FOUND.encode())

                

                




        

class ChatFactory(Factory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return ChatProtocol(self)

if __name__ == "__main__":
	reactor.listenTCP(PORT, ChatFactory())
	reactor.run()
