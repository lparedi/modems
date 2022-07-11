
from pydoc import doc
from commonfunctions import *
from Modem import Modem
import sys
import time
debug = 1
argsvector = sys.argv

status, argsdict = parsearguments(argsvector)
condID = argsdict["syncID"]
mixedrecordsdict = cretamixedrecordsdict(condID)
ealEstates = []
meterslist = {}


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
MyModem = Modem(modemnumber)

acon, arn, firstatime = MyModem.ans()
atime = firstatime
setlastrecived(condID, atime)
if debug == 1:
    print(colored("atime:" + atime + " acon:" + acon, "red"))
if actions["MbusMixedRecords"] == 1:
    mixedrecordsdict = cretamixedrecordsdict(condID)

if actions["CustomList"] == 1:
    meterslist = getcustommeterlist(RealEstates, actions["AppendList"])
else:
    for re in RealEstates:
        meterslist.update(getmeterslist(re))

print(meterslist)
metersliststatus, MbusDict = createmeterslistfile(meterslist, condID, actions["CustomList"])

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
        for i in range(0,3):
            MyModem.lpw0()
            time.sleep(5)
        
        # time.sleep(90)
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
    today = "202201"
    if not os.path.isdir(condID + "/" + today):
        os.mkdir(condID + "/" + today)
    if debug == 1:
        print(colored("Today: " + today, "red"))
    # alllocal(today)
    # std(modemnumber)

    if actions["Parity"] != "":
        if debug == 1:
            print(colored("Parity " + actions["Parity"],"red"))
        for i in range(0,3):
            MyModem.sendprecomputed(ascii_to_hex("###AT+EVEN=" + actions["Parity"] +";"))
            time.sleep(5)

    if actions["Baud"] != "":
        if debug == 1:
            print(colored("Baud " + actions["Baud"],"red"))
        for i in range(0,3):
            MyModem.sendprecomputed(ascii_to_hex("###AT+BAUD=" + actions["Baud"] +";"))
            time.sleep(5)

    if actions["Npol"] != "":
        if debug == 1 :
            print(colored("Npol " + actions["Npol"],"red"))
        for i in range(0,3):
            MyModem.sendprecomputed(ascii_to_hex("###AT+NPOL=" + actions["Npol"] +";"))
            time.sleep(5)
    
    if actions["Sched2"] != "":
        if debug == 1 :
            print(colored("sched2 " + actions["Sched2"],"red"))
        for i in range(0,3):
            MyModem.sendprecomputed(ascii_to_hex("###AT+SCHD=2-" + actions["Sched2"] +";"))
            time.sleep(5)
    

    if actions["Sched4"] != "":
        if debug == 1 :
            print(colored("sched4 " + actions["Sched4"],"red"))
        for i in range(0,3):
            MyModem.sendprecomputed(ascii_to_hex("###AT+SCHD=4-" + actions["Sched4"] +";"))
            time.sleep(5)

    if actions["S_LPW"] != "0":
        if debug == 1:
            print(colored("Set LPW " + actions["S_LPW"], "red"))
        for i in range(0,3):
            MyModem.lpw()
            time.sleep(5)
    
    if actions["StdData"] != "0":
        if debug == 1:
            print(colored("StdData "  + actions["StdData"], "red"))
        
            MyModem.sendprecomputed("###AT+MBUS=?,i;")
            time.sleep(5)

# time.sleep(60)
setactive(False, condID)
os.remove(condID + "/" + condID + ".pid")
