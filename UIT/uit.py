
# -*- coding: utf-8 -*-
import sys
import codecs
sys.path.insert(1,"../")

import http.client
from datetime import date
from datetime import datetime
from threading import get_ident
from xml.etree.ElementInclude import include
import sys
from numpy import count_nonzero
from termcolor import colored
import binascii
import meterbus
from  commonfuctionsui import *
import commonfunctions
import locale
from os import walk
import shutil

class Uit:
    condid = 0
    condata = []
    errors = []
    def __init__(self,condid,condata,errors):
        self.condid  = condid
        self.condata =condata
        self.errors = errors

if len(sys.argv) == 1:
    print("Manca l'argomento")
    exit(0)
#print(sys.argv[1])
#exit(0)
if sys.argv[1] == "modem":
    today = date.today().strftime("%Y%m")
    today = "202205"
    conds = getcondsid(today)
    pprint(conds)
    #exit(0)
    #conds = [[24192]]

    for condid in conds:
        #print("****************")
        #pprint(condid[0])
        #continue
        Apps = []
        MissedMeters = []
        condata = []
        condata = getcondata(condid[0])
        if not condata:
            continue
        #pprint(condata[0]['Città'])
        #continue
        #exit(0)
        mir  = getmetersinerror(condid[0],str(today))
        
        readedfromsql = commonfunctions.getmetersreaded([str(condid[0])], str(today),0)
        meterslist = commonfunctions.getmeterslist(condid[0],0,0,0)
        #pprint(meterslist)
        for hca in meterslist.keys():
            line = str(hca)
            if str(line) not in readedfromsql:
                MissedMeters.append(line)
                
       
        for meter in MissedMeters:

            a = {'SecAddr': int(meter) , 'CodiceErrore': '0', 'DataErrore': '', 'Lettura' : '' ,'DataLettura' :today}
            mir.append(a)
        
            
        if len(mir)> 1000:
            #del MyUit
            continue 
        pprint(mir)
    
        for Meter in mir:

            if debug ==1: 
                pprint(Meter)
                pprint(Meter['SecAddr'])
            App,MeterLoc = GetAppartmentDatafromMeter(condid[0],Meter['SecAddr'])
            
            if App:
                
                App[0].update(Meter)
                App[0].update(MeterLoc[0])
                Apps.extend(App)
                if debug ==1:
                    pprint(App)
    
        MyUit = Uit(condid,condata,Apps)
        if debug == 1:
            pprint(MyUit.condata)
            pprint(MyUit.errors)
        ArchiveAllBycondId(condid[0])

        for err in MyUit.errors:
        
            ToSql(err,MyUit.condata[0])
        del MyUit
else:
    for (dirpath, dirnames, filenames) in walk("./01LETTURE/" ):
        for filename in filenames:
            subdir =  "./01LETTURE/"
            filename =  filename
            print(filename)
            Apps = []
            MissedMeters = []
            condata = []
            
            condid = extractidfromfilename(filename)
            condata = getcondata(condid)
            
            
            type = getmeterstype(condid)
            meterslist = commonfunctions.getmeterslist(condid,0,0,0)
            if type == "Unknown":
                exit(1) 
            today = date.today().strftime("%Y%m%d")
            #today = "202204"
            if type == "AMR":
                
                fin = codecs.open(subdir + filename,"r","latin1")
                strrep = fin.read()
                meters = readstodict(strrep,"AMR")
                fin.close
                strcsv =""
            if "5" in type:
                fin = codecs.open(subdir + filename,"r","latin1")
                strcsv = fin.read()
                meters = readstodict(strcsv,type)
                fin.close
                strcsv =""
            #print(meterslist)

            for hca in meterslist.keys():
                
                line = str(hca)
                if str(line) not in meters:
                    MissedMeters.append(line)
            mir  = getmetersinerrorfromdict(meterslist , meters,type,today)
            for miss in MissedMeters:
                a = {'SecAddr': int(miss) , 'CodiceErrore': '0', 'DataErrore': '', 'Lettura' : '' ,'DataLettura' :today}
                mir.append(a)

            #print(mir)
            
            for Meter in mir:
                

                if debug ==1: 
                    pprint(Meter)
                    pprint(Meter['SecAddr'])
                App,MeterLoc = GetAppartmentDatafromMeter(condid,Meter['SecAddr'])
            
                if App:
                    
                    App[0].update(Meter)
                    App[0].update(MeterLoc[0])
                    Apps.extend(App)
                    if debug ==1:
                        pprint(App)
                
            MyUit = Uit(condid,condata,Apps)
            if debug == 1:
                pprint(MyUit.condata)
                pprint(MyUit.errors)
            ArchiveAllBycondId(condid)

            for err in MyUit.errors:
            
                ToSql(err,MyUit.condata[0])
            destination = isOkDestFolder(MyUit.condata[0])
            if destination:
                shutil.copyfile(subdir + filename,destination + "/" + "LETTURE/" + filename)
            del MyUit

    pass

