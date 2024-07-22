import db_commands
import datetime

def update_node(interface, nodeid):
    node_info = interface.nodes.get(nodeid)
    if node_info:
        shortname = node_info['user']['shortName']
        longname = node_info['user']['longName']
        if "macaddr" in node_info["user"]:
            macaddr = node_info["user"]["macaddr"]
        else:
            macaddr = ""
        if "hwModel" in node_info["user"]:
            hwmodel = node_info["user"]["hwModel"]
        else:
            hwmodel = ""
        if "longitude" in node_info["position"]:
            long = node_info["position"]["longitude"]
        else:
            long = ""
        if "latitude" in node_info["position"]:
            lat = node_info["position"]["latitude"]
        else:
            lat = ""
        if "altitude" in node_info["position"]:
            alt = node_info["position"]["altitude"]
        else:
            alt = ""
        if "isLicensed" in node_info["user"]:
            lic = node_info["user"]["isLicensed"]
        else:
            lic = ""
        
        
        db_commands.update_nodeinfo(nodeid, shortname, longname, "", "" , macaddr, hwmodel, "", "","","",lic,long,lat,alt)

def update_node_packet_nodeapp(interface, nodeid, packet):
    node_info = packet['decoded'].get('user', {})
    print(f"Nodeinfo recieved from: {nodeid}")
    hoplimit = ""
    snr = ""
    hopstart = ""
    if 'hopLimit' in packet:
        hoplimit = packet['hopLimit']
    if 'rxSnr' in packet:
        snr = packet['rxSnr']
    if 'rxRssi' in packet:
        rssi = packet['rxRssi']
    if 'hopStart' in packet:
        hopstart = packet['hopStart']
        db_commands.update_nodeinfo(nodeid, node_info.get('shortName', ''), node_info.get('longName', '') , str(datetime.datetime.now().timestamp()), "", \
                                node_info.get('macaddr', ''),node_info.get('hwModel', ''),node_info.get('role', ''),hopstart,hoplimit,snr,node_info.get('isLicensed', ''),"","","","","","")

def update_node_packet_posapp(interface, nodeid, packet):
    if packet['decoded'].get('portnum') == 'POSITION_APP':         
        position = packet['decoded']['position']
        print(f"Positioninfo recieved from: {nodeid}")
        hoplimit = ""
        snr = ""
        hopstart = ""
        if 'hopLimit' in packet:
            hoplimit = packet['hopLimit']
        if 'rxSnr' in packet:
            snr = packet['rxSnr']
        if 'rxRssi' in packet:
            rssi = packet['rxRssi']
        if 'hopStart' in packet:
            hopstart = packet['hopStart']
        db_commands.update_nodeinfo(nodeid, "","", str(datetime.datetime.now().timestamp()) , "","","","",hopstart,hoplimit,snr,"", \
                                position.get('latitude', ''), position.get('longitude', ''), position.get('altitude', ''),"","","")

def update_node_packet_teleapp(interface, nodeid, packet):
    if packet['decoded'].get('portnum') == 'TELEMETRY_APP':
            hoplimit = ""
            snr = ""
            hopstart = ""
            telemetry = packet['decoded'].get('telemetry', {})
            if 'hopLimit' in packet:
                hoplimit = packet['hopLimit']
            if 'rxSnr' in packet:
                snr = packet['rxSnr']
            if 'rxRssi' in packet:
                rssi = packet['rxRssi']
            if 'hopStart' in packet:
                hopstart = packet['hopStart'] 
            environment_metrics = telemetry.get('environmentMetrics', {})
            if environment_metrics:
                print(f"Recieved environment_metrics from {nodeid}")
                db_commands.update_nodeinfo(nodeid,"","",str(datetime.datetime.now().timestamp()),"","","","",hopstart,hoplimit,snr,"","","","", \
                                            environment_metrics.get('temperature', ''),environment_metrics.get('relativeHumidity', ''),environment_metrics.get('barometricPressure', ''))
def update_node_packet_neighborapp(interface, nodeid, packet):
    if packet['decoded'].get('portnum') == 'NEIGHBORINFO_APP':
            # Neighbor Information
            print("  Neighbor Information:")
            message = mesh_pb2.NeighborInfo()
            payload_bytes = packet['decoded'].get('payload', b'')
            message.ParseFromString(payload_bytes)
            print(f"    Node ID: {message.node_id} / {idToHex(message.node_id)}")
            print(f"    Last Sent By ID: {message.last_sent_by_id}")
            print(f"    Node Broadcast Interval (secs): {message.node_broadcast_interval_secs}")
            print("    Neighbors:")
            for neighbor in message.neighbors:
                print(f"      Neighbor ID: {neighbor.node_id} / {idToHex(neighbor.node_id)}")
                print(f"        SNR: {neighbor.snr}")

def update_connected(interface, nodeid):
    node_info = interface.nodes.get(nodeid)
    db_commands.update_nodeinfo(nodeid,node_info['user']['shortName'],node_info['user']['longName'],str(datetime.datetime.now().timestamp()), \
                                str(datetime.datetime.now().timestamp()),"","","","","","","","","","","","","")


