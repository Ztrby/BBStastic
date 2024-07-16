import time
import logging
import meshtastic
import meshtastic.serial_interface, meshtastic.tcp_interface
from pubsub import pub

def onReceive(packet, interface): # called when a packet arrives
    print(f"Received: ")
    logging.info(f"Packet received")

def onConnection(interface, topic=pub.AUTO_TOPIC): # called when we (re)connect to the radio
    print(f"Connected")

pub.subscribe(onReceive, "meshtastic.receive")
pub.subscribe(onConnection, "meshtastic.connection.established")

# Create inteface
interface = meshtastic.tcp_interface.TCPInterface(hostname='192.168.100.165')
# interface = meshtastic.serial_interface.SerialInterface()


try:
    while True:
        time.sleep(1000)

except KeyboardInterrupt:
    logging.info("Shutting down the server...")
    interface.close()
