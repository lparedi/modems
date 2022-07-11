
from asyncio.proactor_events import _ProactorBaseWritePipeTransport
import http.client
from datetime import date
from datetime import datetime
from pprint import pprint
from threading import get_ident

from numpy import count_nonzero
from termcolor import colored
import binascii
import meterbus
import base64
from Crypto.Cipher import AES
# import commonfunctions
# from commonfunctions import *
debug = 1


class Modem:
    Modemnumber = 0
    Telegrams = []
    Rescued = ""
    RescuedReversed = ""
    Mbresults = []
    Lpwsec = 60
    RestServer = ""
    AuthString = ""
    TryToGuess = ""
    MetersType = []
    AesKey = ""
    Special = ""

    def __init__(self, modemnumber,restserver,authstring,trytoguess,MetersType = [] , AesKey = "",Special = ''):
        self.Modemnumber = modemnumber
        self.RestServer = restserver
        self.AuthString = authstring
        self.TryToGuess = trytoguess
        self.AesKey = AesKey
        self.MetersType = MetersType
        self.Special = Special

    def Clear(self):
        self.Telegrams.clear()
        self.Mbresults.clear()

    def DoRemoteRead(self, dataread, nrecords=999):
        import http.client

        rescue = ""
        rescuereversed = ""

        # conn = http.client.HTTPSConnection("olivettiiot.tim.it",context = ssl._create_unverified_context())
        conn = http.client.HTTPSConnection(self.RestServer)
        payload = ''
        headers = {
            'Cache-Control': 'no-cache',
            'X-M2M-RI': 'CIN_1618507463',
            'X-M2M-Origin': 'CCEDB769A-ad46824a',
            'Content-Type': 'application/vnd.onem2m-res+json',
            'Accept': 'application/vnd.onem2m-res+json',
            'Authorization': self.AuthString
        }
        conn.request("GET", "/onem2m/" + str(self.Modemnumber) + "/nbiot/inbox?fu=2&ty=4&lim=" + str(nrecords), payload, headers)
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
                
                if len(buff[1].replace(" ", "")) > 2:
                    if len(buff[1].replace(" ", "")) > 24:
                        meter = self.extractmeterfromtelegram(buff[1].replace(" ", ""))
                    else:
                        meter = "00000000"
                    
                    if debug == 1:  # and False:
                        # print(colored("Expected: " + line, "red"))
                        print(colored("Meter: " + meter, "red"))
                        print(colored("Datared: " + dataread, "red"))
                        print(colored("CT: " + ct[0], "red"))
                    
                    if True:  # line == "26847569" and meter == "26847569":

                        if dataread in ct[0]:  # line in meter and dataread in ct[0]:  # buff[1].replace(" ", "")[14:20] ==

                            if buff[1][-2:].rstrip() == "16" and not ("00000000" in meter):
                                if debug == 1:
                                    print(colored(
                                        "check + tel line  : " + self.mbcheksum(buff[1]) + " " + buff[1][-5:].replace(" ", ""),
                                        "green"))
                                if self.mbcheksum(buff[1]) in buff[1][-5:].replace(" ", ""):
                                    if debug == 1:
                                        print("*******************************************")
                                        print("***  Dati : " + ct[0] + "-" + buff[1] + "  ******************")
                                        print("*******************************************")
                                        # print(colored("File line : " + line, "red"))
                                    self.Telegrams.append(s)
                                
                            else:
                                if debug == 1:
                                    print("Adding " + buff[1].replace(" ", ""))
                                rescue = buff[1].replace(" ", "") + rescue
                                rescuereversed = rescuereversed + buff[1].replace(" ", "")
                                # print(rescue)
                                # rescue = rescue + buff[1].replace(" ", "")
                                self.Rescued = rescue
                                self.RescuedReversed = rescuereversed
        conn.close()

    def DoSontexRead(self,inipaths):
        
        debug = 0
        for inipath in inipaths:
            fin = open(inipath,"r")
            lines = fin.readlines()
            fin.close()
            lineindex = 0 
           
            for line in lines:
                if "d0-" in line or lineindex < 6 or not "-" in line:
                    lineindex = lineindex +1 
                    continue
            
                codedtelegra = line.replace(line.split("=")[0] , "")
                if debug == 1:
                    print(line)
                b64decoded = base64.b64decode(codedtelegra).hex()
                
                self.Telegrams.append(b64decoded.upper())
            
        if debug == 1:    
            print(self.Telegrams)
        #exit(0)
        
    def DoRemoteReadCustom(self,dataread,searchfunction,nrecords=999):
        import http.client

        rescue = ""
        rescuereversed = ""

        # conn = http.client.HTTPSConnection("olivettiiot.tim.it",context = ssl._create_unverified_context())
        conn = http.client.HTTPSConnection(self.RestServer)
        payload = ''
        headers = {
            'Cache-Control': 'no-cache',
            'X-M2M-RI': 'CIN_1618507463',
            'X-M2M-Origin': 'CCEDB769A-ad46824a',
            'Content-Type': 'application/vnd.onem2m-res+json',
            'Accept': 'application/vnd.onem2m-res+json',
            'Authorization': self.AuthString
        }
        conn.request("GET", "/onem2m/" + str(self.Modemnumber) + "/nbiot/inbox?fu=2&ty=4&lim=" + str(nrecords), payload, headers)
        res = conn.getresponse()
        data = res.read()
        datastr = data.decode("utf-8")
        telegrams = searchfunction(datastr,dataread)
        self.Telegrams.append(telegrams)
        conn.close()


    def DecodeUsingPymbus(self, recordnumber=2,lastrecivedrecord =6 ,mixedlastrecived = 0, mixedrecords=0, mixedrecordsdict={},mixedlastrecivedrecordic={},ExceptSpecialConf=""):

        LocalTelegrams = self.Telegrams[:]
        exist = 0
        hitted = 0
        debug = 1
        position = 0
        for telegram in LocalTelegrams:
             
            try:
                lastrecivedrecordc = lastrecivedrecord
                recordnumberc = recordnumber 
                rdecoded = {}
                rdecodedf={}
                rdecodedin1={}
                rdecodedin2={}
                if debug == 1:
                    print("Decoding " + telegram)
                if len(telegram) < 40:
                    self.Telegrams.remove(telegram)
                    continue
                strtl = bytes.fromhex(telegram)

                try:
                    tg = meterbus.TelegramLong(strtl)

                except:
                    #raise
                    if debug == 1:
                        print("Could not interprete : " + telegram)
                    self.Telegrams.remove(telegram)
                    continue
                
                if not self.extractmeterfromtelegram(telegram) in ExceptSpecialConf and self.Special != "0":
                    
                    
                    if self.Special =="7x9cf2imp" and  (tg.body.bodyHeader.interpreted["medium"] == "0x4" or tg.body.bodyHeader.interpreted["medium"] == "0xc")  :
                        #exit(0)
                        if tg.body.interpreted["records"][0]['type'] == 'VIFUnitExt.RSSI':
                            #Main energy
                            ID = tg.body.bodyHeader.interpreted['identification']
                            ID = ID.replace(",", "")
                            ID = ID.replace("0x", "")
                            ID = ID.replace(" ", "")
                            rdecoded["ID"] = ID
                            Status = str(int( tg.body.bodyHeader.interpreted['status'], 16))
                            rdecoded["Status"] = Status
                            rdecoded["CurrentValue"] = tg.body.interpreted["records"][1]['value']
                            rdecoded["SetDayValue"] = tg.body.interpreted["records"][1]['value']
                            rdecoded["LastRecived"] = tg.body.interpreted["records"][17]['value']
                            rdecoded["SetDay"] = tg.body.interpreted["records"][18]['value']
                            rdecoded["Units"] = tg.body.interpreted["records"][1]['unit']
                            if debug == 1:
                                pprint(rdecoded)
                            position = position +1 
                            self.Mbresults.append(rdecoded)
                            
                            #Tariff 1
                            ID = "1"+  tg.body.bodyHeader.interpreted['identification']
                            ID = ID.replace(",", "")
                            ID = ID.replace("0x", "")
                            ID = ID.replace(" ", "")
                            rdecodedf["ID"] = ID
                            Status = str(int( tg.body.bodyHeader.interpreted['status'], 16))
                            rdecodedf["Status"] = Status
                            rdecodedf["CurrentValue"] = tg.body.interpreted["records"][7]['value']
                            rdecodedf["SetDayValue"] = tg.body.interpreted["records"][7]['value']
                            rdecodedf["LastRecived"] = tg.body.interpreted["records"][17]['value']
                            rdecodedf["SetDay"] = tg.body.interpreted["records"][18]['value']
                            rdecodedf["Units"] = tg.body.interpreted["records"][7]['unit']
                            if debug == 1:
                                pprint(rdecodedf)
                            position = position +1
                            self.Mbresults.append(rdecodedf)
                            self.Telegrams.insert(position,telegram+"freddo")
                            
                            
                            #Imp1
                            
                            rdecodedin1["ID"] = str(tg.body.interpreted["records"][10]['value'])
                            Status = str(int( tg.body.bodyHeader.interpreted['status'], 16))
                            rdecodedin1["Status"] = Status
                            rdecodedin1["CurrentValue"] = tg.body.interpreted["records"][11]['value']
                            rdecodedin1["SetDayValue"] = tg.body.interpreted["records"][11]['value']
                            rdecodedin1["LastRecived"] = tg.body.interpreted["records"][17]['value']
                            rdecodedin1["SetDay"] = tg.body.interpreted["records"][18]['value']
                            rdecodedin1["Units"] = tg.body.interpreted["records"][11]['unit']
                            if debug == 1:
                                pprint(rdecodedin1)
                            position = position +1
                            self.Mbresults.append(rdecodedin1)
                            self.Telegrams.insert(position,telegram +"imp1")
                            
                            #Imp2
                            rdecodedin2["ID"] = str(tg.body.interpreted["records"][13]['value'])
                            Status = str(int( tg.body.bodyHeader.interpreted['status'], 16))
                            rdecodedin2["Status"] = Status
                            rdecodedin2["CurrentValue"] = tg.body.interpreted["records"][14]['value']
                            rdecodedin2["SetDayValue"] = tg.body.interpreted["records"][14]['value']
                            rdecodedin2["LastRecived"] = tg.body.interpreted["records"][17]['value']
                            rdecodedin2["SetDay"] = tg.body.interpreted["records"][18]['value']
                            rdecodedin2["Units"] = tg.body.interpreted["records"][14]['unit']
                            if debug == 1:
                                pprint(rdecodedin2)
                            position = position +1 
                            self.Mbresults.append(rdecodedin2)
                            self.Telegrams.insert(position,telegram+"imp2")
                            
                        else:
                            self.Telegrams.remove(telegram)
                    elif self.Special =="7x9c2imp" and  (tg.body.bodyHeader.interpreted["medium"] == "0x4" or tg.body.bodyHeader.interpreted["medium"] == "0xc") :
                            
                        if tg.body.interpreted["records"][0]['type'] == 'VIFUnitExt.RSSI':
                            #Main energy
                            ID = tg.body.bodyHeader.interpreted['identification']
                            ID = ID.replace(",", "")
                            ID = ID.replace("0x", "")
                            ID = ID.replace(" ", "")
                            rdecoded["ID"] = ID
                            Status = str(int( tg.body.bodyHeader.interpreted['status'], 16))
                            rdecoded["Status"] = Status
                            rdecoded["CurrentValue"] = tg.body.interpreted["records"][1]['value']
                            rdecoded["SetDayValue"] = tg.body.interpreted["records"][1]['value']
                            rdecoded["LastRecived"] = tg.body.interpreted["records"][14]['value']
                            rdecoded["SetDay"] = tg.body.interpreted["records"][15]['value']
                            rdecoded["Units"] = tg.body.interpreted["records"][1]['unit']
                            if debug == 1:
                                pprint(rdecoded)
                            position = position +1 
                            self.Mbresults.append(rdecoded)
                            
                            
                            
                            
                            #Imp1
                            
                            rdecodedin1["ID"] = str(tg.body.interpreted["records"][7]['value'])
                            Status = str(int( tg.body.bodyHeader.interpreted['status'], 16))
                            rdecodedin1["Status"] = Status
                            rdecodedin1["CurrentValue"] = tg.body.interpreted["records"][8]['value']
                            rdecodedin1["SetDayValue"] = tg.body.interpreted["records"][9]['value']
                            rdecodedin1["LastRecived"] = tg.body.interpreted["records"][14]['value']
                            rdecodedin1["SetDay"] = tg.body.interpreted["records"][15]['value']
                            rdecodedin1["Units"] = tg.body.interpreted["records"][8]['unit']
                            if debug == 1:
                                pprint(rdecodedin1)
                            position = position +1 
                            self.Mbresults.append(rdecodedin1)
                            self.Telegrams.insert(position,telegram +"imp1")
                            
                            #Imp2
                            rdecodedin2["ID"] = str(tg.body.interpreted["records"][10]['value'])
                            Status = str(int( tg.body.bodyHeader.interpreted['status'], 16))
                            rdecodedin2["Status"] = Status
                            rdecodedin2["CurrentValue"] = tg.body.interpreted["records"][11]['value']
                            rdecodedin2["SetDayValue"] = tg.body.interpreted["records"][12]['value']
                            rdecodedin2["LastRecived"] = tg.body.interpreted["records"][14]['value']
                            rdecodedin2["SetDay"] = tg.body.interpreted["records"][15]['value']
                            rdecodedin2["Units"] = tg.body.interpreted["records"][11]['unit']
                            if debug == 1:
                                pprint(rdecodedin2)
                            position = position +1 
                            self.Mbresults.append(rdecodedin2)
                            self.Telegrams.insert(position,telegram+"imp2")

                        else:
                            self.Telegrams.remove(telegram)

                    else:
                        self.Telegrams.remove(telegram)
                        
                    continue


               
                try:
                    if  ("566" in  self.MetersType[0][0] or self.MetersType[0][1] == 1):#  and tg.body.bodyHeader.interpreted["medium"] == "0x8": #tg.interpreted['body']['header']['medium'] == "0x8" :
                        if debug == 1:
                            print("Decoding " + tg.body.bodyHeader.interpreted['identification'] )
                        ID = tg.body.bodyHeader.interpreted['identification']
                        ID = ID.replace(",", "")
                        ID = ID.replace("0x", "")
                        ID = ID.replace(" ", "")
                        rdecoded["ID"] = ID

                        Status = str(int( tg.body.bodyHeader.interpreted['status'], 16))
                        rdecoded["Status"] = Status
                        print(self.AesKey)
                        
                        bloks =  self.decrypt566(telegram,self.AesKey)
                        

                        CurrentValue,SetDayValue =  self.getreadings(bloks)
                        rdecoded["CurrentValue"] = CurrentValue
                        rdecoded["SetDayValue"] =  SetDayValue
                        rdecoded["LastRecived"] = date.today().strftime("%Y-%m-%dT00:00")#"2022-04-15T02:28"
                        rdecoded["SetDay"] = "2021-09-20"
                        rdecoded["Units"] = "MeasureUnit.HCA"

                        self.Mbresults.append(rdecoded)
                        position = position +1 
                        continue
                except:
                    pass
                  
                if not "body" in tg.interpreted.keys() or len(tg.body.interpreted["records"]) < int(recordnumber) + 1:
                    rdecoded["ID"] = self.extractmeterfromtelegram(telegram)
                    rdecoded["Status"] = "Error"
                    rdecoded["CurrentValue"] = "Error"
                    rdecoded["Units"] = "Error"
                    rdecoded["LastRecived"] = "Error"
                    rdecoded["SetDayValue"] = "Error"
                    rdecoded["SetDay"] = "Error"
                else:
                
                    if mixedrecords == 1:
                        meterid = self.extractmeterfromtelegram(telegram)
                        
                        if meterid in mixedrecordsdict.keys():
                            print(meterid)
                            
                            recordnumberc = mixedrecordsdict[meterid]
                        
                            
                        

                    if mixedlastrecived == 1:
                        meterid = self.extractmeterfromtelegram(telegram)
                        if meterid in mixedlastrecivedrecordic.keys():
                            
                            lastrecivedrecordc = mixedlastrecivedrecordic[meterid] 
                        
                            
                    if self.TryToGuess == 1:
                        recordnumberc,lastrecivedrecordc,setdayvaluerc , setdayrc = self.trytoguess(telegram)
                        if recordnumberc == -2:
                            if debug == 1:
                                print(colored("removing telegram " + telegram + " SecAddr " + self.extractmeterfromtelegram(telegram)  ,"red"))
                            self.Telegrams.remove(telegram)
                            continue
                        if debug == 1:
                            print("Current Record - LastRecicved: " + str(recordnumberc) + " - " + str(lastrecivedrecordc) + " - " + str(setdayvaluerc) + " - " + str(setdayrc))
                            #print(tg.body.interpreted["records"][int(setdayrc)]["value"])
                            #print(tg.body.interpreted["records"][int(setdayvaluerc)]["value"])
                        #exit(0)
                
                    if debug == 1:
                        
                        print(colored("pymbus RecordNumber: " + str(recordnumberc), "yellow"))
                        print(colored("pymbus ID: " + tg.body.interpreted['header']['identification'], "yellow"))
                        print(colored("pymbus Status " + tg.body.interpreted["header"]["status"], "yellow"))
                        print(colored(
                            "pymbus Current Value: " + str(tg.body.interpreted["records"][int(recordnumberc)]["value"]),
                            "yellow"))
                        print(colored(
                            "pymbus Current Unit: " + str(tg.body.interpreted["records"][int(recordnumberc)]["unit"]),
                            "yellow"))
                        print(colored("pymbus LastRecived: " + str(tg.body.interpreted["records"][int(lastrecivedrecordc)]["value"]),"yellow" ))
                        print(colored("pymbus Value at SetDay: " + str(tg.body.interpreted["records"][int(setdayvaluerc)]["value"]),"yellow" ))
                        print(colored("pymbus Set Day: " + str(tg.body.interpreted["records"][int(setdayrc)]["value"]),"yellow" ))
                
                    ID = str(tg.body.interpreted['header']['identification'])
                    ID = ID.replace(",", "")
                    ID = ID.replace("0x", "")
                    ID = ID.replace(" ", "")
                    rdecoded["ID"] = ID
                    
                    Status = str(int(tg.body.interpreted["header"]["status"], 16))
                    rdecoded["Status"] = Status
                    if int(recordnumberc) == -1:
                        CurrentValue =""
                        hitted = 1
                    else:
                        CurrentValue = str(tg.body.interpreted["records"][int(recordnumberc)]["value"])
                    
                    rdecoded["CurrentValue"] = CurrentValue
                    if int(recordnumberc) == -1:
                        Units = ""
                        hitted = 1
                    else:
                        Units = str(tg.body.interpreted["records"][int(recordnumberc)]["unit"])
                    
                    rdecoded["Units"] = Units
                    if  int(lastrecivedrecordc) == -1:
                        LastRecived = ""
                        hitted = 1
                    else:
                        LastRecived = tg.body.interpreted["records"][int(lastrecivedrecordc)]["value"]
                    
                    rdecoded["LastRecived"] = LastRecived

                    if setdayvaluerc == -1:
                        rdecoded["SetDayValue"] =""
                        hitted = 1
                    else:
                        rdecoded["SetDayValue"] = tg.body.interpreted["records"][int(setdayvaluerc)]["value"]
                        SetDayValue = tg.body.interpreted["records"][int(setdayvaluerc)]["value"]
                    if int(setdayrc) == -1:
                        rdecoded["SetDay"] = ""
                        hitted = 1
                    else:
                        rdecoded["SetDay"] = tg.body.interpreted["records"][int(setdayrc)]["value"]
                        SetDayDate =tg.body.interpreted["records"][int(setdayrc)]["value"]
                    
                    if  False: #"NONE" in Units :
                        self.Telegrams.remove(telegram)
                        continue
                if hitted == 1:
                    for single in self.Mbresults:
                        if rdecoded["ID"] in single.values():
                            exist = 1
                            if int(recordnumberc) == -1 :
                                pass
                            else :
                                single["CurrentValue"] = CurrentValue
                            if  int(lastrecivedrecordc) == -1 :
                                pass
                            else :
                                single["LastRecived"] = LastRecived
                            if setdayvaluerc == -1 :
                                pass
                            else :
                                single["SetDayValue"] = SetDayValue
                            if setdayrc == -1 :
                                pass
                            else :
                                single["SetDay"] = SetDayDate  
                            self.Telegrams.remove(telegram)
                            break     
                    
                if exist == 0:
                    self.Mbresults.append(rdecoded)
                    position = position +1 
            except:
                #raise
                print("Exception in " + telegram)
                self.Telegrams.remove(telegram)
                

    def set_rstm_now(self):
        today = date.today()
        now = datetime.now()
        rstm = "###AT+RSTM=" + str(today) + " " + now.strftime("%H:%M:%S") + ";"
        request = self.ascii_to_hex(rstm)
        conn = http.client.HTTPSConnection(self.RestServer)
        payload = "{\n  \"m2m:cin\": {\n\t\"lbl\": [ \"proto:udp\", \"port:5685\" ],\n    \"cnf\": \"text/plain:0\",\n  " \
                  "  \"con\": \"" + request.decode("utf-8") + "\"\n  }\n}"

        headers = {
            'X-M2M-RI': 'CIN_1625560933',
            'X-M2M-Origin': 'CCEDB769A-ad46824a',
            'Content-Type': 'application/vnd.onem2m-res+json;ty=4',
            'Accept': 'application/vnd.onem2m-res+json',
            'Authorization':  self.AuthString
        }
        conn.request("POST", "/onem2m/" + str(self.Modemnumber) + "/nbiot/outbox", payload, headers)
        res = conn.getresponse()
        data = res.read()
        if debug == 1:
            print(data.decode("utf-8"))
        conn.close()

    def lpw(self):
        request = self.ascii_to_hex("###AT+LPWR=1-" + str(self.Lpwsec) + "-1;")
        conn = http.client.HTTPSConnection(self.RestServer)
        payload = "{\n  \"m2m:cin\": {\n\t\"lbl\": [ \"proto:udp\", \"port:5685\" ],\n    \"cnf\": \"text/plain:0\",\n" \
                  "    \"con\": \"" + request.decode("utf-8") + "\"\n  }\n}"

        headers = {
            'X-M2M-RI': 'CIN_1625560933',
            'X-M2M-Origin': 'CCEDB769A-ad46824a',
            'Content-Type': 'application/vnd.onem2m-res+json;ty=4',
            'Accept': 'application/vnd.onem2m-res+json',
            'Authorization': self.AuthString
        }
        conn.request("POST", "/onem2m/" + str(self.Modemnumber) + "/nbiot/outbox", payload, headers)
        res = conn.getresponse()
        data = res.read()
        if debug == 1:
            print(data.decode("utf-8"))

    def std(self):
        conn = http.client.HTTPSConnection(self.RestServer)
        payload = "{\n  \"m2m:cin\": {\n\t\"lbl\": [ \"proto:udp\", \"port:5685\" ],\n    \"cnf\": \"text/plain:0\",\n" \
                  "    \"con\": \"6804046853FD5010B016\"\n  }\n}"
        headers = {
            'X-M2M-RI': 'CIN_1617968604',
            'X-M2M-Origin': 'CCEDB769A-ad46824a',
            'Content-Type': 'application/vnd.onem2m-res+json;ty=4',
            'Accept': 'application/vnd.onem2m-res+json',
            'Authorization':  self.AuthString
        }
        conn.request("POST", "/onem2m/" + str(self.Modemnumber) + "/nbiot/outbox", payload, headers)
        res = conn.getresponse()
        data = res.read()
        if debug == 1:
            print("STD")
            print(data.decode("utf-8"))
        conn.close()

    def sel(self, telegram):
        conn = http.client.HTTPSConnection(self.RestServer)
        payload = "{\n  \"m2m:cin\": {\n\t\"lbl\": [ \"proto:udp\", \"port:5685\" ],\n    \"cnf\": \"text/plain:0\",\n" \
                  "    \"con\": \"" + telegram + "\"\n  }\n}"
        # payload1 = "{\n  \"m2m:cin\": {\n\t\"lbl\": [ \"proto:udp\", \"port:5685\" ],\n    \"cnf\": \"text/plain:0\",\n
        # \"con\": \"680B0B6873FD5282414970FFFFFFFF3A16\"\n  }\n}"
        headers = {
            'X-M2M-RI': 'CIN_1617968469',
            'X-M2M-Origin': 'CCEDB769A-ad46824a',
            'Content-Type': 'application/vnd.onem2m-res+json;ty=4',
            'Accept': 'application/vnd.onem2m-res+json',
            'Authorization':  self.AuthString
        }
        conn.request("POST", "/onem2m/" + str(self.Modemnumber) + "/nbiot/outbox", payload, headers)
        res = conn.getresponse()
        data = res.read()
        # print(payload + "\n" + payload1 )
        if debug == 1:
            print("SEL")
            print(data.decode("utf-8"))
        conn.close()

    def lpw0(self):
        conn = http.client.HTTPSConnection(self.RestServer)
        payload = "{\n  \"m2m:cin\": {\n\t\"lbl\": [ \"proto:udp\", \"port:5685\" ],\n    \"cnf\": \"text/plain:0\",\n" \
                  "    \"con\": \"23232341542b4c5057523d302d302d303b\"\n  }\n}"
        headers = {
            'X-M2M-RI': 'CIN_1625559583',
            'X-M2M-Origin': 'CCEDB769A-ad46824a',
            'Content-Type': 'application/vnd.onem2m-res+json;ty=4',
            'Accept': 'application/vnd.onem2m-res+json',
            'Authorization':  self.AuthString
        }
        conn.request("POST", "/onem2m/" + str(self.Modemnumber) + "/nbiot/outbox", payload, headers)
        res = conn.getresponse()
        data = res.read()
        if debug == 1:
            print(data.decode("utf-8"))
        conn.close()

    def ans(self):
        conn = http.client.HTTPSConnection(self.RestServer)
        payload = ''
        headers = {
            'X-M2M-RI': 'CIN_1616163460',
            'X-M2M-Origin': 'CCEDB769A-ad46824a',
            'Content-Type': 'application/vnd.onem2m-res+json',
            'Accept': 'application/vnd.onem2m-res+json',
            'Authorization': self.AuthString
        }
        conn.request("GET", "/onem2m/" + str(self.Modemnumber) + "/nbiot/inbox/la", payload, headers)
        res = conn.getresponse()
        data = res.read()

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
        conn.close()
        return con, rn, rtime

    def anscustom(self,customsearch):
        conn = http.client.HTTPSConnection(self.RestServer)
        payload = ''
        headers = {
            'X-M2M-RI': 'CIN_1616163460',
            'X-M2M-Origin': 'CCEDB769A-ad46824a',
            'Content-Type': 'application/vnd.onem2m-res+json',
            'Accept': 'application/vnd.onem2m-res+json',
            'Authorization': self.AuthString
        }
        conn.request("GET", "/onem2m/" + str(self.Modemnumber) + "/nbiot/inbox/la", payload, headers)
        res = conn.getresponse()
        data = res.read()
        con, rn, rtime = customsearch(data)
        conn.close()
        return con, rn, rtime


    def mbcheksum(self,telegram):
        buff = telegram.replace(" ", "")
        if debug == 1:
            print(colored(telegram, "green"))
        buff = buff[8:len(buff) - 4]
        if debug == 1:
            print(colored(buff, "red"))
        a = []
        for i in range(0, len(buff), 2):
            a.append("0x" + buff[i:i + 2])
        if debug == 1:
            print(colored(a, "red"))
        res = 0
        for k in a:
            res = res + int(k, 16)
        result = str(hex(res))
        if debug == 1:
            print(colored(result, "red"))
        return result[-2:]

    def sendprecomputed(self, telegram):
        conn = http.client.HTTPSConnection(self.RestServer)
        if not isinstance(telegram,str):
            return
        payload = "{\n  \"m2m:cin\": {\n\t\"lbl\": [ \"proto:udp\", \"port:5685\" ],\n    \"cnf\": \"text/plain:0\",\n    \"con\": \"" + telegram + "\"\n  }\n}"
        headers = {
            'X-M2M-RI': 'CIN_1631194038',
            'X-M2M-Origin': 'CCEDB769A-ad46824a',
            'Content-Type': 'application/vnd.onem2m-res+json;ty=4',
            'Accept': 'application/vnd.onem2m-res+json',
            'Authorization':  self.AuthString
        }
        conn.request("POST", "/onem2m/" + str(self.Modemnumber) + "/nbiot/outbox", payload, headers)
        res = conn.getresponse()
        data = res.read()
        # print(payload + "\n" + payload1 )
        if debug == 1:
            print("SEL")
            print(data.decode("utf-8"))

    def computetelegram(self, ttype="REQ_UD2_FD", mid="-1"):
        if mid == '-1':
            if ttype == "REQ_UD2_FD":
                return "105BFD5816"
            if ttype == "SND_NKE":
                return "1040004016"
            if ttype == "REQ_UD2_00":
                return "105b005b16"
            if ttype == "SELECT_STD":
                return "6804046853FD5010B016"

        idreversed = str(mid)
        if len(idreversed) < 8 :
            idrev = "0"+idreversed
        if int(mid) > 255:

            if ttype == "SELECT_FD":
                prefix = "680B0B6873FD52"
                meterid = ""
                for i in range(8, 0, -2):
                    # print ( i )
                    # print (idreversed[i -2 :i])
                    idrev = idreversed[i - 2:i]
                    meterid = meterid + idrev
                if debug == 1:
                    print(idreversed + " -> " + meterid)

                Telegram = prefix + meterid + "FFFFFFFF" + "XX" + "16"
                checksum = self.mbcheksum(Telegram)
                Telegram = Telegram.replace("XX", checksum.upper())
                if debug == 1:
                    print(Telegram)
                return Telegram.upper()


    def trytorescue(self,rescued):
        import re
        counter = 0

        print("*****************")

        for match in re.finditer("68", rescued):
            a = match.start()
            # print(a)
            # telegram = rescue[a: a + 118]
            telegram = rescued[a: a + 2 * int("0x" + rescued[a + 2:a + 4], 16) + 8 + 4]
            meter = self.extractmeterfromtelegram(telegram.replace(" ", ""))
            if debug == 1:
                print("RTelegram :" + telegram + " has meter: " + meter)


            if debug == 1:
                print("rescued telegramm: " + telegram + " whith meter: " + meter)
            if telegram[-2:].rstrip() == "16":
                if debug == 1:
                    print(colored("check + tel line  : " + self.mbcheksum(telegram) + " " + telegram[-5:].replace(" ", ""),
                                  "green"))
                if self.mbcheksum(telegram) in telegram[-5:].replace(" ", ""):
                    counter = counter + 1
                    s = telegram
                    telegram = " ".join(s[i:i + 2] for i in range(0, len(s), 2))
                    if debug == 1:
                        print("*******************************************")
                        print("***  Dati : " + "From Rescue - " + telegram + "  ******************")
                        print("*******************************************")

                    print("add telegram from rescued: " + s)
                    self.Telegrams.append(s)
            else:
                print(colored("Invalid Telegram", "red"))
        print(colored("***************** rescued " + str(counter), "yellow"))

    def extractmeterfromtelegram(self,telegram):
        debug = 1
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

    def ascii_to_hex(self,ascii_str):
        hex_str = binascii.hexlify(ascii_str.encode())
        return hex_str

    def tocsv(self):

        csv = ""
        for res in self.Telegrams:
            strtl = bytes.fromhex(res)
            try:
                tg = meterbus.TelegramLong(strtl)
            except:
                print("Error")
                continue
            if self.TryToGuess == 1:
                currentrc,lastreciedrc = self.trytoguess(res)
            ID = str(tg.body.interpreted['header']['identification'])
            ID = ID.replace(",", "")
            ID = ID.replace("0x", "")
            ID = ID.replace(" ", "")
            csv = csv + ID + ";"
            Status = str(int(tg.body.interpreted["header"]["status"], 16))
            csv = csv + Status + ";"
            CurrentValue = str(tg.body.interpreted["records"][currentrc]["value"])
            csv = csv + CurrentValue + ";"
            Units = str(tg.body.interpreted["records"][currentrc]["unit"])
            csv = csv + Units + ";"
            SetDay = str(tg.body.interpreted["records"][3]["value"])
            csv = csv + SetDay + ";"
            ValueAtSetday = str(tg.body.interpreted["records"][4]["value"])
            csv = csv + ValueAtSetday + ";"
            LastRecived = str(tg.body.interpreted["records"][lastreciedrc]["value"])
            csv = csv + LastRecived + "\n"
        return csv

    def trytoguess(self,telegram):
        fieldallowd = ["MeasureUnit.HCA","MeasureUnit.WH","MeasureUnit.M3"]
        QUNDIS = ["QDS","LSE","HON"]
        strtl = bytes.fromhex(telegram)

           
        tg = meterbus.TelegramLong(strtl)
        count = 0
        lastreadrc = -1
        currentrc  = -1
        setdayrc = -1
        setdayvaluerc = -1
        isantenna = False
        if "SON" in tg.body.interpreted["header"]["manufacturer"]:
            if "10" in tg.body.interpreted["header"]["version"]:
                #556
                return(3,2,11,10)
            if tg.interpreted['body']['header']['medium'] == "0x7":
                #581
                
                return(2,1,2,1)
            if False: # tg.body.interpreted["header"]["version"] =="0x0":
                #531
                if tg.body.interpreted["header"]["access_no"]=="1":
                    return(2,-1,3,-1)
                if tg.body.interpreted["header"]["access_no"]=="3":
                    return(-1,3,-1,-1)
            if (tg.interpreted['body']['header']['medium'] =="0x4" or tg.interpreted['body']['header']['medium'] =="0xc")  and tg.body.interpreted["records"][-1]['function'] == 'FunctionType.MORE_RECORDS_FOLLOW':
                #739 liscio 
                return(1,8,2,8)
                if tg.body.interpreted["header"]["access_no"]=="73":
                    return(2,-1,3,-1)
                if tg.body.interpreted["header"]["access_no"]=="3":
                    return(1,17,2,18)
            
                

        if tg.body.interpreted["header"]["manufacturer"] in QUNDIS:
            a = tg.body.interpreted["records"]
            for record in a:
                if "BATT" in record["unit"]:
                    isantenna = True
                    currentrc = count
                if  record["type"] == "VIFUnit.DATE_TIME_GENERAL":
                    lastreadrc = count
                if record["unit"] in fieldallowd and currentrc == -1:
                    currentrc = count
                
                if not isantenna:
                    if  record["type"] == "VIFUnit.DATE" and setdayrc == -1 :
                        setdayrc = count
                        if count -1 != currentrc:
                            setdayvaluerc = count -1
                        else:
                            setdayvaluerc = count +1
                    
                else:
                    if  record["type"] == "VIFUnit.DATE" and setdayrc == -1 :
                        setdayrc = count
                    setdayvaluerc = currentrc
                if lastreadrc != -1 and currentrc != -1 and setdayrc != -1 and setdayvaluerc != -1 :
                        return currentrc,lastreadrc,setdayvaluerc,setdayrc        
                count = count +1 


        return (-2,-1 ,-1 ,-1)
    def initialvector(self,telegram):
        vct =  telegram[22:26]  + telegram[14:22] + telegram[26:30] + telegram[30:32] * 8
        return vct
    def getencriptedblocks(self,telegram):
        result = []
        pos = telegram.find("A0C5") + 4 
        
        result.append(telegram[pos:pos+32])
        offset = 2
        #print(str(len(telegram)) + str(pos + offset*36))
        while len(telegram) >(pos + offset*32) :
            result.append(telegram[pos  + (offset-1)*32 : pos   + offset*32])
            offset = offset+1

        return result
    def getreadings(self,bloks):
        debug = 0
        setdayhex = bloks[0][22:24] +  bloks[0][20:22] 
        currenthex = bloks[1][8:10] + bloks[1][6:8]
        if debug == 1:
            print(int(setdayhex,16))
            print(int(currenthex,16))
        return int(setdayhex,16),int(currenthex,16)
    
    def decrypt566(self,telegram,key):
        debug = 0
        AESK=binascii.unhexlify(key)
        AESBLK = self.getencriptedblocks(telegram)
        INITVECT = self.initialvector(telegram)
        results = []
        firsttime = True
        blkpos = 0
        
        for BLK in AESBLK:
            #pprint(AESBLK)
        
            #print(len(BLK))
            #pprint("8B52E0062B5DF4B26D16C28187ABC90A")
            AESB = binascii.unhexlify(BLK)
            rijn = AES.new(AESK, AES.MODE_ECB)
            decripted = rijn.decrypt(AESB)
            A=binascii.hexlify(decripted).decode('utf-8')
            if firsttime:
                B=INITVECT
                firsttime = False
            else:
                B = AESBLK[blkpos -1]
            blkpos = blkpos + 1
            #print(A)
            #print(B)
            C = hex(int(A, 16) ^ int(B, 16))
            if debug == 1:
                print( "Blocco Decriptato: " + C.replace("0x","").upper())
            results.append(C.replace("0x","").upper())
        return results