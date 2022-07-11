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
    MyModem.sendprecomputed("23232341542b534348443d342d312d302d302d31322d31352d2a2d2a2d2a3b")
    MyModem.sendprecomputed("23232341542b534348443d342d312d302d302d31322d31352d2a2d2a2d2a3b")
    MyModem.sendprecomputed("23232341542B534348443D322D312D30302D31332D31302D2F332D2A2D2A2D2A3B")
    MyModem.sendprecomputed("23232341542B534348443D322D312D30302D31332D31302D2F332D2A2D2A2D2A3B")
    MyModem.sendprecomputed("23232341542B4D4255533D3F2C693B")

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
setactive(False, condID)
os.remove(condID + "/" + condID + ".pid")
