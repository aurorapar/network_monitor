import asyncio
import threading

import pyshark
from pyshark.packet.packet import Packet

from logger import Logger, LoggerMethod


class Monitor(threading.Thread):

    interface = None
    threads = []
    logger = None
    capture = None

    def __init__(self, interface, logging_method: LoggerMethod):
        threading.Thread.__init__(self)
        self.interface = interface
        self.logger = Logger(logging_method)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.capture = pyshark.LiveCapture(interface=self.interface)
        self.capture.apply_on_packets(self.log_packet_data)

    def log_packet_data(self, packet: Packet):
        self.logger.log(packet)

