#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

### Protocol Implementation

# This is just about the simplest possible protocol
class Echo(Protocol):
    def dataReceived(self, data):
        """
        As soon as any data is received, write it back.
        """
        if data.startswith(b'ver'):
            self.transport.write(b'ACME Widgets version 4.0\n> ')
        elif data.startswith(b'EVIL'):
            self.transport.write(b'Rebooting...\n> ')
            self.transport.loseConnection()
        else:
            self.transport.write(b'Unknown command\n> ')
        return


def main():
    f = Factory()
    f.protocol = Echo
    reactor.listenTCP(1234, f)
    reactor.run()

if __name__ == '__main__':
    main()
