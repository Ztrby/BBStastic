import sqlite3
import datetime


def db_connect():
    try:
        connect = sqlite3.connect("BBStastic.db")
    except:
        print(f"Can not connect to database")
    return connect

def db_create():
    connect = db_connect()
    c = connect.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS hw(hw_id INTEGER PRIMARY KEY AUTOINCREMENT, \
              hw_name TEXT NOT NULL, \
              manufacture TEXT NOT NULL)")
    c.execute("CREATE TABLE IF NOT EXISTS nodes(node_id  PRIMARY KEY,  \
              short_name TEXT NOT NULL, \
              long_name TEXT NOT NULL, \
              mac_address, \
              hw_model, \
              role, \
              hop_start INTEGER, \
              hop_limit INTEGER, \
              snr, \
              lastheard, \
              lastconnected, \
              is_licensed INTEGER, \
              longitude, \
              latitude, \
              altitude INTEGER, \
              temperature, \
              relativeHumidity, \
              barometricPressure, \
              num_updates INTERGER)")
    c.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, \
            alias TEXT NOT NULL, \
            primnode NOT NULL, \
            FOREIGN KEY (primnode) \
            REFERENCES nodes (node_id))")
    c.close()
#    c.execute("CREATE TABLE IF NOT EXISTS mail")
    connect.commit()

def update_nodeinfo(node_id, shortname, longname , lastheard , lastconnected, macaddress, hwmodel, role, hopstart, hoplimit,snr, islic, long, lat, alt, temperature, relativeHumidity, barometricPressure):
        connect = db_connect()
        c = connect.cursor()
        SQLcommand = "UPDATE nodes set "
        if lastheard:
            SQLcommand = SQLcommand + "lastheard = '" + str(lastheard) + "'"
        else:
            SQLcommand = SQLcommand + "lastheard = '" + str(datetime.datetime.now().timestamp()) + "'"
        if shortname:
             SQLcommand = SQLcommand + " ,short_name = '" + shortname + "'"
        if longname:
             SQLcommand = SQLcommand + " , long_name = '" + longname + "'"
        if macaddress:
             SQLcommand = SQLcommand + " , mac_address = '" + macaddress + "'"
        if lastconnected:
            SQLcommand = SQLcommand + " , lastconnected = '" + lastconnected + "'"
        if role:
            SQLcommand = SQLcommand + " , role = '" + role + "'"
        if hopstart:
            SQLcommand = SQLcommand + " , hop_start = '" + str(hopstart) + "'"
        if hoplimit:
            SQLcommand = SQLcommand + " , hop_limit = '" + str(hoplimit) + "'"
        if snr:
            SQLcommand = SQLcommand + " , snr = '" + str(snr) + "'"
        if islic:
            SQLcommand = SQLcommand + " , is_licensed = '" + str(islic) + "'"
        if long:
            SQLcommand = SQLcommand + " , longitude = '" + str(long) + "'"
        if lat:
             SQLcommand = SQLcommand + " , latitude = '" + str(lat) + "'"
        if alt:
             SQLcommand = SQLcommand + " , altitude = '" + str(alt) + "'"
        if hwmodel:
             SQLcommand += f" , hw_model = '{hwmodel}'"
        if temperature:
             SQLcommand +=  f" , temperature = '{temperature}'"
        if relativeHumidity:
             SQLcommand +=  f" , relativeHumidity = '{relativeHumidity}'"
        if barometricPressure:
             SQLcommand +=  f" , barometricPressure = '{barometricPressure}'"

        SQLcommand = SQLcommand + " , num_updates = num_updates + 1 "
        
        
        exists = check_exists("nodes", "node_id", str(node_id))
        
        if exists == True:
            SQLcommand = SQLcommand + " WHERE node_id = '" + str(node_id) + "'"
            #print("Node " +node_id +" already in DB")
            #print("Update to DB: " + SQLcommand)
            c.execute(SQLcommand)
        else:
            c.execute("INSERT INTO nodes (node_id, short_name, long_name, num_updates) VALUES (?, ?, ?, ?)", (node_id, shortname, longname, 1,))
        connect.commit()
        connect.close()

def create_user(alias, node_id):
        connect = db_connect()
        c = connect.cursor()
        exists = check_exists("users", "primnode", node_id)
        if exists == True:
            print("User already in DB")           
        else: 
            c.execute("INSERT INTO users (alias, primnode) VALUES (?, ?)", (alias, node_id))
        connect.commit()
        connect.close()

def check_exists(database, col, value):
    c = db_connect().cursor()
    SQLstring = "SELECT " + col + " FROM " + database + " WHERE " + col + " = '" + value + "'"
    c.execute(SQLstring)
    exists = c.fetchone()
    if exists:
         return True
    else:
         return False
    
def statistics_nodes():
        connect = db_connect()
        c = connect.cursor()
        SQLstring = "SELECT \
                    hw_model, \
                    COUNT(*) \
                    FROM nodes \
                    GROUP BY hw_model \
                    ORDER BY COUNT(*) DESC"
        result = c.execute(SQLstring).fetchall()
        prettyresult = ""
        for res in result:
             prettyresult = prettyresult + str(res[0]) + "     " + str(res[1]) + "\n"
        return prettyresult

def statistic_mesh():
        connect = db_connect()
        c = connect.cursor()
        SQLstring = "SELECT \
                    COUNT(*) \
                    FROM nodes"
        result = c.execute(SQLstring).fetchone()
        prettyresult = result
        return str(result)
                    