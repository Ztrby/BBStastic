import BBSmenus
import nodes
import db_commands
import time

def readmessage(packet, interface):
    try:
        if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
            message_bytes = packet['decoded']['payload']
            message_string = message_bytes.decode('utf-8')
            meshfrom_hex_id = packet['fromId']
            sender_id = packet['from']
            to_id = packet.get('to')
            # Update database
            print("Textmessage resived")
            #nodes.update_node(interface, meshfrom_hex_id)

            #Check that message is a direct message to BBS-node
            mynode=interface.getNode('^local')

            if str(to_id)==str(mynode.nodeNum):
                nodes.update_connected(interface, meshfrom_hex_id)
                print("message: " + str(message_string) + " from " + str(meshfrom_hex_id))
                match len(message_string):
                    # First level main menu3
                    case 1:
                        match message_string.upper():
                            case "M":
                                print("Mailmenu")
                                replay(BBSmenus.mail_menu(), interface, meshfrom_hex_id)
                            case "N":
                                print("News menu")
                                replay(BBSmenus.news_menu(), interface, meshfrom_hex_id)
                            case "S":
                                print("Stats menu")
                                replay(BBSmenus.stats_menu(), interface, meshfrom_hex_id)
                            case "U":
                                print("User menu")
                                replay(BBSmenus.user_menu(), interface, meshfrom_hex_id)
                            case "Q":
                                print("Quick menu")
                                replay(BBSmenus.quick_menu(), interface, meshfrom_hex_id)
                            case "H":
                                print("Help menu")
                                replay(BBSmenus.help_menu(), interface, meshfrom_hex_id)
                            case _:
                                print("mainmenu")
                                replay(BBSmenus.main_menu(), interface, meshfrom_hex_id)
                    case 2:
                        # Second level menu
                        match message_string.upper():
                        # Mail
                            # Mail read
                            case "MR":
                                if db_commands.check_exists("users", "primnode", meshfrom_hex_id):
                                    replay("Mail read, not implemented yet", interface, meshfrom_hex_id)
                                else:
                                    replay("You have to create a user to read mail", interface, meshfrom_hex_id)
                            # Mail send
                            case "MS":
                                replay("Mail send, not implemented yet", interface, meshfrom_hex_id)
                            # Mail delete
                            case "MD":
                                replay("Mail delete, not implemented yet", interface, meshfrom_hex_id)
                        # News
                            # News read
                            case "NR":
                                replay("News read, not implemented yet", interface, meshfrom_hex_id)
                            # News post
                            case "NP":
                                replay("News post, not implemented yet", interface, meshfrom_hex_id)
                            # News delete
                            case "ND":
                                replay("News delete, not implemented yet", interface, meshfrom_hex_id)
                        # Stats
                            # Stats nodes
                            case "SN":
                                replay(db_commands.statistics_nodes(), interface, meshfrom_hex_id)
                            # Stats Mesh
                            case "SM":
                                replay("There are: " + db_commands.statistic_mesh() + " known nodes in this mesh" , interface, meshfrom_hex_id)
                        # User menu
                            # User Create
                            case "UC":
                                if db_commands.check_exists("users", "primnode", meshfrom_hex_id):
                                    replay("You are already a user in the BBS", interface,meshfrom_hex_id)
                                else:
                                    replay("User crete not implementet yet", interface, meshfrom_hex_id)
                            # User Update
                            case "UU":
                                replay("User update, not implemented yet", interface, meshfrom_hex_id)
                            # User Create
                            case "UD":
                                replay("User Delete, not implemented yet", interface, meshfrom_hex_id)
                            case _:
                                print("mainmenu")
                                replay(BBSmenus.main_menu(), interface, meshfrom_hex_id)
                    case 4:
                        # Second level menu
                        match message_string.upper():
                            case "HELP":
                                print("Help menu")
                                replay(BBSmenus.help_menu(), interface, meshfrom_hex_id)
                            case _:
                                replay(BBSmenus.main_menu(), interface, meshfrom_hex_id) 
                    # Protecting from autoreplay ping pong        
                    case _ if len(message_string) < 5:
                        print("under 5 char sent")
                        replay(BBSmenus.main_menu(), interface, meshfrom_hex_id)         

                    case _:
                        print(f"Received: {message_string} from {meshfrom_hex_id} , {sender_id} , {to_id}")
            else:
                 print(f"Not sent to BBS-node")
        # NODEINFO_APP
        if 'decoded' in packet and packet['decoded']['portnum'] == 'NODEINFO_APP':
            meshfrom_hex_id = packet['fromId']
            if meshfrom_hex_id:
                nodes.update_node_packet_nodeapp(interface, meshfrom_hex_id,packet)
        # TETELEMETRY_APP
        if 'decoded' in packet and packet['decoded']['portnum'] == 'TELEMETRY_APP':
            meshfrom_hex_id = packet['fromId']
            nodes.update_node_packet_teleapp(interface, meshfrom_hex_id,packet)
        # POSITION_APP
        if 'decoded' in packet and packet['decoded']['portnum'] == 'POSITION_APP':
            meshfrom_hex_id = packet['fromId']
            nodes.update_node_packet_posapp(interface, meshfrom_hex_id,packet)
        if 'decoded' in packet and packet['decoded']['portnum'] == 'NEIGHBORINFO_APP':
            meshfrom_hex_id = packet['fromId']
            print("NEIGHBORINFO recived from " + meshfrom_hex_id)
            nodes.update_node_packet_neighborapp(interface, meshfrom_hex_id,packet)
    except KeyError as e:
            print(f"Error processing packet: {e}")


def replay(answer_string, interface, dest):
    max_size = 180
    for i in range(0, len(answer_string), max_size):
        piece = answer_string[i:i + max_size]
        interface.sendText(
            text=piece,
            destinationId=dest,
            wantAck=False,
            wantResponse=False
        )
        time.sleep(5)


""" def idToHex(nodeId):
    return '!' + hex(nodeId)[2:] """

