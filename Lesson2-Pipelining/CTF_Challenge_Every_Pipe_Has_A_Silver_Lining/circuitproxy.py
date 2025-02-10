from uuid import uuid4 as uuid

from circuits import Component
from circuits.net.events import close, connect, write
from circuits.net.sockets import TCPClient, TCPServer
import hexdump
import struct
restricted_command_list = [b"\x63\x00", # list identity
                           b"\x04\x00", # list services
                           b"\x64\x00", # list interfaces
                           b"\x64\x00", # register session
                           b"\x66\x00", # unregister session
                           b"\x6f\x00", # send rr data
                           b"\x70\x00" # send unit data 
                           ]

whitelist = ['192.168.0.99', '10.2.0.1']

enip_type = 101 # Unknown
enip_vendor = 978 # Reserved
enip_productName = b"Fauxfino Shallow Packet Inspection Engine (Unauthorized Access Detected)" # 
enip_productCode = 0 # "<I2" packing
enip_revision = 0 # "BB" packing
enip_status = 65535 #"I2" packing %#0.4x display
enip_state = 255 #"B" packing

class Client(Component):

    channel = "client"

    def init(self, sock, host, port, channel=channel):
        self.sock = sock
        self.host = host
        self.port = port

        TCPClient(channel=self.channel).register(self)

    def ready(self, *args):
        self.fire(connect(self.host, self.port))

    def disconnect(self, *args):
        self.fire(close(self.sock), self.parent.channel)

    def read(self, data):
        self.fire(write(self.sock, data), self.parent.channel)


class Proxy(Component):

    channel = "server"

    def init(self, bind, host, port):
        self.bind = bind
        self.host = host
        self.port = port

        self.clients = dict()

        TCPServer(self.bind).register(self)

    def connect(self, sock, host, port):
        channel = uuid()

        client = Client(
            sock, self.host, self.port, channel=channel
        ).register(self)

        self.clients[sock] = client

    def disconnect(self, sock):
        client = self.clients.get(sock)
        if client is not None:
            client.unregister()
            del self.clients[sock]

    def read(self, sock, data):
        client = self.clients[sock]
        print("proxy received the following request from", sock.getpeername()[0])
        raddr, rport = sock.getpeername()
        packet_okay = False
        if raddr in whitelist:
            print("in whitelist, all data allowed")
            packet_okay = True
        else:
            print("not in whitelist, applying strict settings")
            packet_okay = self.check_packet(sock, data)
        if packet_okay:
            self.fire(write(data), client.channel)
        else:
            self.disconnect(sock)
        return

#    @staticmethod
    def generate_error_response(self, data, error, fakeip):
        enip_fc = struct.unpack("<H", data[0:2])[0]
        context = data[12:19]
        session_handle = data[4:9]
        csd = b""
        csd += b"\x01\x00\x0c\x00"
        ev = b"\x01\x00"
        sa = b"\x00\x02\xaf\x12" + fakeip + b"\x00" * 8
        vi = struct.pack("<H", enip_vendor)
        dt = struct.pack("<H", enip_type)
        pc = struct.pack("<H", enip_productCode)
        rv = b"\x00\x01"
        st = struct.pack("<H", enip_status)
        serNum = b"\x00\x00\x00\x00" # 
        pl = struct.pack("B", len(error))
        nm = error
        state = struct.pack("B", enip_state)
        reply = ev+sa+vi+dt+pc+rv+st+serNum+pl+nm+state
        csd += struct.pack("<H", len(reply)) + reply
        enip_reply = b"\x63\x00"
        enip_reply += struct.pack("<H", len(csd))
        enip_reply += session_handle
        enip_reply += b"\x00\x00\x00\x00" # success
        enip_reply += context
        enip_reply += b"\x00\x00\x00\x00" # options
        enip_reply += csd
        enip_reply += b"\x00" * 24
        return enip_reply
    
    # check packet and generate response if it's invalid
    def check_packet(self, sock, data):
        print("received data: \n")
        hexdump.hexdump(data)
        if len(data) < 24:
            print("sending invalid request response")
            padbytes = 24 - len(data)
            enip_reply = self.generate_error_response(data + b"\x00" * padbytes, b"Fauxfino Shallow Packet Inspection Engine (Invalid request)", b"derp")
            sock.send(enip_reply)
            return False # no answer, not valid
        if(data.startswith(b"\x00"*24)):
            print("!!!TALOS EVASION!!!")
            enip_reply = self.generate_error_response(data, b"TALOS Evasion Detected, Disconnecting (https://talosintelligence.com/vulnerability_reports/TALOS-2017-0440)", b"jred")
            sock.send(enip_reply)
            return False
        if(data[0:2] in restricted_command_list):
            print("!!!FILTERED!!!")
            enip_reply = self.generate_error_response(data, b"Fauxfino Shallow Packet Inspection Engine (Unauthorized Access Detected)", b"noob")
            sock.send(enip_reply)
            return False
        print("PACKET OKAY, FORWARDING")
        return True




app = Proxy(("0.0.0.0", 44818), "127.0.0.1", 44819)

from circuits import Debugger
#Debugger().register(app)

app.run()
