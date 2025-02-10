# enip simulator server
# waits for a ENIP 'list identity' request and provides a response
import struct
import socket
import hexdump

from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

enip_type = 35 # Safety Discrete I/O Device
enip_vendor = 976 # Invensys Process Systems
enip_productName = b"Hudsucker Industries Portable Nuclear Generator (y'know, for kids)" # 
enip_productCode = 0 # "<I2" packing
enip_revision = 0 # "BB" packing
enip_status = 65535 #"I2" packing %#0.4x display
enip_state = 255 #"B" packing

# listen on tcp/44818
class SafetySimulator(Protocol):
  def __init__(self, factory):
    self.factory = factory
  def connectionMade(self):
    self.factory.numProtocols = self.factory.numProtocols + 1
    print("New connection made. There are currently %d open connections\n" % (self.factory.numProtocols))
    #self.transport.write("Welcome! There are currently %d open connections\n" % (self.factory.numProtocols))
  def connectionLost(self, reason):
    self.factory.numProtocols = self.factory.numProtocols - 1
    print("Connection closed. There are currently %d open connections\n" % (self.factory.numProtocols))
  def dataReceived(self, tdata):
    data = tdata
    tlen = len(tdata)
    print("received data: \n")
    hexdump.hexdump(data)
    if len(data) < 24:
      return # no answer, not valid
    totalConsumed = 0
    while totalConsumed < tlen:
      print("Processing data:")
      hexdump.hexdump(data)
      enip_fc = struct.unpack("<H", data[0:2])[0]
      dlen = 24 + struct.unpack("<H", data[2:4])[0]
      totalConsumed += dlen
      context = data[12:19]
      session_handle = data[4:9]
      response = ""
      csd = b""
      if 0x63 == enip_fc: # legit request
        csd += b"\x01\x00\x0c\x00"
        ev = b"\x01\x00"
        sa = b"\x00\x02\xaf\x12\x70\x77\x6e\x64" + b"\x00" * 8
        vi = struct.pack("<H", enip_vendor)
        dt = struct.pack("<H", enip_type)
        pc = struct.pack("<H", enip_productCode)
        rv = b"\x00\x01"
        st = struct.pack("<H", enip_status)
        serNum = b"toow" # 
        pl = struct.pack("B", len(enip_productName))
        nm = enip_productName
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
        print("sending reply:\n")
        hexdump.hexdump(enip_reply)
        self.transport.write(enip_reply) # will fix this later
      print("consumed %d bytes of %d total so far" % (totalConsumed, tlen))
      data = data[dlen:] # keep processing the pipeline

class SafetyFactory(Factory):
  def __init__(self):
    self.numProtocols = 0
  def buildProtocol(self, addr):
    return SafetySimulator(self)

endpoint = TCP4ServerEndpoint(reactor, 44819, backlog=50, interface='127.0.0.1')
endpoint.listen(SafetyFactory())
reactor.run()
