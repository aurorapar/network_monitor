# Network Monitor

Logs network traffic sniffed on a specified interface to a local SQLite3 database. Uses pyshark as a wrapper to wireshark.

Stores the following data: 
* PacketType
* SourceAddress
* SourcePort
* DestinationAddress
* DestinationPort
* PacketLengthBytes
* TimeCaptured
  
## TODO: 
Add a queryable graph
