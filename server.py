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
import subprocess

def check_service_status():
    try:
        # Run the systemctl status command and capture the output
        result = subprocess.run(
            ['sudo', 'systemctl', 'status', 'mesh-bbs.service'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Check if "BrokenPipeError" is in the output
        if "BrokenPipeError: [Errno 32] Broken pipe" in result.stdout or "BrokenPipeError: [Errno 32] Broken pipe" in result.stderr:
            print("BrokenPipeError detected. Restarting the service...")
            restart_service()
        else:
            print("Service is running normally.")

    except Exception as e:
        print(f"An error occurred: {e}")

def restart_service():
    try:
        # Restart the service
        subprocess.run(['sudo', 'systemctl', 'restart', 'mesh-bbs.service'], check=True)
        print("Service restarted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart the service: {e}")
    



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
            check_service_status()

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




