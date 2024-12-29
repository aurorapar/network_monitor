import datetime
import ipaddress
import time
import traceback

from dateutil.parser import parse
from pyshark.packet.packet import Packet

from data_objects import DataObject
from logger.sql.tables import TABLES, COLUMNS, PACKET_LOG_DATA


def ip_address_to_integer(addr: str):
    return int(ipaddress.ip_address(addr))


def integer_to_ip_address(addr: int):
    return ipaddress.ip_address(addr).compressed


class PacketDataObject(DataObject):
    PacketDataId = None
    PacketType = None
    SourceAddress = None
    SourcePort = None
    DestinationAddress = None
    DestinationPort = None
    PacketLengthBytes = None
    TimeCaptured = None

    TableName = PACKET_LOG_DATA

    def __init__(self, packet: Packet):
        try:
            self.PacketType = packet.highest_layer

            if hasattr(packet, 'ip'):
                self.SourceAddress = packet.ip.src
                self.DestinationAddress = packet.ip.dst
            elif hasattr(packet, 'ipv6'):
                self.SourceAddress = packet.ipv6.src
                self.DestinationAddress = packet.ipv6.dst
            elif hasattr(packet, 'arp'):
                self.SourceAddress = packet.arp.src_proto_ipv4
                self.DestinationAddress = packet.arp.dst_proto_ipv4

            for layer in packet.layers:
                port = [getattr(layer, attr) for attr in dir(layer) if attr == 'srcport']
                if port:
                    self.SourcePort = int(port[0])
                    break

            for layer in packet.layers:
                port = [getattr(layer, attr) for attr in dir(layer) if attr == 'dstport']
                if port:
                    self.DestinationPort = int(port[0])
                    break

            self.PacketLengthBytes = int(packet.length)
            self.TimeCaptured = parse(time.ctime(float(packet.sniff_timestamp))).astimezone(datetime.timezone.utc)

        except Exception as e:
            packet.show()
            print(traceback.format_exc())

    def adapt(self):
        data = {}
        for column_name in [col for col in TABLES[PACKET_LOG_DATA][COLUMNS].keys() if not col.lower().endswith('id')]:
            data[column_name] = getattr(self, column_name)
        if self.PacketDataId is not None:
            data['PacketDataId'] = self.PacketDataId
        # data['SourceAddress'] = ip_address_to_integer(self.SourceAddress)
        # data['DestinationAddress'] = ip_address_to_integer(self.DestinationAddress)
        data['TimeCaptured'] = int(self.TimeCaptured.timestamp()) if self.TimeCaptured else int(datetime.datetime.utcnow().timestamp())
        return data

    def convert(self, database_result):
        raise NotImplementedError()
