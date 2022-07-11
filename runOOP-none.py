global debug
from commonfunctions import *
from Modem import Modem
import sys
import time
from Config import configuration

conf = configuration


argsvector = sys.argv

status, argsdict = parsearguments(argsvector)
condID = argsdict["syncID"]
mixedrecordsdict = cretamixedrecordsdict(condID)
ealEstates = []
meterslist = {}
mixedlastrecived = {}


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
RealEstates = getrealestates(condID, actions["MixedRE"])
modemnumber = getmodemnumber(condID)
MyModem = Modem(modemnumber,conf.restserver,conf.restauthstring,actions["TryToGuessR"])

acon, arn, firstatime = MyModem.ans()
atime = firstatime
setlastrecived(condID, atime)
if debug == 1:
    print(colored("atime:" + atime + " acon:" + acon, "red"))
if actions["MbusMixedRecords"] == 1:
    mixedrecordsdict = cretamixedrecordsdict(condID)
if actions["MbusMixedLast"] == 1:
    mixedlastrecived = cretalastrecordsdict(condID)


if actions["CustomList"] == 1:
    meterslist = getcustommeterlist(RealEstates, actions["AppendList"],actions["OverwriteCondID"],actions["ReadRNN"],actions["ReadEnergy"],actions["ReadWater"])
else:
    for re in RealEstates:
        meterslist.update(getmeterslist(re,actions["ReadRNN"],actions["ReadEnergy"],actions["ReadWater"]))

print(meterslist)
metersliststatus, MbusDict = createmeterslistdb(meterslist, condID, actions["CustomList"])

# rip = open("rip","w")
# for hca in meterslist:
# rip.write(str(hca[0]) + "FFFFFFFF\n")
# rip.close()
# rc = call("./genlist.sh " + condID, shell=True)
# print(hca[0])

# while not ("5245414459" in acon) or firstatime == atime:  # acon != "524541445920544f20524551554553540a" or firstatime == atime:
# sendprecomputed("23232341542b5752534e3d31302c312d39333434353839342d39333434353930352d39333434353930362d39333434353930372d39333434353930382d32363834373535332d32363834373535342d32363834373535352d32363834373535362d32363834373535373b","393688441940")

while firstatime == atime:
    try:
        time.sleep(5)
        if debug == 1:
            print(colored(datetime.now(), "green"))
    # sendprecomputed("23232341542b564c534e3d3f3b", modemnumber)

        acon, arn, atime = MyModem.ans()
    except (KeyboardInterrupt):
        sys.exit(0)
    except:
        continue
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
        MyModem.lpw0()
        time.sleep(5)
        MyModem.lpw0()
        time.sleep(5)
        MyModem.lpw0()
        time.sleep(5)
        MyModem.lpw0()
        time.sleep(5)
        # time.sleep(90)
    MyModem.sendprecomputed("23232341542b534348443d342d312d302d302d31322d31352d2a2d2a2d2a3b")
    MyModem.sendprecomputed("23232341542b534348443d342d312d302d302d31322d31352d2a2d2a2d2a3b")
    MyModem.sendprecomputed("23232341542B534348443D322D312D30302D31332D31302D2F332D2A2D2A2D2A3B")
    MyModem.sendprecomputed("23232341542B534348443D322D312D30302D31332D31302D2F332D2A2D2A2D2A3B")
    if actions["UpdateMeterList"] != 0:
        if debug == 1:
            print(colored("Set Meter List", "red"))
            print(MbusDict)
        if True:
            acon, arn, ftime = MyModem.ans()
            for meter in MbusDict:
                atime = ftime
                bird = 0
                print(colored("fuori", "green"))
                while atime == ftime:
                    if bird == 1:
                        print(colored("Ripetizione", "red"))

                    MyModem.sendprecomputed(MbusDict[meter])
                    # sendprecomputed(MbusDict[meter], str(modemnumber))
                    # sendprecomputed(MbusDict[meter], str(modemnumber))
                    time.sleep(40)
                    acon, arn, ftime = MyModem.ans()
                    bird = 1

    if actions["S_RSTM"] == "1":
        if debug == 1:
            print(colored("Set RSTM to NOW", "red"))
        MyModem.set_rstm_now()
        time.sleep(5)
        MyModem.set_rstm_now()
        time.sleep(5)

    # today = date.today().strftime("%Y%m%d")
    destfolder = actions["LastRead"]
    destfolder = "20211206"
    today = date.today().strftime("%Y%m%d")
    today = "202203"
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
            MyModem.Clear()
            MyModem.DoRemoteRead(today)
            MyModem.trytorescue(MyModem.Rescued)
            MyModem.trytorescue(MyModem.RescuedReversed)
            MyModem.DecodeUsingPymbus(actions["MbusRecordCurrentValue"],actions["MbusRecordLastRecived"],actions["MbusMixedLast"], actions["MbusMixedRecords"], mixedrecordsdict,mixedlastrecived)

            if actions["UseSQL"] == 1:
                TelegramToSql(meterslist, MyModem.Telegrams, today, actions["MbusRecordCurrentValue"], actions["MbusMixedRecords"],
                              mixedrecordsdict, actions["PyMbus"], MyModem.Mbresults)
                readedfromsql = getmetersreaded(RealEstates, today)

            if actions["WriteOnFile"] == 1:
                for mbres, telegram in zip(MyModem.Mbresults, MyModem.Telegrams):
                    meter = MyModem.extractmeterfromtelegram(telegram)
                    fout = open(condID + "/" + today + "/" + meter.rstrip() + ".hex", "w+")
                    fout.write(telegram + '\n')
                    fout.close()
                    if actions["PyMbus"] == 1:
                        fout = open(condID + "/" + today + "/" + meter.rstrip() + ".txt", "w+")
                        fout.write(
                            mbres["ID"] + "," + mbres["Status"] + "," + mbres["CurrentValue"] + "," + mbres["Units"] + '\n')
                        fout.close()

            for hca in meterslist.keys():
                if actions["CustomList"]:
                    line = hca
                else:
                    line = str(hca)
                if actions["WriteOnFile"] == 1 and actions["UseSQL"] == 0:
                    if not os.path.isfile(condID + "/" + today + "/" + str(line) + ".hex") and str(line) not in actions["IgnoredList"]:
                        if debug == 1:
                            print(colored("Miss From File " + str(line), "red"))
                        unreads = unreads + 1
                else:
                    if str(line) not in readedfromsql and str(line) not in actions["IgnoredList"] :
                        if debug == 1:
                            print(colored("Miss From SQL " + str(line), "red"))
                        unreads = unreads + 1

            for hca in meterslist:

                if actions["CustomList"] == 1:
                    

                    line = str(hca)
                    if len(line) < 8:
                        line = ( 8 - len(line)) * "0" + line
                else:
                    line = str(hca)
                    if len(line) < 8:
                        line = ( 8 - len(line)) * "0" + line
                # all(line.rstrip(),today)
                # print(os.path.isfile(condID + "/" + today + "/" + line.rstrip() + ".hex"))
                if actions["WriteOnFile"] == 1:
                    if not os.path.isfile(condID + "/" + today + "/" + str(line) + ".hex") and str(line) not in actions["IgnoredList"]:

                        if actions["StrictMbus"] == 1:
                            if debug == 1:
                                print(colored("Sending Mbus command for " + line, "red"))
                            # precomputed = computetelegram("SND_NKE")
                            # sendprecomputed(precomputed, modemnumber)
                            time.sleep(5)
                            precomputed = MyModem.computetelegram("SELECT_FD", line)
                            MyModem.sendprecomputed(precomputed)
                            # time.sleep(5)
                            # precomputed = computetelegram("SELECT_STD")
                            # sendprecomputed(precomputed, modemnumber)
                            time.sleep(5)
                            precomputed = MyModem.computetelegram("REQ_UD2_FD")
                            MyModem.sendprecomputed(precomputed)
                            time.sleep(5)
                            # precomputed = computetelegram("SND_NKE")
                            # sendprecomputed(precomputed, modemnumber)

                        else:
                            rd = 0
                            acon, arn, ftime = MyModem.ans()
                            atime = ftime
                            if len(line) < 8:
                                line = "0"+line
                            precomputed = "###AT+MBUS=" + line + ";"
                            MyModem.sendprecomputed(ascii_to_hex(precomputed).decode("utf-8"))
                            while atime == ftime and rd < 6:
                                rd = rd + 1
                                time.sleep(5)
                                acon, arn, ftime = MyModem.ans()

                        missing = 1

                if actions["UseSQL"] == 1:
                    if str(line) not in readedfromsql  and   str(line) not in actions["IgnoredList"]  :
                        if actions["StrictMbus"] == 1:
                            if debug == 1:
                                print(colored("Sending Mbus command for " + line, "red"))
                            # precomputed = computetelegram("SND_NKE")
                            # sendprecomputed(precomputed, modemnumber)
                            time.sleep(5)
                            precomputed = MyModem.computetelegram("SELECT_FD", line)
                            MyModem.sendprecomputed(precomputed)
                            time.sleep(5)
                            precomputed = MyModem.computetelegram("SELECT_STD")
                            MyModem.sendprecomputed(precomputed)
                            # sendprecomputed(precomputed, modemnumber)
                            time.sleep(5)
                            precomputed = MyModem.computetelegram("REQ_UD2_FD")
                            MyModem.sendprecomputed(precomputed)
                            time.sleep(5)
                            # precomputed = computetelegram("SND_NKE")
                            # sendprecomputed(precomputed, modemnumber)

                        else:
                            rd = 0
                            acon, arn, ftime = MyModem.ans()
                            atime = ftime
                            precomputed = "###AT+MBUS=" + line + ";"
                            if debug == 1:
                                print(colored(precomputed, "red"))
                            MyModem.sendprecomputed(ascii_to_hex(precomputed).decode("utf-8"))
                            while atime == ftime and rd < 6:
                                rd = rd + 1
                                time.sleep(5)
                                acon, arn, ftime = MyModem.ans()

                        missing = 1

            count += 1
            if missing == 1:
                if debug == 1:
                    print(colored("ITERATION NUMBER " + str(count), "red"))

            setunreads(unreads, condID)

    if actions["S_LPW"] != "0":
        if debug == 1:
            print(colored("Set LPW" + actions["S_LPW"], "red"))
        MyModem.lpw()
        time.sleep(5)
        MyModem.lpw()
        time.sleep(5)
        MyModem.lpw()
        time.sleep(5)
        MyModem.lpw()
        time.sleep(5)
        MyModem.lpw()
# time.sleep(60)
setactive(False, condID)
os.remove(condID + "/" + condID + ".pid")
