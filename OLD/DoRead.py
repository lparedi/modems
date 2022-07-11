import sys
import mysql.connector
import http.client
from datetime import date
import time
import os.path
from datetime import datetime
from subprocess import call
from termcolor import colored
import binascii
import commonfunctions
from commonfunctions import *


argsvector = sys.argv
global debug

# condID = str(argvector[1])
status, argsdict = parsearguments(argsvector)
condID = argsdict["syncID"]
actions = getactions(condID)
mixedrecordsdict = {}

if actions["MbusMixedRecords"] == 1:
    mixedrecordsdict = cretamixedrecordsdict(condID)

if actions["CustomList"] == 1:
    meterslist = getcustommeterlist(condID, actions["AppendList"])
else:
    meterslist = getmeterslist(condID)

setactive(True, condID)
if "debug" in argsdict:
    debug = int(argsdict["debug"])
else:
    debug = 0

modemnumber = getmodemnumber(condID)
today = date.today().strftime("%Y%m%d")
today = "20211109"
Telegrams,rescue,rescuereversed = DoRemoteRead(today, modemnumber, 365)
Mbresults = DecodeUsingPymbus(Telegrams,actions["MbusRecordCurrentValue"], actions["MbusMixedRecords"], mixedrecordsdict)
if actions["UseSQL"] == 1:
    TelegramToSql(condID,Telegrams,today,actions["MbusRecordCurrentValue"],actions["MbusMixedRecords"],mixedrecordsdict,actions["PyMbus"],Mbresults)

if actions["WriteOnFile"] == 1:
    if not  os.path.isdir(condID + "/" + today + "/"):
        os.mkdir(condID + "/" + today + "/")
    for mbres,telegram in zip (Mbresults,Telegrams):
        meter = extractmeterfromtelegram(telegram)
        fout = open(condID + "/" + today + "/" + meter.rstrip() + ".hex", "w+")
        fout.write(telegram + '\n')
        fout.close()
        if actions["UseSQL"] == 1:
            fout = open(condID + "/" + today + "/" + meter.rstrip() + ".txt", "w+")
            fout.write(mbres["ID"] + "," + mbres["Status"] + "," + mbres["CurrentValue"] + "," + mbres["Units"] + '\n')
            fout.close()
if debug == 1:
    print("Set Last Read to " + today)
setlastread(today, condID)
count = 0
readedfromsql = getmetersreaded(condID,today)
for hca in meterslist:
    if actions["CustomList"]:
        line = hca
    else:
        line = str(hca[0])
    if actions["WriteOnFile"] == 1:
        if not os.path.isfile(condID + "/" + today + "/" + str(line) + ".hex"):
            if debug == 1:
                print(colored("Miss From File " + str(line), "red"))
            count = count + 1
    else:
        if  str(line)  not in readedfromsql:
            if debug == 1:
                print(colored("Miss From SQL " + str(line), "red"))
            count = count + 1

if debug == 1:
    print(colored("Unreads:" + str(count), "red"))


setunreads(count, condID)
setreadstatus(count, condID)
if count != 0:
    setdoto(1, condID)
setactive(False, condID)
