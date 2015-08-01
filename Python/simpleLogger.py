import plugins
import os

@plugins.raw_packet_hook
def log_that_shit(context, packet, packet_type, packet_subtype):
    """
    :type context: ShipProxy.ShipProxy
    """
    if not os.path.exists("rawlog/%i" % context.connTimestamp):
        os.makedirs("rawlog/%i" % context.connTimestamp)
    packet_file = open("rawlog/%i/%s.%x-%x.%s.bin" % (context.connTimestamp, context.packetCount, packet_type, packet_subtype, context.transport.getPeer().host), 'wb')
    packet_file.write(packet)
    packet_file.close()

    return packet
