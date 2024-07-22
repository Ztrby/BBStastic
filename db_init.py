import meshtastic
import meshtastic.serial_interface, meshtastic.tcp_interface
import sys
import db_commands

# Create inteface2
try:
        interface = meshtastic.tcp_interface.TCPInterface(sys.argv[1])
except:
        print(f"Error: Could not connect to {sys.argv[1]}")
        sys.exit(1)

if interface.nodes:
    for node in interface.nodes.values():
        # print (node)
        

        

        if "snr" in node:
            print("SNR:", node["snr"])
        if "lastHeard" in node:
            last = node["lastHeard"]
            print("Last Heard:", node["lastHeard"])
        else:
            last = ""
        if "hopsAway" in node:
            print("Hops Away:", node["hopsAway"])
        if "hopLimit" in node:
            print("Hoplimit:", node["hopLimit"])
        if "role" in node:
            print("Role:", node["role"])

        if "user" in node:
            if "macaddr" in node["user"]:
                macaddress = node["user"]["macaddr"]
            else:
                macaddress = "N/A"
            if "hwModel" in node["user"]:
                hwmodel = node["user"]["hwModel"]
                print("Hardware Model:", node["user"]["hwModel"])
            else:
                hwmodel = ""
        if "position" in node:
            if "latitude" in node["position"]:
                lat = node["position"]["latitude"]
                print("Longitude:", node["position"]["latitude"])
            else:
                lat = ""
            if "longitude" in node["position"]:
                long = node["position"]["longitude"]
                print("Longitude:", node["position"]["longitude"])
            else:
                long = ""
            if "altitude" in node["position"]:
                alt = node["position"]["altitude"]
                print("Altitude:", node["position"]["altitude"])
            else:
                alt = ""
            if "time" in node["position"]:
                print("Time:", node["position"]["time"])

        if "deviceMetrics" in node:
            if "batteryLevel" in node["deviceMetrics"]:
                print("Battery Level:", node["deviceMetrics"]["batteryLevel"])
            if "voltage" in node["deviceMetrics"]:
                print("Voltage:", node["deviceMetrics"]["voltage"])
            if "channelUtilization" in node["deviceMetrics"]:
                print("Channel Utilization:", node["deviceMetrics"]["channelUtilization"])
            if "airUtilTx" in node["deviceMetrics"]:
                print("Air Util Tx:", node["deviceMetrics"]["airUtilTx"])
        db_commands.update_nodeinfo(node["user"]["id"],node["user"]["shortName"], node["user"]["longName"],last,"",macaddress,hwmodel,"N/A","N/A","N/A","N/A","N/A",long, lat ,alt,"","","")
        print("\n")
interface.close()