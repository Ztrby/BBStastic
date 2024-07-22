import time
import sys
from urllib.request import urlopen 
from socket import timeout
import logging
import meshtastic
import meshtastic.serial_interface, meshtastic.tcp_interface
import BBScommands
import db_commands
from pubsub import pub
import errno 


try:

    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} IP")
        sys.exit(3)
    
 #  Create tables if they not exists allready
    db_commands.db_create()

    def onReceive(packet, interface): # called when a packet arrives
        BBScommands.readmessage(packet, interface)



    def onConnection(interface, topic=pub.AUTO_TOPIC): # called when we (re)connect to the radio
        print(f"Connected")

    def onDisconnect(interface, topic=pub.AUTO_TOPIC):
        print(f"Disconnected")
        #interface.close()
        """ try:
            print("reconnect")
            interface = meshtastic.tcp_interface.TCPInterface(sys.argv[1])
        except BrokenPipeError:
            print("==> BrokePipeerror pub")
        except:
            print(f"Error: Could not connect to {sys.argv[1]}")
            sys.exit(1) """
    try:
        pub.subscribe(onReceive, "meshtastic.receive")
        pub.subscribe(onConnection, "meshtastic.connection.established")
        pub.subscribe(onDisconnect, "meshtastic.connection.lost")
    except BrokenPipeError:
        print("==> BrokePipeerror pub")
    except IOError as e: 
        if e.errno == errno.EPIPE: 
            print(e.errno)

# Create inteface2
    try:
        interface = meshtastic.tcp_interface.TCPInterface(sys.argv[1])
    except:
        print(f"Error: Could not connect to {sys.argv[1]}")
        sys.exit(1)

    try:
        while True:
            time.sleep(1000)

    except KeyboardInterrupt:
        logging.info("Shutting down the server...")
        print(f"\nShutting down the server...")
        interface.close()
    except IOError as e: 
        if e.errno == errno.EPIPE: 
            print(e.errno)
            pass
    except BrokenPipeError:
        print("==> BrokePipeerror sleep")

except IOError as e: 
    if e.errno == errno.EPIPE: 
      print(e.errno)
      pass
       # Handling of the error
except ConnectionResetError:
    print("==> ConnectionResetError")
    pass
except timeout: 
    print("==> Timeout")
    pass
except BrokenPipeError:
    print("==> BrokePipeerror")


# interface = meshtastic.serial_interface.SerialInterface()




