from Modem import Modem
from commonfunctions import *
import sys
from Config import configuration
from pprint import pprint
import commonfuctionsui
meterslist = {}
readingfiles = getfilespath("./LOCAL")
MyModem = Modem("","","","")
today =date.today().strftime("%Y%m")
debug =1

for readingfile in readingfiles:
    
    condid = commonfuctionsui.extractidfromfilename(readingfile.replace("./LOCAL/",""))
    pprint(readingfile)
    type = commonfuctionsui.getmeterstype(condid)
    
    meterslist = getmeterslist(condid,1,0,0)
    
    if ".REP" in readingfile.upper():
       
    
        
        MyModem.DoRepReding(readingfile,type)
        TelegramToSql(meterslist,MyModem.Telegrams,today,"","","",1,MyModem.Mbresults)
        #pprint(MyModem.Mbresults)
        #pprint(MyModem.Telegrams)


    if ".CSV" in readingfile.upper():
        meterslist = getmeterslist(condid,1,0,0)
        MyModem.DoCsvReading(readingfile,type)
        pprint(MyModem.Mbresults)
        #pprint(MyModem.Telegrams)
        #pprint(type)
        TelegramToSql(meterslist,MyModem.Telegrams,today,"","","",1,MyModem.Mbresults)
   
    MyModem.Clear()
    

    

