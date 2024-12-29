
COLUMNS = "COLUMNS"
PACKET_LOG_DATA = "PacketLogData"

TABLES = {
    PACKET_LOG_DATA: {
        COLUMNS: {
            'PacketDataId': 'INTEGER PRIMARY KEY',
            'PacketType': 'TEXT',
            'SourceAddress': 'TEXT',
            'SourcePort': 'INTEGER',
            'DestinationAddress': 'TEXT',
            'DestinationPort': 'INTEGER',
            'PacketLengthBytes': 'INTEGER',
            'TimeCaptured': 'INTEGER'
        }
    }
}
