import sqlite3
import time

from pyshark.packet.packet import Packet

from data_objects.packet import PacketDataObject
from logger.sql.inserts import insert
from logger.sql.create_tables import create_tables
from settings import SQLITE_DATABASE_LOCATION, LoggerMethod


class PacketLogData:
    PacketDataId = None
    PacketType = None
    SourceAddress = None
    SourcePort = None
    DestinationAddress = None
    DestinationPort = None
    PacketLengthBytes = None
    TimeCaptured = None

    def __init__(self, packet: Packet):
        self.PacketType = packet.highest_layer
        self.SourceAddress = packet.ip.src

        for layer in packet.layers:
            port = [getattr(layer, attr) for attr in dir(layer) if attr == 'srcport']
            if port:
                self.SourcePort = int(port[0])
                break

        self.DestinationAddress = packet.ip.dst

        for layer in packet.layers:
            port = [getattr(layer, attr) for attr in dir(layer) if attr == 'dstport']
            if port:
                self.DestinationPort = int(port[0])
                break

        self.PacketLengthBytes = packet.length
        self.TimeCaptured = time.ctime(float(packet.sniff_timestamp))


class Logger:

    method = None
    initiated = False

    def __init__(self, method: LoggerMethod):
        match method:

            case LoggerMethod.SQLite:
                self.method = method

            case _:
                raise NotImplemented(f"Logging Method {str(method)} is not supported")

    def log(self, packet: Packet):
        match self.method:

            case LoggerMethod.SQLite:
                self.log_sqlite(packet)

            case _:
                raise NotImplemented(f"Logging Method {str(self.method)} is not supported")

    def log_sqlite(self, packet: Packet):
        packet_data = PacketDataObject(packet)
        sqlite_database = SQLITE_DATABASE_LOCATION
        database = sqlite3.connect(sqlite_database)
        self.setup_tables(database)
        insert(database, packet_data.TableName, [packet_data.adapt()])

    def setup_tables(self, conn: sqlite3.Connection):
        if not self.initiated:
            create_tables(conn)
            self.initiated = True
