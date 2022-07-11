
from Modem import Modem
from commonfunctions import *
import sys
from Config import configuration
from pprint import pprint

conf = configuration
argsvector = sys.argv
debug =1 

# condID = str(argvector[1])
status, argsdict = parsearguments(argsvector)
condID = argsdict["syncID"]
actions = getactions(condID)
mixedrecordsdict = {}
mixedlastrecived = {}
RealEstates = []
meterslist = {}
RealEstates = getrealestates(condID, actions["MixedRE"])
print(RealEstates)
print(actions)
if actions["OverwriteCondID"] != 0:
    ModemsType = getmodemtype(actions["OverwriteCondID"])
else:
    ModemsType = getmodemtype(condID)


if str(ModemsType[0][0]) == "646":
    inifilepath = getinifilepath(condID)
    SontexMetersType = getsontexmeterstype(condID)
    

    AesKey = getsontexaeskey(condID)
    print(inifilepath)
    
if actions["MbusMixedRecords"] == 1:
    mixedrecordsdict = cretamixedrecordsdict(RealEstates)


if actions["MbusMixedLast"] == 1:
    mixedlastrecived = cretalastrecordsdict(condID)

if actions["CustomList"] == 1:
    meterslist = getcustommeterlist(RealEstates, actions["AppendList"],actions["OverwriteCondID"],actions["ReadRNN"],actions["ReadEnergy"],actions["ReadWater"])

else:
    for re in RealEstates:
        meterslist.update(getmeterslist(re,actions["ReadRNN"],actions["ReadEnergy"],actions["ReadWater"]))

if debug == 1:
    print(meterslist)

#exit(0)
setactive(True, condID)
if "debug" in argsdict:
    debug = int(argsdict["debug"])
else:
    debug = 0
if actions["Disabled"] ==1:
    print(colored("Not Active!!","red"))
    setactive(False, condID)
    try:
        os.remove(condID + "/" + condID + ".pid")
    except:
        pass
    exit(0)
if actions["ReadOnSummer"] == 0 and (int(date.today().strftime("%m")) > 5 and int(date.today().strftime("%m")) < 10  ) and actions["Unreads"] == 0 :
    print(colored("Summer read disabled","red"))
    setactive(False, condID)
    try:
        os.remove(condID + "/" + condID + ".pid")
    except:
        pass
    exit(0)
modemnumber = getmodemnumber(condID)
if str(ModemsType[0][0]) == "646":
    MyModem = Modem(modemnumber,conf.restserver,conf.restauthstring,actions["TryToGuessR"],SontexMetersType,AesKey[0][0],actions["SpecialConf"])
else:
    MyModem = Modem(modemnumber,conf.restserver,conf.restauthstring,actions["TryToGuessR"])
today = date.today().strftime("%Y%m")
if actions["FakeReadingsDate"] != 0 :
    today = str(actions["FakeReadingsDate"])
#today = "202205"
if not os.path.isdir(condID + "/"):
        os.mkdir(condID + "/")
if str(ModemsType[0][0]) == "646":
    MyModem.DoSontexRead(inifilepath)
else:
    MyModem.DoRemoteRead(today, 1999)
MyModem.trytorescue(MyModem.Rescued)
MyModem.trytorescue(MyModem.RescuedReversed)
MyModem.DecodeUsingPymbus(actions["MbusRecordCurrentValue"],actions["MbusRecordLastRecived"],actions["MbusMixedLast"], actions["MbusMixedRecords"], mixedrecordsdict,mixedlastrecived,actions["ExceptSpecial"])
#pprint(MyModem.Mbresults)
if actions["UseSQL"] == 1:
    

    TelegramToSql(meterslist, MyModem.Telegrams, today, actions["MbusRecordCurrentValue"], actions["MbusMixedRecords"], mixedrecordsdict, actions["PyMbus"], MyModem.Mbresults)

if actions["WriteOnFile"] == 1:
    if not os.path.isdir(condID + "/" + today + "/"):
        os.mkdir(condID + "/" + today + "/")
    for mbres, telegram in zip(MyModem.Mbresults, MyModem.Telegrams):
        meter = MyModem.extractmeterfromtelegram(telegram)
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

readedfromsql = getmetersreaded(RealEstates, today,actions["OverwriteCondID"])
#print(meterslist)
#print(readedfromsql)
#exit(0)
for hca in meterslist.keys():
   
    if actions["CustomList"]:
        line = str(hca)
        if len(line) < 8:
            line = ( 8 - len(line)) * "0" + line
    else:
        line = str(hca)
        if len(line) < 8:
            line = ( 8 - len(line)) * "0" + line
    if actions["WriteOnFile"] == 1 and actions["UseSQL"] == 0:
        if not os.path.isfile(condID + "/" + today + "/" + str(line) + ".hex"):
            if debug == 1:
                print(colored("Miss From File " + str(line), "red"))
            count = count + 1
    else:
        if str(line) not in readedfromsql and  str(line) not in actions["IgnoredList"]:
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
print(str(len(MyModem.Telegrams)) + " " + str(len(MyModem.Mbresults)))

if actions["ToDB"] == 1:
    for reid in RealEstates :
        if debug == 1:
            print("insert reading for condid " + str(reid))
        if actions["OverwriteCondID"] != 0:
            lettura =  createxmlletture(actions["OverwriteCondID"], today, "MeasureUnit.HCA")
        else:
            lettura = createxmlletture(reid, today, "MeasureUnit.HCA")
        if lettura != "":
            #PymBusToLetture(condID, lettura, today, "MeasureUnit.HCA")
            if actions["OverwriteCondID"] != 0:
                PymBusToLetture_modem(actions["OverwriteCondID"], lettura, today, "MeasureUnit.HCA")
            else:
                PymBusToLetture_modem(reid, lettura, today, "MeasureUnit.HCA")
        if actions["OverwriteCondID"] != 0:
            lettura = createxmlletture_acqua(actions["OverwriteCondID"], today, "MeasureUnit.M3")
            
        else:        
            lettura = createxmlletture_acqua(reid, today, "MeasureUnit.M3")
        if lettura != "":
            #PymBusToLetture(condID, lettura, today, "MeasureUnit.M3")
            if actions["OverwriteCondID"] != 0:
                PymBusToLetture_modem(actions["OverwriteCondID"], lettura, today, "MeasureUnit.M3")
            else:
                
                PymBusToLetture_modem(reid, lettura, today, "MeasureUnit.M3")
        if actions["OverwriteCondID"] != 0:
             lettura = createxmlletture_energia( actions["OverwriteCondID"], today, "MeasureUnit.WH")
        else:
            lettura = createxmlletture_energia(reid, today, "MeasureUnit.WH")
        if lettura != "":
            #pass
            #PymBusToLetture(condID, lettura, today, "MeasureUnit.WH")
           
            if actions["OverwriteCondID"] != 0:
                
                PymBusToLetture_modem( actions["OverwriteCondID"], lettura, today, "MeasureUnit.WH")

            else:
                PymBusToLetture_modem(reid, lettura, today, "MeasureUnit.WH")
