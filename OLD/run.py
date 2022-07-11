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
from commonfunctions import *

global debug
argsvector = sys.argv
# condID = str(argvector[1])
status, argsdict = parsearguments(argsvector)
condID = argsdict["syncID"]
mixedrecordsdict = cretamixedrecordsdict(condID)

fpid = open(condID + "/" + condID + ".pid", "w")
fpid.write(str(os.getpid()))
fpid.close()
setpid(os.getpid(), condID)
setactive(True, condID)
actions = getactions(condID)
if "debug" in argsdict:
    debug = int(argsdict["debug"])
else:
    debug = 0
if debug == 1:
    print(colored(condID, "red"))

if debug == 1:
    print(colored("ACTIONS", "red"))
    print(actions)
# rnf=open(condID + "/rnf.txt")
# rn=rnf.read()
# rnf.close()
modemnumber = getmodemnumber(condID)
acon, arn, firstatime = ans(modemnumber)
atime = firstatime
setlastrecived(condID, atime)
if debug == 1:
    print(colored("atime:" + atime + " acon:" + acon, "red"))
if actions["CustomList"] == 1:
    meterslist = getcustommeterlist(condID, actions["AppendList"])
else:
    meterslist = getmeterslist(condID)


metersliststatus, MbusDict = createmeterslistfile(meterslist, condID , actions["CustomList"])

# rip = open("rip","w")
# for hca in meterslist:
# rip.write(str(hca[0]) + "FFFFFFFF\n")
# rip.close()
# rc = call("./genlist.sh " + condID, shell=True)
# print(hca[0])

#while not ("5245414459" in acon) or firstatime == atime:  # acon != "524541445920544f20524551554553540a" or firstatime == atime:
#sendprecomputed("23232341542b5752534e3d31302c312d39333434353839342d39333434353930352d39333434353930362d39333434353930372d39333434353930382d32363834373535332d32363834373535342d32363834373535352d32363834373535362d32363834373535373b","393688441940")

while firstatime == atime:
    time.sleep(5)
    if debug == 1:
        print(colored(datetime.now(), "green"))
    #sendprecomputed("23232341542b564c534e3d3f3b", modemnumber)

    acon, arn, atime = ans(modemnumber)
# rnf=open(condID +  "/rnf.txt","w")
# rnf.write(arn)
# rnf.close()
setlastrecived(condID, atime)
if debug == 1:
    print(colored("Something to do:" + str(actions["ToDo"]), "red"))
if actions["ToDo"] == 1:
    if actions["S_LP0"] == 1:
        if debug == 1:
            print(colored("Set LPW0", "red"))
        lpw0(modemnumber)
        time.sleep(5)
        lpw0(modemnumber)
        time.sleep(5)
        #time.sleep(90)        
    if actions["UpdateMeterList"] != 0:
        if debug == 1:
            print(colored("Set Meter List", "red"))
            print(MbusDict)
        if True:
            acon, arn, ftime = ans(modemnumber)
            for meter in MbusDict:
                atime=ftime
                bird = 0
                print(colored("fuori","green"))
                while atime == ftime:
                    if bird == 1:
                        print(colored("Ripetizione","red"))

                    sendprecomputed(MbusDict[meter], str(modemnumber))
                    #sendprecomputed(MbusDict[meter], str(modemnumber))
                    #sendprecomputed(MbusDict[meter], str(modemnumber))
                    time.sleep(40)
                    acon, arn, ftime = ans(modemnumber)
                    bird = 1

    if actions["S_RSTM"] == "1":
        if debug == 1:
            print(colored("Set RSTM to NOW", "red"))
        set_rstm_now(modemnumber)
        time.sleep(5)
        set_rstm_now(modemnumber)
        time.sleep(5)

    # today = date.today().strftime("%Y%m%d")
    destfolder = actions["LastRead"]
    destfolder ="20211102"
    today = date.today().strftime("%Y%m%d")
    today = "20211108"
    if not os.path.isdir(condID + "/" + today):
        os.mkdir(condID + "/" + today)
    if debug == 1:
        print(colored("Today: " + today, "red"))
    # alllocal(today)
    # std(modemnumber)
    if debug == 1:
        print(colored("Red Missing:" + str(actions["ReadMissing"]), "red"))
        print(colored("Unreads:" + str(actions["Unreads"]), "red"))
    if actions["ReadMissing"] == 1 and actions["Unreads"] != 0:

        missing = 1
        count = 1
        unreads = 0

        while missing == 1 and count < 5:
            missing = 0
            Telegrams, rescue, rescuereversed = DoRemoteRead(today, modemnumber, 365)

            Mbresults = DecodeUsingPymbus(Telegrams, actions["MbusRecordCurrentValue"], actions["MbusMixedRecords"],mixedrecordsdict)

            if actions["UseSQL"] == 1:
                TelegramToSql(condID, Telegrams, today, actions["MbusRecordCurrentValue"], actions["MbusMixedRecords"],
                              mixedrecordsdict, actions["PyMbus"], Mbresults)

            if actions["WriteOnFile"] == 1:
                for mbres, telegram in zip(Mbresults, Telegrams):
                    meter = extractmeterfromtelegram(telegram)
                    fout = open(condID + "/" + today + "/" + meter.rstrip() + ".hex", "w+")
                    fout.write(telegram + '\n')
                    fout.close()
                    if actions["UseSQL"] == 1:
                        fout = open(condID + "/" + today + "/" + meter.rstrip() + ".txt", "w+")
                        fout.write(
                            mbres["ID"] + "," + mbres["Status"] + "," + mbres["CurrentValue"] + "," + mbres["Units"] + '\n')
                        fout.close()

            readedfromsql = getmetersreaded(condID, today)
            unreads = 0
            for hca in meterslist:

                if actions["CustomList"] == 1:
                    line = str(hca)
                else:
                    line = str(hca[0])
                # all(line.rstrip(),today)
                #print(os.path.isfile(condID + "/" + today + "/" + line.rstrip() + ".hex"))
                if actions["WriteOnFile"] == 1:
                    if not os.path.isfile(condID + "/" + today + "/" + str(line) + ".hex"):

                        if actions["StrictMbus"] == 1:
                            if debug == 1:
                                print(colored("Sending Mbus command for " + line, "red"))
                            #precomputed = computetelegram("SND_NKE")
                            #sendprecomputed(precomputed, modemnumber)
                            time.sleep(5)
                            precomputed = computetelegram("SELECT_FD", line)
                            sendprecomputed(precomputed, modemnumber)
                            #time.sleep(5)
                            #precomputed = computetelegram("SELECT_STD")
                            #sendprecomputed(precomputed, modemnumber)
                            time.sleep(5)
                            precomputed = computetelegram("REQ_UD2_FD")
                            sendprecomputed(precomputed, modemnumber)
                            time.sleep(5)
                            #precomputed = computetelegram("SND_NKE")
                            #sendprecomputed(precomputed, modemnumber)


                        else:
                            rd = 0
                            acon, arn, ftime = ans(modemnumber)
                            atime = ftime
                            precomputed = "###AT+MBUS=" + line + ";"
                            sendprecomputed(ascii_to_hex(precomputed).decode("utf-8"), modemnumber)
                            while atime == ftime and rd < 6:
                                rd = rd + 1
                                time.sleep(5)
                                acon, arn, ftime = ans(modemnumber)



                        missing = 1
                        unreads = unreads + 1
                if actions["UseSQL"] == 1 and actions["WriteOnFile"] == 0 :
                    if str(line) not in readedfromsql:
                        if actions["StrictMbus"] == 1:
                            if debug == 1:
                                print(colored("Sending Mbus command for " + line, "red"))
                            # precomputed = computetelegram("SND_NKE")
                            # sendprecomputed(precomputed, modemnumber)
                            time.sleep(5)
                            precomputed = computetelegram("SELECT_FD", line)
                            sendprecomputed(precomputed, modemnumber)
                            # time.sleep(5)
                            # precomputed = computetelegram("SELECT_STD")
                            # sendprecomputed(precomputed, modemnumber)
                            time.sleep(5)
                            precomputed = computetelegram("REQ_UD2_FD")
                            sendprecomputed(precomputed, modemnumber)
                            time.sleep(5)
                            # precomputed = computetelegram("SND_NKE")
                            # sendprecomputed(precomputed, modemnumber)


                        else:
                            rd = 0
                            acon, arn, ftime = ans(modemnumber)
                            atime = ftime
                            precomputed = "###AT+MBUS=" + line + ";"
                            if debug ==1:
                                print(colored(precomputed,"red"))
                            sendprecomputed(ascii_to_hex(precomputed).decode("utf-8"), modemnumber)
                            while atime == ftime and rd < 6:
                                rd = rd + 1
                                time.sleep(5)
                                acon, arn, ftime = ans(modemnumber)

                        missing = 1
                        unreads = unreads + 1


            count += 1
            if missing == 1:
                if debug == 1:
                    print(colored("ITERATION NUMBER " + str(count), "red"))

            setunreads(unreads, condID)


    if actions["S_LPW"] != "0":
        if debug == 1:
            print(colored("Set LPW" + actions["S_LPW"], "red"))
        lpw(modemnumber, actions["S_LPW"])
        time.sleep(5)
        lpw(modemnumber, actions["S_LPW"])
        time.sleep(5)
        lpw(modemnumber, actions["S_LPW"])
        time.sleep(5)
        lpw(modemnumber, actions["S_LPW"])
        time.sleep(5)
        lpw(modemnumber, actions["S_LPW"])
#time.sleep(60)
setactive(False, condID)
os.remove(condID + "/" + condID + ".pid")
