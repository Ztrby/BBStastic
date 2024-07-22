def main_menu():
    menu_string = f"***** Main menu ******\n[M]ail\n[N]ews\n[S]tats\n[U]ser\n[Q]uick commands\n[H]elp"
    return menu_string

def mail_menu():
    menu_string = f"***** Mail menu ******\n[MR] Read\n[MS] Send\n[MD] Delete"
    return menu_string

def news_menu():
    menu_string = f"***** News menu ******\n[NR] Read\n[NP] Post\n[ND] Delete"
    return menu_string

def stats_menu():
    menu_string = f"***** Stats menu ******\n[SN] Nodes\n[SM] Mesh"
    return menu_string

def user_menu():
    menu_string = f"***** User menu ******\n[UC] Create user\n[UU] Update user\n[UD] User delete"
    return menu_string

def quick_menu():
    menu_string = f"***** Quick menu ******\nMS!!shortname!!subject!!text\n"
    return menu_string

def help_menu():
    menu_string = f"***** Help menu ******\nGo to link to see onlinehelp\nhttps://github.com/Ztrby/BBStastic"
    return menu_string