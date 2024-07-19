def readmessage(packet, interface):
    try:
        if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
            message_bytes = packet['decoded']['payload']
            message_string = message_bytes.decode('utf-8')
            meshfrom_hex_id = packet['fromId']
            sender_id = packet['from']
            to_id = packet.get('to')

            #Check that message is a direct message to BBS-node
            if to_id==3662954260:
                match len(message_string):
                    # First level main menu3
                    case 1:
                        match message_string.upper():
                            case "M":
                                print("Mailmenu")
                                replay(mail_menu(), interface, meshfrom_hex_id)
                            case "N":
                                print("News menu")
                                replay(news_menu(), interface, meshfrom_hex_id)
                            case "S":
                                print("Stats menu")
                                replay(stats_menu(), interface, meshfrom_hex_id)
                            case _:
                                print("mainmenu")
                                replay(main_menu(), interface, meshfrom_hex_id)
                    case 2:
                        # Second level menu
                        match message_string.upper():
                        # Mail
                            # Mail read
                            case "MR":
                                replay("Mail read, not implemented yet", interface, meshfrom_hex_id)
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
                                replay("Stats nodes, not implemented yet", interface, meshfrom_hex_id)
                            # Stats Mesh
                            case "SM":
                                replay("Stats mesh, not implemented yet", interface, meshfrom_hex_id)
                            case _:
                                replay(main_menu(), interface, meshfrom_hex_id)  
                            
                    case _ if len(message_string) < 5:
                        print("not one or 2 caracater")
                        replay(main_menu(), interface, meshfrom_hex_id)         

                    case _:
                        print(f"Received: {message_string} from {meshfrom_hex_id} , {sender_id} , {to_id}")
            else:
                 print(f"Not sent to BBS-node")
    except KeyError as e:
            print(f"Error processing packet: {e}")

def replay(answer_string, interface, dest):
    interface.sendText(\
    text=answer_string, \
    destinationId=dest, \
    wantAck=False, \
    wantResponse=False)
    
    
    
def get_node_short_name(node_id, interface):
    node_info = interface.nodes.get(node_id)
    if node_info:
        return node_info['user']['shortName']
    return None

def idToHex(nodeId):
    return '!' + hex(nodeId)[2:]

def main_menu():
    mainmenu_string = f"***** Main menu ******\n[M]ail\n[N]ews\n[S]tats"
    return mainmenu_string

def mail_menu():
    menu_string = f"***** Mail menu ******\n[MR]ead\n[MS]end\n[MD]elete"
    return menu_string

def news_menu():
    menu_string = f"***** News menu ******\n[NR]ead\n[NP]ost\n[ND]elete"
    return menu_string

def stats_menu():
    menu_string = f"***** Stats menu ******\n[SN]Nodes\n[SM]Mesh"
    return menu_string


