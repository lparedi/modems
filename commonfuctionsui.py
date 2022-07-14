from ast import Global
from pickletools import read_string1
from unittest import result
from click import pass_context
#debug =1
import pyodbc
from cmath import sin
from distutils.log import debug, error
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
from pprint import pprint


conf = configuration

debug = 0
def getcondata(codid):
    debug =0
    mydb = mysql.connector.connect(
        charset='utf8mb4',
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )
    #mydb.set_character_set('utf8')
    if debug == 1:
        print(colored("Creating Cond Data dictionary", "red"))
        
    mycursor = mydb.cursor()
    mycursor.execute('SET NAMES utf8;')
    mycursor.execute('SET CHARACTER SET utf8;')
    mycursor.execute('SET character_set_connection=utf8;')
    sql = "SELECT * FROM condomini  WHERE idCONpk = " + str(codid)
    if debug == 1:
        print(sql)
    mycursor.execute(sql)
    columns = mycursor.description 
    result = [{columns[index][0]:column for index, column in enumerate(value)} for value in mycursor.fetchall()]
    if debug == 1:
        pprint(result)
    mydb.close()
    return result


def getmetersinerror(condid , readdate):
    mydb = mysql.connector.connect(
        charset='utf8mb4',
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )

    if debug == 1:
        print("Get meters w error " + str(condid) + " " +  str(readdate))

    mycursor = mydb.cursor()
    mycursor.execute("SELECT SecAddr,Status as CodiceErrore , LastRecived as DataErrore , Value  as Lettura, ReadDate as DataLettura  FROM Telegrams  WHERE idCONfk = " + str(condid) + " AND (Status <> '0' AND  Status <> '4') AND ReadDate ='" + str(readdate) + "'")
    columns = mycursor.description 
    result = [{columns[index][0]:column for index, column in enumerate(value)} for value in mycursor.fetchall()]
    if debug == 1:
        pprint(result)
    mydb.close()
    return result

def GetAppartmentDatafromMeter(condid,meter):
    mydb = mysql.connector.connect(
        charset='utf8mb4',
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )
   
    if debug == 1:
        print("Get Appdata  w error " + str(condid) + " " +  str(meter))

    mycursor = mydb.cursor()
    sql = "SELECT intestatario,Locale,Note,Note as NoteRip,Ripartitore FROM elementi  WHERE idCONfk = " + str(condid) + " AND Ripartitore = " + str(meter)
    if debug == 1:
        print(sql)
    mycursor.execute(sql)
    columns = mycursor.description 
    resulti = [{columns[index][0]:column for index, column in enumerate(value)} for value in mycursor.fetchall()]
    if debug == 1:
        pprint(resulti)

    if not resulti:
        return [],[]  
    mycursor.execute("SELECT * FROM appartamenti  WHERE idCONfk = " + str(condid) + " AND intestatario = '" + addquote(str(resulti[0]['intestatario'])) +"'")
    columns = mycursor.description 
    result = [{columns[index][0]:column for index, column in enumerate(value)} for value in mycursor.fetchall()]
    if debug == 1:
        pprint(result)
    mydb.close()

    return result,resulti


def ArchiveAllBycondId(condid):
    debug = 0
    server = 'tcp:linux' 
    database = 'Ticket' 
    username = 'sa' 
    password = '1!Spikazzo11' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';encrypt=no')
    cursor = cnxn.cursor()
    sql = "UPDATE TicketTest set Stato = 'A' WHERE CondID = " + str(condid) + " AND ((Stato <> 'F' AND Stato <> 'L') or Stato is Null)"
    if debug == 1:
        print(sql)
    cursor.execute(sql)
    cnxn.commit()
    cnxn.close()
  

def ToSql(meter,condata):
    debug =0
    server = 'tcp:linux' 
    database = 'Ticket' 
    username = 'sa' 
    password = '1!Spikazzo11' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';encrypt=no')
    cursor = cnxn.cursor()

    
    if debug == 1:
        pprint(meter)

    sql = "SELECT Stato  From TicketTest WHERE CondID = " + str(condata['SyncID']) +  " AND CodiceRipartitore = '"  + str(meter['Ripartitore']) + "' AND ( Stato ='F' or stato ='L')"
    
    cursor.execute(sql)
    row = cursor.fetchone()
    if not row:
        sql = "INSERT INTO  TicketTest (Provincia , Citta,CAP,Indirizzo,Numero1,Numero2,Inquilino,Numero3,Numero4,Scala,Piano,Locale,CodiceErrore,DataErrore" \
                                        ",Antenna,Lettura,DataLettura,Letturista,CommittenteLetture,CommittenteRiparazioni,Alert,NoteCondominio,Amministratore, CondID,Appart, Note , Intestatario , CodiceRipartitore, Sessione )" \
                                        " VALUES ('" + condata['Provincia'] + "','" + condata['Città'] + "','" + str(condata['CAP']) + "','" + condata['Indirizzo'] + "','" + str(meter['Telefono']) + "','" + str(meter['CellProp']) + "','" + addquote(meter['Inquilino']) + "','" + str(meter['CellInq']) + "','" + str(meter['CellInq']) + "','" \
                                        + meter['Scala'] + "','" + str(meter['Piano']) + "','" + addquote(meter['Locale']) + "','" + str(meter['CodiceErrore']) + "','" + str(meter['DataErrore']) + "','" + '0' + "','" + str(meter['Lettura']) + "','" + str(meter['DataLettura']) + "','" + condata['Letturista'] + "','" \
                                        + condata['CommittenteLetture'] + "','" + condata['CommittenteLettureRiparazioni'] + "','" \
                                        + addquote(condata['Allert']) + "','" + addquote(condata['Note_x0020_Condominio']) + "','" + condata['Amministratore'] + "','" + str(condata['SyncID']) + "','" + str(meter['Appart']) + "','" + addquote(meter['NoteRip']) + "','" + addquote(meter['Intestatario']) + "','" + str(meter['Ripartitore']) + "' , '" + date.today().strftime("%m-%y") + "' )"
        if debug == 1:
            print(sql)
        
        cursor.execute(sql)
        cursor.commit()
    
    cnxn.close()
    pass

def getcondsid(today):
    
    mydb = mysql.connector.connect(
        charset='utf8mb4',
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )
   
    if debug == 1:
        print("Get Conds   error " + str(today))

    sql = "SELECT idconfk FROM Modems WHERE LastRead = " + str(today) + " AND Disabled = 0"
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    results = mycursor.fetchall()
    mydb.close()
    return results
    pass
def addquote(imp):
    return imp.replace("'","''")

def readstodict(rep,type):
    debug = 0
    results = []
    meterdic = {}

    buff = rep.split("\n")
    if debug ==1:
        print(buff)
    #exit(0)
    if type == "AMR":
        linecount = 0
        for line in buff:
            linecount= linecount +1
            if linecount > 5:
                metersatus = {}
                
                if len(line) < 2:
                    continue
               
                singlebuff = line.split("\t")
                if debug == 1:
                    print(line)
                meter = singlebuff[4]
                sts = singlebuff[7]
                if not "x" in singlebuff[8]:
                    dataerror = singlebuff[8]
                else:
                    dataerror = " "
                av = singlebuff[10]
                metersatus["Status"] = sts
                metersatus["ErrorDate"] = dataerror
                metersatus["CurrentValue"] = av
                meterdic[meter] = metersatus
                #results.append(meterdic)
    if type == "556":
        linecount = 0
        for line in buff:
            linecount = linecount +1
            if linecount >2:
                if len(line) < 2:
                    continue
                metersatus = {}
                singlebuff = line.split(";")
                if singlebuff[4] != "Lettura OK":
                    continue
                meter = singlebuff[2]
                sts = singlebuff[9]
                dataerror= singlebuff[54]
                av = singlebuff[10]
                metersatus["Status"] = sts
                metersatus["ErrorDate"] = dataerror
                metersatus["CurrentValue"] = av
                meterdic[meter] = metersatus
    
    if type == "566":
        linecount = 0
        for line in buff:
            linecount = linecount +1
            if linecount >2:
                if len(line) < 2:
                    continue
                metersatus = {}
                singlebuff = line.split(";")
                if singlebuff[4] != "Lettura OK":
                    continue
                meter = singlebuff[2]
                sts = singlebuff[11]
                dataerror= singlebuff[21]
                av = singlebuff[19]
                metersatus["Status"] = sts
                metersatus["ErrorDate"] = dataerror
                metersatus["CurrentValue"] = av
                meterdic[meter] = metersatus
        

    if debug == 1:
        pprint(meterdic)
    return(meterdic)


def getmeterstype(condid):
    debug =1
    mydb = mysql.connector.connect(
        charset='utf8mb4',
        host=conf.sqlhost,
        user=conf.sqluser,
        password=conf.sqlpassword,
        database=conf.sqldb,
        allow_local_infile=True
    )
   
    if debug == 1:
        print("Get MetersType for condid " + str(condid) )

    mycursor = mydb.cursor()
    sql = "SELECT MarcaRipartitoriInstallati,_x0035_66 from condomini where idconpk = " + str(condid)
    print(sql)
    mycursor.execute(sql)
    columns = mycursor.description 
    resulti = [{columns[index][0]:column for index, column in enumerate(value)} for value in mycursor.fetchall()]
    if debug == 1:
        pprint(resulti[0]['MarcaRipartitoriInstallati'])
        pprint(resulti[0]['_x0035_66'])
    if "Sie" in resulti[0]['MarcaRipartitoriInstallati'] or "Hon" in resulti[0]['MarcaRipartitoriInstallati']:
        return "AMR"
    if resulti[0]['_x0035_66']==1:
        return "566"
    if "556" in resulti[0]['MarcaRipartitoriInstallati'] :
        return "556"
 
    if "566" in resulti[0]['MarcaRipartitoriInstallati']:
        return "566"
    return "Unknown"

def extractidfromfilename(filename):
    buff = filename.split("_")
    return buff[0]
    pass

def getmetersinerrorfromdict(meterlist , meterdict,type,today):
    results = []
    if debug == 1:
        pprint(meterlist)
    for meter in meterdict.keys():
        if int(meter) in meterlist:
            if type == "AMR":
                if meterdict[meter]['Status'] != "0" and  meterdict[meter]['Status'] != "4":
                    a = a = {'SecAddr': meter , 'CodiceErrore': meterdict[meter]['Status'], 'DataErrore': meterdict[meter]['ErrorDate'], 'Lettura' : meterdict[meter]['CurrentValue'] ,'DataLettura' :today}
                    results.append(a)
            if  "5" in type:
                if meterdict[meter]['Status'] != "0" and  meterdict[meter]['Status'] != "2":
                    a = a = {'SecAddr': meter , 'CodiceErrore': meterdict[meter]['Status'], 'DataErrore': meterdict[meter]['ErrorDate'], 'Lettura' : meterdict[meter]['CurrentValue'] ,'DataLettura' :today}
                    results.append(a)
        else:
                pass
    if debug == 1:        
        pprint(results)
    return results

            
def isOkDestFolder(condata,basedir = "./PROVINCE/"):
    import glob
    debug =0
    basedir = "./ALBERATURA/"
    #pprint(condata)
    destforlder = basedir + condata["Provincia"] + "/" + condata["Città"] + "/" +  condata["SyncID"] + "*"
    if debug == 1:
        print(destforlder)
    destination = glob.glob(destforlder)
    if debug == 1:
        pprint(destination)
    if destination:
        return destination[0]
    destgroup = basedir + condata["Provincia"] + "/" + condata["Città"] + "/" + "GR " + condata["Indririzzo"] + "/*"
    

    destination = glob.glob(destgroup)
    for singles in destination:
        if  str(condata["SyncID"]) in singles:
            return  singles

    return []
    pass