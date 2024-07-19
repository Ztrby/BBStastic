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
                            case "U":
                                print("User menu")
                                replay(user_menu(), interface, meshfrom_hex_id)
                            case "Q":
                                print("Quick menu")
                                replay(quick_menu(), interface, meshfrom_hex_id)
                            case "H":
                                print("Help menu")
                                replay(help_menu(), interface, meshfrom_hex_id)
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
                        # User menu
                            # User Create
                            case "UC":
                                replay("User create, not implemented yet", interface, meshfrom_hex_id)
                            # User Update
                            case "UU":
                                replay("User update, not implemented yet", interface, meshfrom_hex_id)
                            # User Create
                            case "UD":
                                replay("User Delete, not implemented yet", interface, meshfrom_hex_id)
                            case _:
                                replay(main_menu(), interface, meshfrom_hex_id)
                    case 4:
                        # Second level menu
                        match message_string.upper():
                            case "HELP":
                                print("Help menu")
                                replay(help_menu(), interface, meshfrom_hex_id)
                            case _:
                                replay(main_menu(), interface, meshfrom_hex_id) 
                    # Protecting from autoreplay ping pong        
                    case _ if len(message_string) < 5:
                        print("under 5 char sent")
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
    menu_string = f"***** Main menu ******\n[M]ail\n[N]ews\n[S]tats\n[U]ser\n[Q]uick commands\n[H]elp"
    return menu_string

def mail_menu():
    menu_string = f"***** Mail menu ******\n[MR]ead\n[MS]end\n[MD]elete"
    return menu_string

def news_menu():
    menu_string = f"***** News menu ******\n[NR]ead\n[NP]ost\n[ND]elete"
    return menu_string

def stats_menu():
    menu_string = f"***** Stats menu ******\n[SN]Nodes\n[SM]Mesh"
    return menu_string

def user_menu():
    menu_string = f"***** User menu ******\n[UC]Create user\n[UU]Update user\n[UD]User delete"
    return menu_string

def quick_menu():
    menu_string = f"***** Quick menu ******\n[MS!!shortname!!subject!!text]\n"
    return menu_string

def help_menu():
    menu_string = f"***** Help menu ******\nGo to link to see onlinehelp\nhttps://github.com/Ztrby/BBStastic"
    return menu_string