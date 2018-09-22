from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor


class MulticastUDPClient(DatagramProtocol):

    def startProtocol(self):
        # Join the multicast address, so we can receive replies:
        self.transport.joinGroup("224.0.0.1")
        # Send to 224.0.0.1:10000 - all listeners on the multicast address
        # (including us) will receive this message.
        self.transport.write(bytes('Hello World','utf-8'), ("224.0.0.1", 10000))

    def datagramReceived(self, datagram, address):
        print("client:  Datagram {} received from {}".format(repr(datagram.decode('utf-8')), repr(address)))


reactor.listenMulticast(10000, MulticastUDPClient(), listenMultiple=True)
reactor.run()