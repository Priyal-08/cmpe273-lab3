from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor


class MulticastUDPServer(DatagramProtocol):

    def startProtocol(self):
        """
        Called after protocol has started listening.
        """
        # Set the TTL>1 so multicast will cross router hops:
        self.transport.setTTL(5)
        # Join a specific multicast group:
        self.transport.joinGroup("224.0.0.1")

    def datagramReceived(self, datagram, address):
        print("server: Datagram {} received from {}".format(repr(datagram.decode('utf-8')), repr(address)))
        if datagram == bytes('Hello World','utf-8') or datagram == 'Hello World':
            self.transport.write(bytes('Hello World Response','utf-8'), ("224.0.0.1", 10000))


# We use listenMultiple=True so that we can run MulticastUDPServer and
# MulticastUDPClient on same machine
reactor.listenMulticast(10000, MulticastUDPServer(),listenMultiple=True)
reactor.run()