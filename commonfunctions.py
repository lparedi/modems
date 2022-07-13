from ast import Global
#debug =1

from cmath import sin
from distutils.log import debug
import mysql.connector
import http.client
from datetime import date
import os.path
from datetime import datetime
from termcolor import colored
import binascii
import meterbus
import xmlrpc.client
import os
import hashlib
from Config import configuration
from os import walk
from pprint import pprint

conf = configuration



def setlastread(datetoset, condID):
    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )
    if debug == 1:
        print(colored("Set the LastRecived", "red"))
        print(colored(datetoset, "green"))
    mycursor = mydb.cursor()
    mycursor.execute("UPDATE Modems set LastRead = '" + str(datetoset) + "'" + " WHERE idCONfk = " + str(condID))
    mydb.commit()
    mydb.close()


def getlastread(condID):
    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT LastRead From Modems WHERE idCONfk = " + str(condID))
    result = mycursor.fetchone()
    mydb.close()
    if debug == 1:
        print("Numero Modem")
        print(int(result[0]))
    return str(result[0])


def ascii_to_hex(ascii_str):
   
    hex_str = binascii.hexlify(ascii_str.encode())
    return hex_str


def parsearguments(argsvector):
    results = {}
    print(argsvector)
    if len(argsvector) < 2:
        return "TOO FEEW ARGUMENTS", results
    results["syncID"] = argsvector[1]
    if len(argsvector) > 3:
        if argsvector[2] == "debug":
            results["debug"] = argsvector[3]
        if len(argsvector)>4:
            if argsvector[4] == "noread":
                results["noread"] = 1
    return "OK", results


def setlastrecived(condID, timeFromPoc):
    debug =1
    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )
    if debug == 1:
        print(colored("Set the LastRecived", "red"))
        print(colored(timeFromPoc + "->" + str(condID), "green"))
    mycursor = mydb.cursor()
    mycursor.execute("UPDATE Modems set LastRecived = '" +
                     timeFromPoc + "'" + " WHERE idCONfk = " + str(condID))
    mydb.commit()
    if "," in timeFromPoc:
        buff = timeFromPoc.split(",")
        ct =buff[0].split("T")
        mycursor.execute("UPDATE Modems set FirstWakeUpTime = '" + ct[1][:4] + "'" + " WHERE idCONfk = " + str(condID))
        mydb.commit()
    mydb.close()


def getactions(condID):
    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT  * From Modems   WHERE idCONfk = " + str(condID))
    result = mycursor.fetchall()
    mydb.close()
    # print(result)
    actions = {}
    index = 0
    for columnames in mycursor.description:
        actions[columnames[0]] = result[0][index]
        index += 1
    return actions


def getmeterslist(condID , readrnn,readenergy,readwater):
    result = {}
    meterlist = {}
    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )
    
    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT Ripartitore,idCONfk From elementi  WHERE idCONfk = " + str(condID))
    
    resulthca = mycursor.fetchall()
    result.update(resulthca)
    if readrnn == 1:
        mycursor.execute("SELECT CAST( Seriale as UNSIGNED ),idCONfk From antenne  WHERE idCONfk = " + str(condID))
        resultrnn = mycursor.fetchall()
        result.update(resultrnn)
        
                
    if readenergy == 1:
        mycursor.execute("SELECT  CAST(SerialeE as UNSIGNED),idCONfk From energia  WHERE idCONfk = " + str(condID))
        resultrnn = mycursor.fetchall()
        result.update(resultrnn)
    if readwater == 1:
        mycursor.execute("SELECT CAST(Seriale as UNSIGNED),idCONfk From acqua  WHERE idCONfk = " + str(condID))
        resultrnn = mycursor.fetchall()
        result.update(resultrnn)
    mydb.close()
    #print("**********************")
    print(result)
    
    return result


def getmodemnumber(condID):
    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )
    mycursor = mydb.cursor()
    if int(condID) < 100000000:
        mycursor.execute("SELECT NumeroModem From condomini WHERE idCONpk = " + str(condID))
    else:
        mycursor.execute("SELECT Numero From Modems WHERE idCONfk = " + str(condID))
    
    result = mycursor.fetchone()
    mydb.close()
    if debug == 1:
        print("Numero Modem")
        print(int(result[0]))
    return int(result[0])



def ans(number):
    conn = http.client.HTTPSConnection("olivettiiot.tim.it")
    payload = ''
    headers = {
        'X-M2M-RI': 'CIN_1616163460',
        'X-M2M-Origin': 'CCEDB769A-ad46824a',
        'Content-Type': 'application/vnd.onem2m-res+json',
        'Accept': 'application/vnd.onem2m-res+json',
        'Authorization': 'Q0NFREI3NjlBLWFkNDY4MjRhOjVlNjNjYWI5OTdjZDQ2MjNhYzBkMTU5N2I4MWM3MzRl'
    }
    conn.request("GET", "/onem2m/" + str(number) + "/nbiot/inbox/la", payload, headers)
    res = conn.getresponse()
    data = res.read()
    try:
        buff = data.decode("utf-8").split("\"lt\"")
        buff1 = buff[1].split("\",\"")
        buff[1] = buff1[0].replace(":\"", "")

        if debug == 1:
            print("time")
            print(buff[1].replace(" ", ""))
        rtime = buff[1].replace(" ", "")

        buff = data.decode("utf-8").split("\"rn\"")
        buff1 = buff[1].split("\",\"")
        buff[1] = buff1[0].replace(":\"", "")

        if debug == 1:
            print("rn")
            print(buff[1].replace(" ", ""))
        rn = buff[1].replace(" ", "")

        buff = data.decode("utf-8").split("con")
        buff[1] = buff[1].replace("\"", "")
        buff[1] = buff[1].replace(":", "")
        buff[1] = buff[1].replace("}}", "")
        s = buff[1]
        buff[1] = " ".join(s[i:i + 2] for i in range(0, len(s), 2))
        if debug == 1:
            print("con")
            print(buff[1].replace(" ", ""))
        con = buff[1].replace(" ", "")
    except:
        con =""
        rn= ""
        rtime = ""
    conn.close()
    return con, rn, rtime 


 


def setunreads(count, condID):
    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )
    if debug == 1:
        print(colored("Set the Unreads", "red"))
        print(colored(str(count), "green"))
    mycursor = mydb.cursor()
    mycursor.execute("UPDATE Modems set Unreads = '" + str(count) + "'" + " WHERE idCONfk = " + str(condID))
    mydb.commit()
    mydb.close()


def setreadstatus(count, condID, Force=False):
    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )
    if debug == 1:
        print(colored("Set the ReadStatus", "red"))
        print(colored(str(count), "green"))
    mycursor = mydb.cursor()
    if count == 0 or Force:
        mycursor.execute("UPDATE Modems set LastReadStatus = 'OK'" + " WHERE idCONfk = " + str(condID))
    else:
        mycursor.execute("UPDATE Modems set LastReadStatus = 'KO'" + " WHERE idCONfk = " + str(condID))
    mydb.commit()
    mydb.close()


def setdoto(todo, condID):
    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )
    if debug == 1:
        print(colored("Set the ToDo", "red"))
        print(colored(str(todo), "green"))
    mycursor = mydb.cursor()
    mycursor.execute("UPDATE Modems set ToDo = " + str(todo) + " WHERE idCONfk = " + str(condID))
    mydb.commit()
    mydb.close()


def setactive(active, condID):
    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )
    mycursor = mydb.cursor(buffered=True)
    if active:
        mycursor.execute("UPDATE Modems set Active = 1  WHERE idCONfk = " + str(condID))
    else:
        mycursor.execute("UPDATE Modems set Active = 0  WHERE idCONfk = " + str(condID))
    mydb.commit()


def checkifistime(condID):
    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )

    mycursor = mydb.cursor(buffered=True)
    if debug == 1:
        print("SELECT Active From Modems  WHERE idCONfk = " + str(condID))
    mycursor.execute("SELECT Active From Modems  WHERE idCONfk = " + str(condID))
    result = mycursor.fetchone()
    if debug == 1:
        print(colored("Active:" + str(result[0]), "red"))
    if str(result[0]) == "1":
        return False

    if debug == 1:
        print("SELECT ForceIfIsTime From Modems  WHERE idCONfk = " + str(condID))
    mycursor.execute("SELECT ForceIfIsTime From Modems  WHERE idCONfk = " + str(condID))
    result = mycursor.fetchone()
    if debug == 1:
        print(colored("Force:" + str(result[0]), "red"))
    if str(result[0]) == "1":
        return True

    mycursor.execute("SELECT LastRecived From Modems  WHERE idCONfk = " + str(condID))
    result = mycursor.fetchone()
    if debug == 1:
        print(colored("LastRecived:" + str(result[0]), "red"))
    buff = str(result[0]).split(",")
    lastrecived = buff[0].split("T")
    today = datetime.now().strftime("%Y%m%d")
    localnow = datetime.now().strftime("%H%M")

    mycursor.execute("SELECT Recursion From Modems  WHERE idCONfk = " + str(condID))
    recursion = mycursor.fetchone()

    mycursor.execute("SELECT FirstWakeUpTime From Modems  WHERE idCONfk = " + str(condID))
    wt = mycursor.fetchone()

    mydb.close()

    if debug == 1:
        print(colored("Recursion:" + str(recursion[0]), "red"))
    # hours = int(str(result[0]))
    # days = hours // 24
    deltam = int(today) - int(lastrecived[0]) + int(recursion[0])
    if debug == 1:

        print(today)
        print(lastrecived[0])
        print("deltam: " + str(deltam))

    if deltam == 0:
        if debug == 1:
            print(wt[0])
            print(localnow)
            print("dw: " + str(int(wt[0]) - int(localnow)))
        dw = int(wt[0]) - int(localnow)
        if dw in range(0, 5):
            return True
        else:
            return False
    else:
        return False


def getcondids():
    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT idCONfk From Modems  WHERE Disabled = 0 ")
    result = mycursor.fetchall()
    return result


def getreadingdate(condID):
    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT ReadingDate From Modems  WHERE idCONfk = " + str(condID))
    result = mycursor.fetchone()
    return result[0]


def setalllastrecived():
    condids = getcondids()
    for cond in condids:
        modemnumber = getmodemnumber(cond[0])
        acon, arn, firstatime = ans(modemnumber)
        setlastrecived(cond[0], firstatime)

def setalllastrecivednoread():
    condids = getcondids()
    for cond in condids:
        modemnumber = getmodemnumber(cond[0])
        firstatime = ansnoread(modemnumber)
        setlastrecived(cond[0], firstatime)

def setpid(pid, condID):
    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )
    if debug == 1:
        print(colored("Set the pid", "red"))
        print(colored(pid, "green"))
    mycursor = mydb.cursor()
    mycursor.execute("UPDATE Modems set pid = " + str(pid) + "" + " WHERE idCONfk = " + str(condID))
    mydb.commit()
    mydb.close()


def createmeterslistfile(meterslist, condID, customlist):
    today = date.today().strftime("%Y%m%d")
    prefix = "###AT+WRSN="
    buff = ""
    counter = 0
    fcount = 0
    status = "KO"
    MbusDict = {}

    for rip in meterslist.keys():

        counter = counter + 1
        if customlist == 1:
            buff = buff + "-" + str(rip).rstrip()
        else:
            buff = buff + "-" + str(rip).rstrip()
        if counter % 10 == 0:
            if os.path.exists(condID + "/LIST/CURRENT/" + str(fcount + 1) + ".hex"):
                for fin in open(condID + "/LIST/CURRENT/" + str(fcount + 1) + ".hex", "r"):
                    hexstring = ascii_to_hex(prefix + str(counter) + "," + str(fcount * 10 + 1) + buff + ";").decode("utf-8")
                    # hexstring = ascii_to_hex(prefix + str(counter) + buff + ";").decode("utf-8")
                    if debug == 1:
                        print("********* METERS ALREADY PRESENT *********")
                        print(prefix + str(counter) + "-" + str(fcount * 10 + 1) + buff + ";")
                        print(hexstring)
                    if hexstring != fin:
                        MbusDict[str(fcount + 1)] = hexstring
                        status = "OK"
                    else:
                        pass

            else:
                hexstring = ascii_to_hex(prefix + str(counter) + "," + str(fcount * 10 + 1) + buff + ";").decode("utf-8")
                # hexstring = ascii_to_hex(prefix + str(counter) +  buff + ";").decode("utf-8")
                if debug == 1:
                    print("********* METERS CREATED *********")
                    print(prefix + str(counter) + "," + str(fcount * 10 + 1) + buff + ";")
                    print(hexstring)
                MbusDict[str(fcount+1)] = hexstring
                status = "OK"
            buff = ""
            counter = 0
            fcount = fcount + 1

    if len(buff) != 0:
        if os.path.exists(condID + "/LIST/CURRENT/" + str(fcount + 1) + ".hex"):
            for fin in open(condID + "/LIST/CURRENT/" + str(fcount + 1) + ".hex", "r"):
                hexstring = ascii_to_hex(prefix + str(counter) + "," + str(fcount * 10 + 1) + buff + ";").decode("utf-8")
                # hexstring = ascii_to_hex(prefix + str(counter) +  buff + ";").decode("utf-8")
                if debug == 1:
                    print("********* METERS *********")
                    print(prefix + str(counter) + buff + ";")
                    print(hexstring)
                if hexstring != fin:
                    MbusDict[str(fcount+1)] = hexstring
                    status = "OK"
                else:
                    pass
        else:
            hexstring = ascii_to_hex(prefix + str(counter) + "," + str(fcount * 10 + 1) + buff + ";").decode("utf-8")
            # hexstring = ascii_to_hex(prefix + str(counter)   + buff + ";").decode("utf-8")
            if debug == 1:
                print("********* METERS CREATED *********")
                # print(prefix + str(counter) + "," + str(fcount * 10 + 1) + buff + ";")
                print(prefix + str(counter) + buff + ";")
                print(hexstring)
            MbusDict[str(fcount+1)] = hexstring
            status = "OK"

    for singles in MbusDict:
        hexout = open(condID + "/LIST/CURRENT/" + str(singles) + ".hex", "w")
        hexout.write(MbusDict[singles])
        if debug == 1:
            print("******** FILE WRITTEN *********")
            print(singles + " " + MbusDict[singles])
        hexout.close()
    return status, MbusDict

def createmeterslistdb(meterslist,condID,customlist):
    debug =1
    today = date.today().strftime("%Y%m%d")
    prefix = "###AT+WRSN="
    buff = ""
    counter = 0
    fcount = 0
    status = "KO"
    MbusDict = {}

    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT ReadingDate From Modems  WHERE idCONfk = " + str(condID))
    result = mycursor.fetchone()
    
    mycursor.execute("SELECT Indexl, MetersString From Modems_CurrentMeters  WHERE idCONfk = " + str(condID))
    result = mycursor.fetchall()
    mycursor.execute("SELECT Indexl From Modems_CurrentMeters  WHERE idCONfk = " + str(condID))
    resultindex = mycursor.fetchall()
   
    for rip in meterslist.keys():
        rips = str(rip)
        if len(rips) < 8:
            rips= "0" + rips
        counter = counter + 1
        if customlist == 1:
            buff = buff + "-" + str(rips).rstrip()
        else:
            buff = buff + "-" + str(rips).rstrip()
        if counter % 10 == 0:
            
            
            if (int(fcount +1),) in resultindex:
                mycursor.execute("SELECT MetersString From Modems_CurrentMeters  WHERE Indexl = " + str(fcount +1) + " AND  idCONfk = " + str(condID))
                resultstr = mycursor.fetchone()
                hexstring = ascii_to_hex(prefix + str(counter) + "," + str(fcount * 10 + 1) + buff + ";").decode("utf-8")
                # hexstring = ascii_to_hex(prefix + str(counter) + buff + ";").decode("utf-8")
                
                
                if hexstring != resultstr[0]:
                    MbusDict[str(fcount + 1)] = hexstring
                    status = "OK"
                    print("**** METERS UPDATED ******")
                    print(hexstring + " - " + resultstr[0] )
                else:
                    pass

            else:
                hexstring = ascii_to_hex(prefix + str(counter) + "," + str(fcount * 10 + 1) + buff + ";").decode("utf-8")
                # hexstring = ascii_to_hex(prefix + str(counter) +  buff + ";").decode("utf-8")
                if debug == 1:
                    print("********* METERS CREATED *********")
                    print(prefix + str(counter) + "," + str(fcount * 10 + 1) + buff + ";")
                    print(hexstring)
                MbusDict[str(fcount+1)] = hexstring
                status = "OK"
            buff = ""
            counter = 0
            fcount = fcount + 1

    if len(buff) != 0:
        if  (int(fcount +1),) in resultindex:
            mycursor.execute("SELECT MetersString From Modems_CurrentMeters  WHERE Indexl = " + str(fcount +1) + " AND  idCONfk = " + str(condID))
            resultstr = mycursor.fetchone()
            hexstring = ascii_to_hex(prefix + str(counter) + "," + str(fcount * 10 + 1) + buff + ";").decode("utf-8")
            # hexstring = ascii_to_hex(prefix + str(counter) +  buff + ";").decode("utf-8")
            
            if hexstring != resultstr[0]:
                if debug ==1:
                    print("********* METERS UPDATED *********")
                    print(prefix + str(counter) + "," + str(fcount * 10 + 1) + buff + ";")
                    print(hexstring)
                MbusDict[str(fcount+1)] = hexstring
                status = "OK"
            else:
                pass
        else:
            hexstring = ascii_to_hex(prefix + str(counter) + "," + str(fcount * 10 + 1) + buff + ";").decode("utf-8")
            # hexstring = ascii_to_hex(prefix + str(counter)   + buff + ";").decode("utf-8")
            if debug == 1:
                print("********* METERS CREATED *********")
                # print(prefix + str(counter) + "," + str(fcount * 10 + 1) + buff + ";")
                print(prefix + str(counter) + buff + ";")
                print(hexstring)
            MbusDict[str(fcount+1)] = hexstring
            status = "OK"

    for singles in MbusDict:
        a=int(singles)
       
        if (a,) in resultindex:
            mycursor.execute("UPDATE Modems_CurrentMeters SET MetersString ='"  + MbusDict[singles]  +"'   WHERE Indexl = " + str(singles) + " AND  idCONfk = " + str(condID))
            #print("UPDATE Modems_CurrentMeters SET MetersString ='"  + MbusDict[singles]  +"'   WHERE Indexl = " + str(fcount +1) + " AND  idCONfk = " + str(condID))
            mydb.commit()
            if debug == 1:
                print("******** DATABASE UPDATED *********")
                print(singles + " " + MbusDict[singles])
        else:
            mycursor.execute("INSERT INTO   Modems_CurrentMeters (MetersString,Indexl,idCONfk) VALUES( '"  + MbusDict[singles]  +"'," + str(singles) +"," + str(condID) + ")")
            mydb.commit()
            if debug == 1:
                print("******** DATABASE INSERTER *********")
                print(singles + " " + MbusDict[singles])

    return status, MbusDict

""" def sendprecomputed(telegram, number):
    conn = http.client.HTTPSConnection("olivettiiot.tim.it")
    payload = "{\n  \"m2m:cin\": {\n\t\"lbl\": [ \"proto:udp\", \"port:5685\" ],\n    \"cnf\": \"text/plain:0\",\n    \"con\": \"" + telegram + "\"\n  }\n}"
    headers = {
        'X-M2M-RI': 'CIN_1631194038',
        'X-M2M-Origin': 'CCEDB769A-ad46824a',
        'Content-Type': 'application/vnd.onem2m-res+json;ty=4',
        'Accept': 'application/vnd.onem2m-res+json',
        'Authorization': 'Q0NFREI3NjlBLWFkNDY4MjRhOjVlNjNjYWI5OTdjZDQ2MjNhYzBkMTU5N2I4MWM3MzRl'
    }
    conn.request("POST", "/onem2m/" + str(number) + "/nbiot/outbox", payload, headers)
    res = conn.getresponse()
    data = res.read()
    # print(payload + "\n" + payload1 )
    if debug == 1:
        print("SEL")
        print(data.decode("utf-8"))
 """

# def computetelegram(ttype, mid="-1"):
#     if mid == '-1':
#         if ttype == "REQ_UD2_FD":
#             return "105bFD5816"
#         if ttype == "SND_NKE":
#             return "1040004016"
#         if ttype == "REQ_UD2_00":
#             return "105b005b16"
#         if ttype == "SELECT_STD":
#             return "6804046853FD5010B016"
#
#     idreversed = str(mid)
#     if int(mid) > 255:
#
#         if ttype == "SELECT_FD":
#             prefix = "680B0B6873FD52"
#             meterid = ""
#             for i in range(8, 0, -2):
#                 # print ( i )
#                 # print (idreversed[i -2 :i])
#                 idrev = idreversed[i - 2:i]
#                 meterid = meterid + idrev
#             if debug == 1:
#                 print(idreversed + " -> " + meterid)
#
#             Telegram = prefix + meterid + "FFFFFFFF" + "XX" + "16"
#             checksum = mbcheksum(Telegram)
#             Telegram = Telegram.replace("XX", checksum)
#             if debug == 1:
#                 print(Telegram)
#             return Telegram.upper()


def getcustommeterlist(RealEstates, append,overwritecondid,readrnn,readenergy,readwater):
    meters = {}
    meterlist = {}
   
    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )


   

    for re in RealEstates:
        if append == 1:
            meterlist.update(getmeterslist(re,readrnn,readenergy,readwater))

        meters.update(meterlist)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT MeterID,idCONfk  From Modems_Custom   WHERE idCONfk = " + str(re))
        result = mycursor.fetchall()
        
       

        for meter in result:
            if not int(meter[0]) in meterlist:
                if str(overwritecondid) == "0":
                    meterlist[int(meter[0])] = int(meter[1])
                else:
                    meterlist[int(meter[0])] = int(overwritecondid)

    #print(meters)
    mydb.close()
    return meterlist


def cretamixedrecordsdict(realestates):
    dictres =  {}
    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )

    mycursor = mydb.cursor()
    for  condid in realestates:
        mycursor.execute("SELECT MeterID,MBCurrentValue  From Modems_Custom  WHERE (MBCurrentValue is not NULL) AND  idCONfk = " + str(condid))
        result = mycursor.fetchall()
    
    
        dictres.update(result)
    
  
    return dictres
    
def cretalastrecordsdict(realestates):
    dictres =  {}
    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )

    mycursor = mydb.cursor()
    for condid in realestates:
        mycursor.execute("SELECT MeterID,MBLastRecived  From Modems_Custom  WHERE (MBLastRecived is not NULL) AND  idCONfk = " + str(condid))
        result = mycursor.fetchall()
        dictres.update(result)
    
    
   
    print(dictres)
  
    return dictres

def filetodic(filepath):
    result = {}
    fin = open(filepath)
    for line in fin:
        key, value = line.split(",")
        result[key] = value.rstrip()
    fin.close()
    return result


def extractmeterfromtelegram(telegram):
    if debug == 1:  # and False:
        print(telegram)
    idreversed = telegram[14:22]
    # if debug == 1:
    # print ( "Id reversed " + idreversed)
    meterid = ""
    for i in range(8, 0, -2):
        # print ( i )
        # print (idreversed[i -2 :i])
        idrev = idreversed[i - 2:i]
        meterid = meterid + idrev
       
    return meterid


def TelegramToSql(meterlists, telegrams, ReadDate, RecorNumber, mixedrecords, mixedrecordsdict, pymbus, Mbresults=[]):
    debug =1
    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )
    
    mycursor = mydb.cursor(buffered=True)
    if pymbus == 0:
        for telegram in telegrams:

            meter = extractmeterfromtelegram(telegram)
            if meter not in meterlists:
                continue
            condid = meterlists[int(meter)]
            sql = """ INSERT INTO Telegrams (idCONfk, SecAddr , Telegram, ReadDate) 
        SELECT """ + str(condid) + """, """ + str(meter) + """, '""" + telegram + """','""" + ReadDate + """' FROM DUAL 
        WHERE NOT EXISTS (SELECT idCONfk FROM Telegrams WHERE idCONfk = """ + str(condid) + """ AND 
        SecAddr =""" + str(meter) + """ AND ReadDate = '""" + ReadDate + """'
               LIMIT 1) """
            mycursor.execute(sql)
            mydb.commit()
        mydb.close()

    else:

        for result, telegram in zip(Mbresults, telegrams):
            
            
            if int(result["ID"]) in meterlists.keys():
                condid = meterlists[int(result["ID"])]
               
            else:
                continue

            sql = """ INSERT INTO Telegrams (idCONfk, SecAddr , Telegram, ReadDate,Status,Value,Units,LastRecived , SetDayValue , SetDay) 
                SELECT """ + str(condid) + """, """ + str(result["ID"]) + """, '""" + telegram + """','""" + ReadDate + """',
            '""" + str(result["Status"]) + """','""" + str(result["CurrentValue"]) + """','""" + str(result["Units"])+ """','""" + str(result["LastRecived"])+  """','""" + str(result["SetDayValue"]) +  """','""" + str(result["SetDay"]) +  """'
            FROM DUAL 
                WHERE NOT EXISTS (SELECT idCONfk FROM Telegrams WHERE idCONfk = """ + str(condid) + """ AND 
                SecAddr =""" + str(result["ID"]) + """ AND ReadDate = '""" + ReadDate + """'
                       LIMIT 1) """
            if debug == 1:
                print(colored(sql, "green"))
            mycursor.execute(sql)
            mydb.commit()
    mydb.close()


def getmetersreaded(RealEstates, readdate,overwritecondid):
    debug = 1
    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )
    results = []
    mycursor = mydb.cursor(buffered=True)
    
    for condid in RealEstates:

        if int(overwritecondid) != 0 :
            condid = overwritecondid

        sql = "Select SecAddr FROM Telegrams WHERE  idCONfk = " + str(condid) + " AND  ReadDate LIKE '" + readdate + "%'"
        if debug == 1:
            print(colored(sql, "green"))
        mycursor.execute(sql)
        mydb.commit()
        resultsr = mycursor.fetchall()
        
        for meter in resultsr:
            results.append(str(meter[0]))
    mydb.close()
    #exit(0)
    return results


def getrealestates(condID, relist="0"):
    revect = []
    if relist != "0":
        revect = relist.split(",")
    revect.append(condID)
    return revect


def listtodict(list):
    resdict = {}
    for element in list:
        resdict[element[0]] = element[1]
    return resdict


def richiestaCred():
    usernameStringa = "admin"
    passwordStringa = "password"

    usernameStringa = hashlib.md5(usernameStringa.encode('UTF-8'))
    passwordStringa = hashlib.md5(passwordStringa.encode('UTF-8'))

    usernameMd5 = usernameStringa.hexdigest()
    passwordMd5 = passwordStringa.hexdigest()
    credenziali = (usernameMd5, passwordMd5)
    return credenziali


def PymBusToLetture(condID, xml, readdate, unit):

    Proxy = "http://192.168.88.150:2908/"
    server = xmlrpc.client.ServerProxy(Proxy, encoding='utf-8', verbose=False)

    credenziali = richiestaCred()
    usernameMd5 = credenziali[0]
    passwordMd5 = credenziali[1]

    accesso = server.accesso(usernameMd5, passwordMd5)
    if int(condID) > 100000000:
            condID = str(int(condID) - 100000000)
    ok, codiceSessione = server.init(condID)
  
    # print("Sessione " + str(ok))
    if ok:


        if unit == "MeasureUnit.HCA":

            fileNoExt = "lettura"

            contenuto_file = xml
            server.pushNewFiles(str(codiceSessione), fileNoExt, contenuto_file)
            ok, messaggio = server.ins_data_db_letture(int(codiceSessione))
            OK = server.set_datalettura(codiceSessione, readdate)
        if unit == "MeasureUnit.M3":
            fileNoExt = "letturaacqua"

            contenuto_file = xml
            server.pushNewFiles(str(codiceSessione), fileNoExt, contenuto_file)

            ok, messaggio = server.ins_data_db_lettura_acqua(int(codiceSessione))
            OK = server.set_datalettura_acqua(codiceSessione, readdate)

        if unit == "MeasureUnit.WH":
            fileNoExt = "letturaenergia"

            contenuto_file = xml
            server.pushNewFiles(str(codiceSessione), fileNoExt, contenuto_file)

            ok, messaggio = server.ins_data_db_lettura_energia(int(codiceSessione))
            OK = server.set_datalettura_energia(codiceSessione, readdate)

        server.quit(codiceSessione)


def PymBusToLetture_modem(condID, xml, readdate, unit):

    Proxy = "http://192.168.88.150:2908/"
    server = xmlrpc.client.ServerProxy(Proxy, encoding='utf-8', verbose=False)

    credenziali = richiestaCred()
    usernameMd5 = credenziali[0]
    passwordMd5 = credenziali[1]

    #accesso = server.accesso(usernameMd5, passwordMd5)
    if int(condID) > 100000000:
            condID = str(int(condID) - 100000000)
    ok, codiceSessione = server.init(str(condID),usernameMd5,passwordMd5)
    #print("Sessione " + str(codiceSessione))
    #print(ok)
    if ok:

        if unit == "MeasureUnit.HCA":

            fileNoExt = "lettura"

            contenuto_file = xml
            server.pushNewFiles(str(codiceSessione), fileNoExt, contenuto_file)

            ok, messaggio = server.ins_data_db_letture_modem(int(codiceSessione))
            OK = server.set_datalettura(codiceSessione, readdate)
        if unit == "MeasureUnit.M3":
            fileNoExt = "letturaacqua"

            contenuto_file = xml
            server.pushNewFiles(str(codiceSessione), fileNoExt, contenuto_file)

            ok, messaggio = server.ins_data_db_lettura_acqua_modem(int(codiceSessione))
            OK = server.set_datalettura_acqua(codiceSessione, readdate)
        if unit == "MeasureUnit.WH":
            fileNoExt = "letturaenergia"

            contenuto_file = xml
            server.pushNewFiles(str(codiceSessione), fileNoExt, contenuto_file)

            ok, messaggio = server.ins_data_db_lettura_energia_modem(int(codiceSessione))
            OK = server.set_datalettura_energia(codiceSessione, readdate)

        server.quit(codiceSessione)


def createxmlletture(condID, readdate, units ):

    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<dataroot xmlns:od="urn:schemas-microsoft-com:officedata" generated="2021-10-08T17:50:26">"""

    mycursor = mydb.cursor(buffered=True)
    
    sql = "Select * FROM Telegrams WHERE  idCONfk = " + str(condID) + " AND  ReadDate ='" + readdate + "'  And Units = '" + units + "'"
    if debug == 1:
        print(colored(sql, "green"))
    mycursor.execute(sql)
    mydb.commit()
    resultsr = mycursor.fetchall()
    if len(resultsr) > 0:
        for meter in resultsr:
            xml = xml + "<lettura>\n"
            xml = xml + "<CenKVal102>" + str(meter[5]) + "</CenKVal102>\n"
            xml = xml + "<KKunderNr101>" + str(meter[1]) + "</KKunderNr101>\n"
            xml = xml + "<SFehler250>" + str(meter[4]) + "</SFehler250>\n"
            xml = xml + "</lettura>\n"

        xml = xml + "</dataroot>"
    else:
        xml = ""
    mydb.close()
    return xml


def createxmlletture_acqua(condID, readdate, units):

    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<dataroot xmlns:od="urn:schemas-microsoft-com:officedata" generated="2021-10-08T17:50:26">"""

    mycursor = mydb.cursor(buffered=True)
    sql = "Select * FROM Telegrams WHERE  idCONfk = " + str(condID) + " AND  ReadDate ='" + readdate + "'  And Units = '" + units + "'"
    if debug == 1:
        print(colored(sql, "green"))
    mycursor.execute(sql)
    mydb.commit()
    resultsr = mycursor.fetchall()
    if len(resultsr) > 0:
        for meter in resultsr:
            xml = xml + "<letturaacqua>\n"
            xml = xml + "<F1>" + str(meter[1]) + "</F1>\n"
            xml = xml + "<F2>" + str(round(float(meter[5]), 3)) + "</F2>\n"
            xml = xml + "<F3>" + str(meter[4]) + "</F3>\n"
            xml = xml + "</letturaacqua>\n"

        xml = xml + "</dataroot>"
    else:
        xml = ""
    mydb.close()
    return xml


def createxmlletture_energia(condID, readdate, units):

    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<dataroot xmlns:od="urn:schemas-microsoft-com:officedata" generated="2021-10-08T17:50:26">"""

    mycursor = mydb.cursor(buffered=True)
    sql = "Select * FROM Telegrams WHERE  idCONfk = " + str(condID) + " AND  ReadDate ='" + readdate + "'  And Units = '" + units + "'"
    if debug == 1:
        print(colored(sql, "green"))
    mycursor.execute(sql)
    mydb.commit()
    resultsr = mycursor.fetchall()
    if len(resultsr) > 0:
        for meter in resultsr:
            xml = xml + "<letturaenergia>\n"
            xml = xml + "<F1>" + str(meter[1]) + "</F1>\n"
            xml = xml + "<F2>" + str(int(meter[5]) /1000) + "</F2>\n"
            xml = xml + "<F3>" + str(meter[4]) + "</F3>\n"
            xml = xml + "</letturaenergia>\n"

        xml = xml + "</dataroot>"
    else:
        xml = ""
    mydb.close()
    return xml


def cretecsv(condID, today):

    csv = ""

    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT Telegram From Telegrams WHERE idCONfk = " + str(condID) + " AND ReadDate ='" + str(today) + "'")
    result = mycursor.fetchall()
    mydb.close()
    for res in result:
        strtl = bytes.fromhex(res[0])
        try:
            tg = meterbus.TelegramLong(strtl)
        except:
            print("Error")
            pass
        ID = str(tg.body.interpreted['header']['identification'])
        ID = ID.replace(",", "")
        ID = ID.replace("0x", "")
        ID = ID.replace(" ", "")
        csv = csv + ID + ";"
        Status = str(int(tg.body.interpreted["header"]["status"], 16))
        csv = csv + Status + ";"
        CurrentValue = str(tg.body.interpreted["records"][2]["value"])
        csv = csv + CurrentValue + ";"
        Units = str(tg.body.interpreted["records"][2]["unit"])
        csv = csv + Units + ";"
        SetDay = str(tg.body.interpreted["records"][3]["value"])
        csv = csv + SetDay + ";"
        ValueAtSetday = str(tg.body.interpreted["records"][4]["value"])
        csv = csv + ValueAtSetday + ";"
        LastRecived = str(tg.body.interpreted["records"][6]["value"])
        csv = csv + LastRecived + "\n"
        return csv


def getallfileds():
    debug = 1
    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )

    mycursor = mydb.cursor(buffered=True)
    sql = "Select  idCONfk , Active,ForceIfIsTime,LastRecived,Recursion,FirstWakeUpTime,Disabled  FROM Modems "
    if debug == 1:
        print(colored(sql, "green"))
    mycursor.execute(sql)
    results = mycursor.fetchall()
    mydb.close()
    return results


def checkifistime_allfields(Active, ForceIfIsTime, LastRecived, Recursion, FirstWakeUpTime):
    debug = 1
    if debug == 1:
        print(colored("Active:" + str(Active), "red"))
    if str(Active) == "1":
        return False

    if debug == 1:
        print(colored("Force:" + str(ForceIfIsTime), "red"))
    if str(ForceIfIsTime) == "1":
        return True

    buff = str(LastRecived).split(",")
    lastrecived = buff[0].split("T")
    today = datetime.now().strftime("%Y%m%d")
    localnow = datetime.now().strftime("%H%M")

    recursion = Recursion

    wt = FirstWakeUpTime

    if debug == 1:
        print(colored("Recursion:" + str(recursion), "red"))
    # hours = int(str(result[0]))
    # days = hours // 24
    try:
        deltam = int(today) - int(lastrecived[0])
    except:
        return False
    if debug == 1:

        print(today)
        print(lastrecived[0])
        print("deltam: " + str(deltam))

    if deltam == int(recursion):
        if debug == 1:
            print(wt)
            print(localnow)
            print("dw: " + str(int(wt) - int(localnow)))
        dw = int(wt) - int(localnow)
        if dw in range(0, 4):
            return True
        else:
            return False
    else:
        return False

def ansnoread(modemnumber, nrecords=999):
    import http.client

    rescue = ""
    rescuereversed = ""

    conn = http.client.HTTPSConnection("olivettiiot.tim.it")
    #conn = http.client.HTTPSConnection(self.RestServer)
    payload = ''
    headers = {
        'X-M2M-RI': 'CIN_1616163460',
        'X-M2M-Origin': 'CCEDB769A-ad46824a',
        'Content-Type': 'application/vnd.onem2m-res+json',
        'Accept': 'application/vnd.onem2m-res+json',
        'Authorization': 'Q0NFREI3NjlBLWFkNDY4MjRhOjVlNjNjYWI5OTdjZDQ2MjNhYzBkMTU5N2I4MWM3MzRl'
    }
    conn.request("GET", "/onem2m/" + str(modemnumber) + "/nbiot/inbox?fu=2&ty=4&lim=" + str(nrecords), payload, headers)
    res = conn.getresponse()
    data = res.read()
    datastr = data.decode("utf-8")
    databuff = datastr.split("}},")
    print(len(databuff))
    #print(databuff)
    
    if len(databuff) > 1:
        for lbuff in databuff:
            buff = lbuff.split("con")
            buff[1] = buff[1].replace("\"", "")
            buff[1] = buff[1].replace(":", "")
            buff[1] = buff[1].replace("}}", "")
            buff[1] = buff[1].replace("]", "")
            ct1 = lbuff.split("\"ct\":\"")
            ct = ct1[1].split(",")
            # print(ct[0])
            s = buff[1]
            buff[1] = " ".join(s[i:i + 2] for i in range(0, len(s), 2))
            # print(buff[1])
            # print (buff[1].replace(" ","")[0:20] + "-----" + line[14:22])
            
            if "524541445920544f20524551554553" in s:
                conn.close()
                return ct[0].replace("T"," : ")
    
    conn.close()
    return ""
def getmodemtype ( condid):

    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )

    mycursor = mydb.cursor(buffered=True)
    sql = "Select  Tipomodem   FROM condomini WHERE idconpk = " + str(condid)
    if debug == 1:
        print(colored(sql, "green"))
    mycursor.execute(sql)
    results = mycursor.fetchall()
    mydb.close()
    return results
    
def getinifilepath(condid):
    base = "646/"
    results = []
    today  = str(date.today().strftime("%Y")) + "-" + date.today().strftime("%m") 
    #today = "2022-06"
    condifl = getsontexmodemdir(condid)

    condidf = condifl[0][0]
    for (dirpath, dirnames, filenames) in walk("./" +base + "/" + condidf):
        for fname in filenames:
            if ".ini" not in fname:
                continue
            if today in fname:
                results.append("./" + base + "/" + condidf + "/" + fname)

            
    return (results)

def getfilespath(base):
    results = []
    for (dirpath, dirnames, filenames) in walk(base):
        for fname in filenames:
            
            results.append( base + "/" + fname)
    return (results)
  
  
def getsontexmeterstype(condid):
    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )

    mycursor = mydb.cursor(buffered=True)
    sql = "Select  MarcaripartitoriInstallati , _x0035_66   FROM condomini WHERE idconpk = " + str(condid)
    if debug == 1:
        print(colored(sql, "green"))
    mycursor.execute(sql)
    results = mycursor.fetchall()
    mydb.close()
    return results

def getsontexaeskey(condid):
    mydb = mysql.connector.connect(
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )

    mycursor = mydb.cursor(buffered=True)
    sql = "Select  AES   FROM condomini WHERE idconpk = " + str(condid)
    if debug == 1:
        print(colored(sql, "green"))
    mycursor.execute(sql)
    results = mycursor.fetchall()
    mydb.close()
    return results

def getsontexmodemdir(condid):
    debug =1
    mydb = mysql.connector.connect(
    host=conf.sqlhost,
    user=conf.sqluser,
    password=conf.sqlpassword,
    database=conf.sqldb,
    allow_local_infile=True
    )

    mycursor = mydb.cursor(buffered=True)
    sql = "Select NomeCartella from ModemSontex  WHERE  idconfk = " + str(condid)
    if debug == 1:
        print(colored(sql, "green"))
    mycursor.execute(sql)
    results = mycursor.fetchall()
    mydb.close()
    if debug == 1:
        print(results)
    return results
      
