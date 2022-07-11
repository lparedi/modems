import time
import sys
from commonfunctions import *
import time
from subprocess import call

fpid = open("cron.pid", "w")
fpid.write(str(os.getpid()))
fpid.close()
setalllastrecived()
allfields = getallfileds()
count = 0
debug =0
while True:
    if count > 6:
        allfields = getallfileds()
        count = 0
    start = time.time()
    # condids = getcondids()
    currentday = date.today().strftime("%d")
    currentdate = date.today().strftime("%Y%m%d")

    for (idCONfk, Active, ForceIfIsTime, LastRecived, Recursion, FirstWakeUpTime, Disabled) in allfields:
        
        if Disabled == 1:
            continue
        if debug == 1:
            print("\n\n\n\n\n***********")
            print(str(idCONfk))
        if debug == 1:
            print(colored(str(getlastread(str(idCONfk))) +
                  " - " + str(currentdate), "red"))
        if not os.path.isdir(str(idCONfk) + "/"):
            os.mkdir(str(idCONfk) + "/")
        if  True:#idCONfk == 14671 :
            if checkifistime_allfields(Active, ForceIfIsTime, LastRecived, Recursion, FirstWakeUpTime):
                rc = call("nohup python3 runOOP.py " + str(idCONfk) + " debug 1 1>" + str(idCONfk) + "/" +
                          str(idCONfk) + ".out 2>" + str(idCONfk) + "/" + str(idCONfk) + ".err &", shell=True)
                print("Run " + str(idCONfk))
                count = 6

    end = time.time()
    print("Elapsed:" + str(end - start))
    print(count)

    time.sleep(5)
    count = count + 1


print("finito")
