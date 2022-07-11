from operator import concat
import re
from xmlrpc.server import SimpleXMLRPCServer
import numpy as np #pip install numpy (utilizzato per la conversione int64)
from random import randint
import mysql.connector #pip install mysql-connector
import xml.etree.ElementTree as ET #di libreria standard
from lxml import etree #pip install lxml 
import os
import csv
import time
from socketserver import ThreadingMixIn
import meterbus
debug  = 1
def getreading(codice,datalettura,tipodato,SetDay):
        
        if True:  # codice == DatiAccesso.codiceSessione and dati.controlloAccesso() == True :
            mydb = mysql.connector.connect(
                host="192.168.88.150",
                user="root",
                password="",
                database="raf_db",
                allow_local_infile=True
            )

        mycursor = mydb.cursor()
        
        if int(SetDay) == 0:
            if tipodato == "MeasureUnit.HCA":
                Query = "SELECT Value , Status , ReadDate, SecAddr, LastRecived From Telegrams WHERE idCONfk = " + str(codice) +" And ReadDate ='" + datalettura + "' AND (Units ='" + tipodato + "' OR Units ='% BATT') ORDER BY SecAddr DESC "
            else:                 
                Query = "SELECT Value , Status , ReadDate, SecAddr, LastRecived From Telegrams WHERE idCONfk = " + str(codice) +" And ReadDate ='" + datalettura + "' AND Units ='" + tipodato + "' ORDER BY SecAddr DESC "
        else:
            Query = "SELECT SetDayValue , Status , ReadDate, SecAddr, LastRecived From Telegrams WHERE idCONfk = " + str(codice) +" And ReadDate ='" + datalettura + "' AND (Units ='" + tipodato + "' OR Units ='% BATT')  ORDER BY SecAddr DESC "
        print(Query)
        mycursor.execute(Query)

        myresult = mycursor.fetchall()
        mycursor.close()
        

        if myresult != None:
            return myresult
        else:
           
            return "KO"

def getmodemsettings(codice):
    debug = True
    
    if True:  # codice == DatiAccesso.codiceSessione and dati.controlloAccesso() == True :
            mydb = mysql.connector.connect(
                host="192.168.88.150",
                user="root",
                password="",
                database="raf_db",
                allow_local_infile=True
            )

    mycursor = mydb.cursor()
    Query = "Select * From Modems WHERE idCONfk = " + str(codice) 
    if debug:
        print(Query)
    mycursor.execute(Query)
    columns = mycursor.description 
    myresult = [{columns[index][0]:column for index, column in enumerate(value)} for value in mycursor.fetchall()]
    mycursor.close()
    if myresult != None:
            return myresult
    else:
           
        return "KO"


def pushmodemsettings (settings):
    debug = True
    
    if True:  # codice == DatiAccesso.codiceSessione and dati.controlloAccesso() == True :
            mydb = mysql.connector.connect(
                host="192.168.88.150",
                user="root",
                password="",
                database="raf_db",
                allow_local_infile=True
            )
    if debug:
        print(settings)
    mycursor = mydb.cursor()
    for line in settings.splitlines():
        buff = line.split("=")
        if "SyncID" in buff[0] or buff[0] == "":
            id = buff[1]
            continue
        Query = "SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'Modems' AND COLUMN_NAME = '" + buff[0] + "'  AND TABLE_SCHEMA = 'raf_db';"
        if debug:
            print(Query)
        mycursor.execute(Query)
        Myresults = mycursor.fetchall()
        filedtype = Myresults[0][0]
        if debug:
            print( "FieldType : " + filedtype)
        if "int" in filedtype :
            Query = "UPDATE Modems SET " + buff[0] + " = " + buff[1] + " WHERE idCONfk = " + id + ";"
        else:
             Query = "UPDATE Modems SET " + buff[0] + " = '" + buff[1] + "' WHERE idCONfk = " + id + ";"
        if debug:
            print(Query)
        mycursor.execute(Query)
        mydb.commit()
    mycursor.close()
    return "OK"

def CreateRow(conid):
    if True:  # codice == DatiAccesso.codiceSessione and dati.controlloAccesso() == True :
        mydb = mysql.connector.connect(
            host="192.168.88.150",
            user="root",
            password="",
            database="raf_db",
            allow_local_infile=True
        )
    mycursor = mydb.cursor()
    Query="INSERT INTO Modems (idCONfk) VALUES ( " + str(conid) + ");"
    print(Query)
    mycursor.execute(Query)
    mydb.commit()
    mycursor.close()
    return "OK"

def AllDataToCSV(condID,units):
    import meterbus
    import mysql.connector
    
    fieldallowd = ["MeasureUnit.HCA" , "MeasureUnit.DATE", "MeasureUnit.WH", "MeasureUnit.M3"]
    mydb = mysql.connector.connect(
        host="192.168.88.150",
        user="root",
        password="",
        database="raf_db",
        allow_local_infile=True
    )
    mycursor = mydb.cursor()
    Query = "SELECT Telegram , ReadDate, SecAddr From Telegrams WHERE idCONfk = " + str(condID) + " AND Units = '" + units +"'   ORDER BY SecAddr DESC "
    print(Query)
    mycursor.execute(Query)
    # + " AND ReadDate ='" + str(today) + "'")
    result = mycursor.fetchall()
    mydb.close()
    csv = ""
    for res in result:
        
        # print(res[1])
        currentrc,lastreadrc,setdayvaluerc,setdayrc = trytoguess(res[0])
        strtl = bytes.fromhex(res[0])
        try:
            tg = meterbus.TelegramLong(strtl)
        except:
            print("Error")
            continue
        dataread = '.'.join(res[1][i:i+4] for i in range(0, len(res[1]), 4))

        csv = csv + str(dataread) + ";"
        a = tg.body.interpreted['header']
        identification = a["identification"]
        identification = identification.replace("0x" , "")
        identification = identification.replace(",","")
        identification =  identification.replace(" ","")

        status = a["status"]
        status = status.replace("0x" , "")
        status = status.replace(",","")
        status =  status.replace(" ","")

        csv = csv + identification + ";" + status  
        
        #print(csv)
        b = tg.body.interpreted["records"]
        """for k in b:
        
            for r in k:
                if k["unit"] in fieldallowd:
                    csv = csv + r + ";"
                    csv = csv + str(k[r]) +";"
        csv = csv + "\n"""
        csv = csv + ";" + str(b[currentrc]["value"]) +";" + str(b[setdayrc]["value"]) + ";" + str(b[setdayvaluerc]["value"]) + ";" + str(b[lastreadrc]["value"]) + "\n"
    return ( csv )

def CurrentDataToCSV(condID,units,readdate):
    import meterbus
    import mysql.connector
    
    fieldallowd = ["MeasureUnit.HCA" , "MeasureUnit.DATE", "MeasureUnit.WH", "MeasureUnit.M3"]
    mydb = mysql.connector.connect(
        host="192.168.88.150",
        user="root",
        password="",
        database="raf_db",
        allow_local_infile=True
    )
    mycursor = mydb.cursor()
    Query = "SELECT Telegram , ReadDate,  SecAddr From Telegrams WHERE idCONfk = " + str(condID) + " AND Units = '" + units +"' AND ReadDate = '" + readdate + "'  ORDER BY SecAddr DESC "
    print(Query)
    mycursor.execute(Query)
    # + " AND ReadDate ='" + str(today) + "'")
    result = mycursor.fetchall()
    mydb.close()
    csv = ""
    for res in result:
        
        # print(res[1])
        currentrc,lastreadrc,setdayvaluerc,setdayrc = trytoguess(res[0])
        strtl = bytes.fromhex(res[0])
        try:
            tg = meterbus.TelegramLong(strtl)
        except:
            print("Error")
            continue
        dataread = '.'.join(res[1][i:i+4] for i in range(0, len(res[1]), 4))

        csv = csv + str(dataread) + ";"
        a = tg.body.interpreted['header']
        identification = a["identification"]
        identification = identification.replace("0x" , "")
        identification = identification.replace(",","")
        identification =  identification.replace(" ","")

        status = a["status"]
        status = status.replace("0x" , "")
        status = status.replace(",","")
        status =  status.replace(" ","")

        csv = csv + identification + ";" + status  
        
        #print(csv)
        b = tg.body.interpreted["records"]
        c=str(b[lastreadrc]["value"]).split("T")
        csv = csv + ";" + str(b[currentrc]["value"]) +";" + str(b[setdayrc]["value"]) + ";" + str(b[setdayvaluerc]["value"]) + ";" + c[0] + "\r"
    return ( csv )

def trytoguess(telegram):
        fieldallowd = ["MeasureUnit.HCA","MeasureUnit.WH","MeasureUnit.M3"]
        strtl = bytes.fromhex(telegram)

           
        tg = meterbus.TelegramLong(strtl)
        count = 0
        lastreadrc = -1
        currentrc  = -1
        setdayrc = -1
        setdayvaluerc = -1

        a = tg.body.interpreted["records"]
        for record in a:
            if  record["type"] == "VIFUnit.DATE_TIME_GENERAL":
                lastreadrc = count
            if record["unit"] in fieldallowd and currentrc == -1:
                currentrc = count
            
            
            if  record["type"] == "VIFUnit.DATE" and setdayrc == -1 :
                setdayrc = count
                if count -1 != currentrc:
                    setdayvaluerc = count -1
                else:
                    setdayvaluerc = count +1
            if lastreadrc != -1 and currentrc != -1 and setdayrc != -1 and setdayvaluerc != -1 :
                return currentrc,lastreadrc,setdayvaluerc,setdayrc

            count = count +1 


        return (2,3 ,2 ,3)

def GetModems_Custom(condid):
    if True:  # codice == DatiAccesso.codiceSessione and dati.controlloAccesso() == True :
        mydb = mysql.connector.connect(
            host="192.168.88.150",
            user="root",
            password="",
            database="raf_db",
            allow_local_infile=True
        )
    mycursor = mydb.cursor()
    Query="SELECT MeterID,MBCurrentValue,MBLastRecived FROM Modems_Custom WHERE idCONfk =  " + str(condid) + ";"
    print(Query)
    mycursor.execute(Query)
    results = mycursor.fetchall()
    mydb.close()
    return results

def SetModems_Custom(condid,content):
    if True:  # codice == DatiAccesso.codiceSessione and dati.controlloAccesso() == True :
        mydb = mysql.connector.connect(
            host="192.168.88.150",
            user="root",
            password="",
            database="raf_db",
            allow_local_infile=True
        )
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM Modems_Custom WHERE idCONfk = " + str(condid))
    mydb.commit()
    print(content)
    lines = content.splitlines()
    for line in lines:
        if ";" in line:
            line=line.rstrip()
            buff = line.split(";")
            mycursor.execute("INSERT INTO Modems_Custom (idCONfk,MeterID,MBCurrentValue,MBLastRecived) VALUES (" + \
                            str(condid)+"," + "'" + str(buff[0]) +"'," + str(buff[1]) + "," +str(buff[2]) + ")")
            mydb.commit()
    return("OK")

def ForceRead(condid):
    from subprocess import call
    try:
        os.mkdir(str(condid))
    except:
        pass
    rc = call("nohup python3 DoReadOOP.py " + str(condid) + " debug 1 1>" + str(condid) + "/" +
                          str(condid) + ".out 2>" + str(condid) + "/" + str(condid) + ".err &", shell=True)

def ForceActions(condid):
    from subprocess import call
    try:
        os.mkdir(str(condid))
    except:
        pass
    rc = call("nohup python3 runOOP.py " + str(condid) + " debug 1 1>" + str(condid) + "/" +
                          str(condid) + ".out 2>" + str(condid) + "/" + str(condid) + ".err &", shell=True)
    print("nohup python3 runOOP.py " + str(condid) + " debug 1 1>" + str(condid) + "/" +
                          str(condid) + ".out 2>" + str(condid) + "/" + str(condid) + ".err &")
    print(rc)

def GetModemsReadingsStats():
    if True:  # codice == DatiAccesso.codiceSessione and dati.controlloAccesso() == True :
        mydb = mysql.connector.connect(
            host="192.168.88.150",
            user="root",
            password="",
            database="raf_db",
            allow_local_infile=True
        )
    mycursor = mydb.cursor()
    Query="SELECT idCONfk,Memo,LastRead,Unreads,LastRecived FROM Modems;"
    print(Query)
    mycursor.execute(Query)
    results = mycursor.fetchall()
    mydb.close()
    return results

class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
        pass

server =  SimpleThreadedXMLRPCServer(("0.0.0.0", 2808),allow_none=True)
print("Listening on port 2808...")

server.register_function(getreading)
server.register_function(getmodemsettings)
server.register_function(pushmodemsettings)
server.register_function(CreateRow)
server.register_function(AllDataToCSV)
server.register_function(GetModems_Custom)
server.register_function(SetModems_Custom)
server.register_function(ForceRead)
server.register_function(ForceActions)
server.register_function(CurrentDataToCSV)
server.register_function(GetModemsReadingsStats)
try:
    print("Usa Control-C per uscire")
    server.serve_forever()
except KeyboardInterrupt:
    print("Sto uscendo...")
except:
    print("Errore non identificato")
