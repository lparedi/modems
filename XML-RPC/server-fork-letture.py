from xmlrpc.server import SimpleXMLRPCServer
import numpy as np #pip install numpy (utilizzato per la conversione int64)
from random import randint
import mysql.connector #pip install mysql-connector
import xml.etree.ElementTree as ET #di libreria standard
from lxml import etree #pip install lxml
import os
import csv
import time
from socketserver import ThreadingMixIn
def cancellaTemp(codice) :
    pathTemp = "/spool/MARIA/"+str(codice)+"/"
    FileTempList = os.listdir(pathTemp)
    nomiFiles = ["DatiCondominio.xml", "Appartamenti.xml", "Acqua.xml", "Antenne.xml", "Elementi.xml", "Energia.xml", "lettura.xml", "letturaacqua.xml", "letturaacquavecchia.xml", "LetturaCGenerali.xml", "letturaenergia.xml", "letturaenergiavecchia.xml", "TipoIntervento.xml", "Versione.xml"]
    try :
        for fileTemp in FileTempList :
            if fileTemp in nomiFiles :
                os.remove(pathTemp + fileTemp)
                print("file eliminato")
    except :
        return False
        #quit()
    return True

def CondIDFromCodSess(sessione):
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="raf_db",
        allow_local_infile = True
    )
    print(sessione)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT CondID From Sessions WHERE Sessione=" + str(sessione) + " ORDER BY ID DESC LIMIT 1" )
    result = mycursor.fetchone()
    mydb.close()
    print(result[0])
    return result[0]

class DatiAccesso:

    def controlloAccesso(self) :
        if self.accesso_effettuato == True :
            return True
        else :
            return False

    username = "21232f297a57a5a743894a0e4a801fc3"
    password = "5f4dcc3b5aa765d61d8327deb882cf99"
    accesso_effettuato = False #fino a quando accesso è uguale a False non si può fare altro
    pathTemp = r"/spool/MARIA/"
    codiceCondominio = 0 #contiene il codice del condominio da inserire o modificare
    codiceSessione = 0 #contiene il codice restituito da init()
    messaggioStato = "" #contiene lo stato corrente della sessione, dopo quit() viene cancellato
    indiciFiles = []


class MyFuncs:

    #ritorna False se l'accesso non viene eseguito correttamente, True se viene eseguito
    def accesso(self, username, password):
        if username == DatiAccesso.username and password == DatiAccesso.password :
            print("accesso eseguito")
            DatiAccesso.accesso_effettuato = True
            print ("Login eseguito\n")
            return True
        else :
            print("accesso negato")
            return False

    #ritorna un bool di controllo, False se non è stato eseguito l'accesso o se l'ID del condominio contiene caratteri non numerici
    #ritorna True e il codice d'accesso numerico se tutto va a buon fine
    def init(self, codice,username,password):
        dati = DatiAccesso()
        if  not (username == DatiAccesso.username and password == DatiAccesso.password) :
            #l'accesso non è stato ancora eseguito
            return False, 0
        else :
            try:
                DatiAccesso.codiceCondominio = int(codice)
            except:
                #errore nella composizione dell'ID del condominio inserito
                return False, 0

            sessione = randint(1,2147483647)

            DatiAccesso.codiceSessione = sessione
            DatiAccesso.messaggioStato = "Sessione inizializzata\n"
            DatiAccesso.pathTemp = r"/spool/MARIA/" + str(sessione) + "/"
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="raf_db",
                allow_local_infile = True
            )

            mycursor = mydb.cursor()
            mycursor.execute("INSERT INTO Sessions  (Sessione,CondID) values (" + str(sessione) + "," + codice +")")
            mydb.commit()
            mydb.close()
            #ritorna True e la chiave che verrà utilizzata d'ora in poi
            return True, sessione

    #questa funzione permette di caricare su server stringhe XML, con nome del file di appartenenza
    #la funzione gestisce sia la creazione di condomini nuovi che l'aggiornamento di condomini già esistenti
    def pushNewFiles(self, codice, nomeFile, XMLstring) :
        if codice =="0":
            return False
        pathTemp = "/spool/MARIA/" + codice + "/"
        if not os.path.isdir(pathTemp):
            os.mkdir(pathTemp)
        print("*******************" + pathTemp + " " + nomeFile )
        if False:#dati.controlloAccesso() == False :
            #accesso non eseguito
            return False, "accesso non eseguito"
        else:
            if True:#codice == dati.codiceSessione :
                try :
                    file_temp = open(pathTemp + nomeFile + ".xml", "w")
                except :
                    return False, "errore durante la creazione del file"

                try :
                    file_temp.write(XMLstring)
                except :
                    return False, "errore durante la scrittura nel file"

                file_temp.close()
                print( "Scrittura file " + nomeFile + " avvenuta con successo\n")
                return True, "scrittura avvenuta con successo"
            else :
                return False, "il codice di sessione non corrisponde"

    #questa funzione permette di caricare tutti i dati pushati tramite pushNewFiles sul db di riferimento
    #alla fine viene eseguita cancellaTemp() per svuotare la cartella dei file temporanei
    def set_datalettura(self,codice,datalettura):
        pathTemp = "/spool/MARIA/" + str(codice) + "/"
        if True:  # codice == DatiAccesso.codiceSessione and dati.controlloAccesso() == True :
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="raf_db",
                allow_local_infile=True
            )

        mycursor = mydb.cursor()
        contenutoVersione = []
        print("prima della richiesta del codice")
        codiceCondominio = CondIDFromCodSess(codice)
        IDCon = codiceCondominio
        print(codiceCondominio)
        ControlloCondQuery = "SELECT IdCONfk \nFROM sovrascrivi\nWHERE IdCONfk = \"" + str(codiceCondominio) + "\";"
        mycursor.execute(ControlloCondQuery)

        myresult = mycursor.fetchone()
        mycursor.close()
        IDcon = DatiAccesso.codiceCondominio

        if myresult != None:
            # nel database è stato già registrato questo condominio, quindi lo elimino e poi passo all'inserimento
            # print("Condominio presente nel database con id=" + DatiAccesso.codiceCondominio + ",procedere con la cancellazione e poi l'inserimento")
            mycursor = mydb.cursor()
            CondQuery = "UPDATE sovrascrivi SET DataLettura = '" + str(datalettura) + "' WHERE IdCONfk = " + str(IDcon) + ";"
            # print(CondQuery)
            mycursor.execute(CondQuery)
            mydb.commit()
            mycursor.close()
        else:
            # nel database è stato già registrato questo condominio, quindi lo elimino e poi passo all'inserimento
            # print("Condominio presente nel database con id=" + DatiAccesso.codiceCondominio + ",procedere con la cancellazione e poi l'inserimento")
            mycursor = mydb.cursor()
            CondQuery = "INSERT INTO  sovrascrivi  (DataLettura , idCONfk ) VALUES  ( '" + str(datalettura) + "' , " + str(IDcon) + ");"
            # print(CondQuery)
            mycursor.execute(CondQuery)
            mydb.commit()
            mycursor.close()
        return "OK"
    def set_datalettura_acqua(self,codice,datalettura):

        if True:  # codice == DatiAccesso.codiceSessione and dati.controlloAccesso() == True :
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="raf_db",
                allow_local_infile=True
            )

        mycursor = mydb.cursor()
        contenutoVersione = []
        print("prima della richiesta del codice")
        codiceCondominio = CondIDFromCodSess(codice)
        IDCon = codiceCondominio
        print(codiceCondominio)
        ControlloCondQuery = "SELECT IdCONfk \nFROM sovrascrivi\nWHERE IdCONfk = \"" + str(codiceCondominio) + "\";"
        mycursor.execute(ControlloCondQuery)

        myresult = mycursor.fetchone()
        mycursor.close()
        IDcon = DatiAccesso.codiceCondominio

        if myresult != None:
            # nel database è stato già registrato questo condominio, quindi lo elimino e poi passo all'inserimento
            # print("Condominio presente nel database con id=" + DatiAccesso.codiceCondominio + ",procedere con la cancellazione e poi l'inserimento")
            mycursor = mydb.cursor()
            CondQuery = "UPDATE sovrascrivi SET DataLetturaAcqua = '" + str(datalettura) + "' WHERE IdCONfk = " + str(IDcon) + ";"
            # print(CondQuery)
            mycursor.execute(CondQuery)
            mydb.commit()
            mycursor.close()
        else:
            # nel database è stato già registrato questo condominio, quindi lo elimino e poi passo all'inserimento
            # print("Condominio presente nel database con id=" + DatiAccesso.codiceCondominio + ",procedere con la cancellazione e poi l'inserimento")
            mycursor = mydb.cursor()
            CondQuery = "INSERT INTO  sovrascrivi  (DataLetturaAcqua , idCONfk ) VALUES  ( '" + str(datalettura) + "' , " + str(IDcon) + ");"
            # print(CondQuery)
            mycursor.execute(CondQuery)
            mydb.commit()
            mycursor.close()
        return "OK"

    def set_datalettura_energia(self,codice,datalettura):

        if True:  # codice == DatiAccesso.codiceSessione and dati.controlloAccesso() == True :
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="raf_db",
                allow_local_infile=True
            )

        mycursor = mydb.cursor()
        contenutoVersione = []
        print("prima della richiesta del codice")
        codiceCondominio = CondIDFromCodSess(codice)
        IDCon = codiceCondominio
        print(codiceCondominio)
        ControlloCondQuery = "SELECT IdCONfk \nFROM sovrascrivi\nWHERE IdCONfk = \"" + str(codiceCondominio) + "\";"
        mycursor.execute(ControlloCondQuery)

        myresult = mycursor.fetchone()
        mycursor.close()
        IDcon = DatiAccesso.codiceCondominio

        if myresult != None:
            # nel database è stato già registrato questo condominio, quindi lo elimino e poi passo all'inserimento
            # print("Condominio presente nel database con id=" + DatiAccesso.codiceCondominio + ",procedere con la cancellazione e poi l'inserimento")
            mycursor = mydb.cursor()
            CondQuery = "UPDATE sovrascrivi SET DataLetturaEnergia = '" + str(datalettura) + "' WHERE IdCONfk = " + str(IDcon) + ";"
            # print(CondQuery)
            mycursor.execute(CondQuery)
            mydb.commit()
            mycursor.close()
        else:
            # nel database è stato già registrato questo condominio, quindi lo elimino e poi passo all'inserimento
            # print("Condominio presente nel database con id=" + DatiAccesso.codiceCondominio + ",procedere con la cancellazione e poi l'inserimento")
            mycursor = mydb.cursor()
            CondQuery = "INSERT INTO  sovrascrivi  (DataLetturaEnergia , idCONfk ) VALUES  ( '" + str(datalettura) + "' , " + str(IDcon) + ");"
            # print(CondQuery)
            mycursor.execute(CondQuery)
            mydb.commit()
            mycursor.close()
        return "OK"

    def ins_data_db_letture(self, codice):
        #pid = os.fork()
        #if pid > 0:
        #while  os.path.isfile("/spool/MARIA/lock"):
            #time.sleep(2)
        #f=open("/spool/MARIA/lock", "w+")
        #f.close()
        print("DOPO")
        pathTemp="/spool/MARIA/"+str(codice)+ "/"
        if True:#codice == DatiAccesso.codiceSessione and dati.controlloAccesso() == True :
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="raf_db",
                allow_local_infile = True
            )

            #la parte di codice da eseguire si considera in base alla presenza o meno del condominio inserito all'interno del database
            #per controllare il modo migliore è controllare se l'id(univoco) del condominio esiste già nel database

            mycursor = mydb.cursor()
            contenutoVersione = []
            print("prima della richiesta del codice")
            codiceCondominio=CondIDFromCodSess(codice)
            IDCon =  codiceCondominio
            print(codiceCondominio)
            ControlloCondQuery = "SELECT IdCONpk \nFROM condomini\nWHERE IdCONpk = \"" + str(codiceCondominio) + "\";"
            mycursor.execute(ControlloCondQuery)

            myresult = mycursor.fetchone()
            mycursor.close()
            IDcon = DatiAccesso.codiceCondominio

            if myresult != None :
                #nel database è stato già registrato questo condominio, quindi lo elimino e poi passo all'inserimento
                #print("Condominio presente nel database con id=" + DatiAccesso.codiceCondominio + ",procedere con la cancellazione e poi l'inserimento")
                mycursor = mydb.cursor()
                CondQuery = "DELETE FROM letture WHERE IdCONfk = " + str(IDcon) + ";"
                #print(CondQuery)
                mycursor.execute(CondQuery)
                mydb.commit()
                mycursor.close()



            #importo i dati di lettura.xml
            XMLConPath = pathTemp + "/"+ "lettura.xml"
            print(XMLConPath)
            if os.path.exists(XMLConPath) :
                print ("file lettura.xml trovato\n")
                try :
                    size = os.path.getsize(XMLConPath)
                    if size < 500000:
                        mycursor = mydb.cursor()
                        LetQuery = "LOAD XML LOCAL INFILE \"" + XMLConPath + "\"\nINTO TABLE letture\nROWS IDENTIFIED BY '<lettura>'\nSET IdCONfk = " + str(IDcon) + ";"
                        #print(LetQuery)
                        mycursor.execute(LetQuery)
                        mydb.commit()
                        mycursor.close()
                        print ("file lettura.xml caricato nel db\n")
                    else :
                        #eseguo il parsing del file lettura.xml per recuperare i dati e incorporo nell'inserimento anche IDcon in IdCONfk
                        XMLConPath = "/spool/MARIA/" + str(codice) + "/lettura.xml"
                        #mycursor = mydb.cursor()
                        #print(XMLConPath)
                        tree = ET.parse(XMLConPath)
                        lettura = tree.findall("lettura")
                        #mycursor = mydb.cursor()
                        contenutoLettura = {}
                        a = 0
                        for l in lettura :
                            mycursor = mydb.cursor()
                            try :
                                F1 = l.find("F1").text
                                contenutoLettura['F1'] = F1
                            except:
                                pass
                            try :
                                F2 = l.find("F2").text
                                contenutoLettura['F2'] = F2
                            except:
                                pass
                            try :
                                F3 = l.find("F3").text
                                contenutoLettura['F3'] = F3
                            except:
                                pass
                            try :
                                F4 = l.find("F4").text
                                contenutoLettura['F4'] = F4
                            except:
                                pass
                            try :
                                F5 = l.find("F5").text
                                contenutoLettura['F5'] = F5
                            except:
                                pass
                            try :
                                F6 = l.find("F6").text
                                contenutoLettura['F6'] = F6
                            except:
                                pass
                            try :
                                F7 = l.find("F7").text
                                contenutoLettura['F7'] = F7
                            except:
                                pass
                            try :
                                F8 = l.find("F8").text
                                contenutoLettura['F8'] = F8
                            except:
                                pass
                            try :
                                F9 = l.find("F9").text
                                contenutoLettura['F9'] = F9
                            except:
                                pass
                            try :
                                F10 = l.find("F10").text
                                contenutoLettura['F10'] = F10
                            except:
                                pass
                            try :
                                F11 = l.find("F11").text
                                contenutoLettura['F11'] = F11
                            except:
                                pass
                            try :
                                F12 = l.find("F12").text
                                contenutoLettura['F12'] = F12
                            except:
                                pass
                            try :
                                F13 = l.find("F13").text
                                contenutoLettura['F13'] = F13
                            except:
                                pass
                            try :
                                F14 = l.find("F14").text
                                contenutoLettura['F14'] = F14
                            except:
                                pass
                            try :
                                F15 = l.find("F15").text
                                contenutoLettura['F15'] = F15
                            except:
                                pass
                            try :
                                F16 = l.find("F16").text
                                contenutoLettura['F16'] = F16
                            except:
                                pass
                            try :
                                F17 = l.find("F17").text
                                contenutoLettura['F17'] = F17
                            except:
                                pass
                            try :
                                F18 = l.find("F18").text
                                contenutoLettura['F18'] = F18
                            except:
                                pass
                            try :
                                F19 = l.find("F19").text
                                contenutoLettura['F19'] = F19
                            except:
                                pass
                            try :
                                F20 = l.find("F20").text
                                contenutoLettura['F20'] = F20
                            except:
                                pass
                            try :
                                F21 = l.find("F21").text
                                contenutoLettura['F21'] = F21
                            except:
                                pass
                            try :
                                F22 = l.find("F22").text
                                contenutoLettura['F22'] = F22
                            except:
                                pass
                            try :
                                F23 = l.find("F23").text
                                contenutoLettura['F23'] = F23
                            except:
                                pass
                            try :
                                F24 = l.find("F24").text
                                contenutoLettura['F24'] = F24
                            except:
                                pass
                            try :
                                F25 = l.find("F25").text
                                contenutoLettura['F25'] = F25
                            except:
                                pass
                            try :
                                F26 = l.find("F26").text
                                contenutoLettura['F26'] = F26
                            except:
                                pass
                            try :
                                F27 = l.find("F27").text
                                contenutoLettura['F27'] = F27
                            except:
                                pass
                            try :
                                F28 = l.find("F28").text
                                contenutoLettura['F28'] = F28
                            except:
                                pass
                            try :
                                F29 = l.find("F29").text
                                contenutoLettura['F29'] = F29
                            except:
                                pass
                            try :
                                F30 = l.find("F30").text
                                contenutoLettura['F30'] = F30
                            except:
                                pass
                            try :
                                F31 = l.find("F31").text
                                contenutoLettura['F31'] = F31
                            except:
                                pass
                            try :
                                F32 = l.find("F32").text
                                contenutoLettura['F32'] = F32
                            except:
                                pass
                            try :
                                F33 = l.find("F33").text
                                contenutoLettura['F33'] = F33
                            except:
                                pass
                            try :
                                F34 = l.find("F34").text
                                contenutoLettura['F34'] = F34
                            except:
                                pass
                            try :
                                F35 = l.find("F35").text
                                contenutoLettura['F35'] = F35
                            except:
                                pass
                            try :
                                F36 = l.find("F36").text
                                contenutoLettura['F36'] = F36
                            except:
                                pass
                            try :
                                F37 = l.find("F37").text
                                contenutoLettura['F37'] = F37
                            except:
                                pass
                            try :
                                F38 = l.find("F38").text
                                contenutoLettura['F38'] = F38
                            except:
                                pass
                            try :
                                F39 = l.find("F39").text
                                contenutoLettura['F39'] = F39
                            except:
                                pass
                            try :
                                F40 = l.find("F40").text
                                contenutoLettura['F40'] = F40
                            except:
                                pass
                            try :
                                F41 = l.find("F41").text
                                contenutoLettura['F41'] = F41
                            except:
                                pass
                            try :
                                F42 = l.find("F42").text
                                contenutoLettura['F42'] = F42
                            except:
                                pass
                            try :
                                F43 = l.find("F43").text
                                contenutoLettura['F43'] = F43
                            except:
                                pass
                            try :
                                F44 = l.find("F44").text
                                contenutoLettura['F44'] = F44
                            except:
                                pass
                            try :
                                F45 = l.find("F45").text
                                contenutoLettura['F45'] = F45
                            except:
                                pass
                            try :
                                F46 = l.find("F46").text
                                contenutoLettura['F46'] = F46
                            except:
                                pass
                            try :
                                F47 = l.find("F47").text
                                contenutoLettura['F47'] = F47
                            except:
                                pass
                            try :
                                F48 = l.find("F48").text
                                contenutoLettura['F48'] = F48
                            except:
                                pass
                            try :
                                F49 = l.find("F49").text
                                contenutoLettura['F49'] = F49
                            except:
                                pass
                            try :
                                F50 = l.find("F50").text
                                contenutoLettura['F50'] = F50
                            except:
                                pass
                            try :
                                F51 = l.find("F51").text
                                contenutoLettura['F51'] = F51
                            except:
                                pass
                            try :
                                F52 = l.find("F52").text
                                contenutoLettura['F52'] = F52
                            except:
                                pass
                            try :
                                F53 = l.find("F53").text
                                contenutoLettura['F53'] = F53
                            except:
                                pass
                            try :
                                F54 = l.find("F54").text
                                contenutoLettura['F54'] = F54
                            except:
                                pass
                            try :
                                F55 = l.find("F55").text
                                contenutoLettura['F55'] = F55
                            except:
                                pass
                            try :
                                F56 = l.find("F56").text
                                contenutoLettura['F56'] = F56
                            except:
                                pass
                            try :
                                F57 = l.find("F57").text
                                contenutoLettura['F57'] = F57
                            except:
                                pass
                            try :
                                F58 = l.find("F58").text
                                contenutoLettura['F58'] = F58
                            except:
                                pass
                            try :
                                F59 = l.find("F59").text
                                contenutoLettura['F59'] = F59
                            except:
                                pass
                            try :
                                F60 = l.find("F60").text
                                contenutoLettura['F60'] = F60
                            except:
                                pass
                            try :
                                F61 = l.find("F61").text
                                contenutoLettura['F61'] = F61
                            except:
                                pass
                            try :
                                F62 = l.find("F62").text
                                contenutoLettura['F62'] = F62
                            except:
                                pass
                            try :
                                F63 = l.find("F63").text
                                contenutoLettura['F63'] = F63
                            except:
                                pass
                            try :
                                F64 = l.find("F64").text
                                contenutoLettura['F64'] = F64
                            except:
                                pass
                            try :
                                F65 = l.find("F65").text
                                contenutoLettura['F65'] = F65
                            except:
                                pass
                            try :
                                F66 = l.find("F66").text
                                contenutoLettura['F66'] = F66
                            except:
                                pass
                            try :
                                F67 = l.find("F67").text
                                contenutoLettura['F67'] = F67
                            except:
                                pass
                            try :
                                F68 = l.find("F68").text
                                contenutoLettura['F68'] = F68
                            except:
                                pass
                            try :
                                CenKVal102 = l.find("CenKVal102").text
                                contenutoLettura['CenKVal102'] = CenKVal102
                            except:
                                pass
                            try :
                                ZDatEvent = l.find("ZDatEvent").text
                                contenutoLettura['ZDatEvent'] = ZDatEvent
                            except :
                                pass
                            try :
                                KKunderNr101 = l.find("KKunderNr101").text
                                contenutoLettura['KKunderNr101'] = KKunderNr101
                            except :
                                pass
                            try :
                                SFehler250 = l.find("SFehler250").text
                                contenutoLettura['SFehler250'] = SFehler250
                            except :
                                pass
                            try :
                                Durata = l.find("Durata").text
                                contenutoLettura['Durata'] = Durata
                            except :
                                pass

                            query1 = "INSERT INTO letture ("
                            query2 = "VALUES ("
                            for key, value in contenutoLettura.items() :
                                query1 = query1 + key + ","
                                query2 = query2 + "'" + value + "',"
                            query1 = query1 + "IdCONfk ) "
                            query2 = query2 + str(IDcon) + ");"

                            CondQuery = query1 + query2

                            mycursor.execute(CondQuery)
                            mydb.commit()
                            print("query eseguita inserimento lettura " + str(a))
                            a = a + 1
                            mycursor.close()

                        print ("file lettura.xml caricato nel db\n")



                    print("PASSATO DA QUA")



                    #collego le letture ai ripartitori in "elementi"
                    mycursor = mydb.cursor()
                    letQuery1 = "UPDATE letture, elementi \nSET letture.IdELEfk = elementi.IdELEpk \nWHERE elementi.Ripartitore = letture.KKunderNr101 AND letture.IdCONfk = " + str(IDcon) + " AND elementi.IdCONfk = " + str(IDcon) + ";"
                    #print(letQuery1)
                    mycursor.execute(letQuery1)
                    mydb.commit()
                    mycursor.close()
                    print("update letture ed elementi effettuato")



                except :
                    print ("file lettura.xml non caricato nel db, errore o eccezione\n")
            else :
                print ("file lettura.xml non trovato\n")


            #print("\n")


            #importo i dati di energia.xml
            #print("\n")


            #salvo tutti i files nella tabella dedicata

            # nomiFiles = ["DatiCondominio", "Appartamenti", "Acqua", "Antenne", "Elementi", "Energia", "lettura", "letturaacqua", "letturaacquavecchia", "LetturaCGenerali", "letturaenergia", "letturaenergiavecchia", "TipoIntervento", "Versione"]
            # #print("Non sono stati riscontrati errori nel caricamento dei dati, procedo con il salvataggio dei file nella tabella dedicata\n")
            #
            # try :
            #     mycursor = mydb.cursor()
            #     CaricaFilesQuery = "INSERT INTO files_backup (Data_Salvataggio, DatiCondominio, Appartamenti, Acqua, Antenne, Elementi, Energia, lettura, letturaacqua, letturaacquavecchia, LetturaCGenerali, letturaenergia, letturaenergiavecchia, TipoIntervento, Versione) VALUES (NOW()"
            #     a = 0
            #     queryPart1 = "INSERT INTO files_backup (Data_Salvataggio, "
            #     queryPart2 = "IdCONfk) VALUES (NOW(), "
            #     queryPart3 = str(IDcon) + ");"
            #
            #     for nomeFile in nomiFiles:
            #         if os.path.exists(pathTemp + "/"+ nomeFile + ".xml"):
            #             queryPart1 += nomeFile + ","
            #             queryPart2 += "LOAD_FILE(\"" + pathTemp+ "/" + nomeFile + ".xml\"),"
            #             print ("file " + nomeFile + ".xml caricato nel db\n")
            #
            #     CaricaFilesQuery = queryPart1 + queryPart2 + queryPart3
            #     print("\n\n\n\n\n\n" + CaricaFilesQuery + "\n\n\n\n\n\n\n")
            #     mycursor.execute(CaricaFilesQuery)
            #     mydb.commit()
            #     mycursor.close()
            #
            #     print ("inserimento dei dati nel db avvenuto con successo\n")
            # except :
            #     print ("errore nel caricamento dei file di backup nella tabella files_backup\n")
            #
            # mydb.close()


            if cancellaTemp(codice) :
                print ("cancellazione dei file temporanei avvenuta con successo\n")
                #os.remove("/spool/MARIA/lock")
                return True, "Inserimento nel db avvenuto con SUCCESSO, cancellazione dei file temporanei avvenuta con successo"
            else :
                print ("errore o eccezione durante la cancellazione dei file temporanei\n")
                return False, "Inserimento nel db avvenuto con SUCCESSO, ERRORE o Eccezione trovata durante la cancellazione dei file temporanei"

    def ins_data_db_letture_modem(self, codice):
        # pid = os.fork()
        # if pid > 0:
        # while  os.path.isfile("/spool/MARIA/lock"):
        # time.sleep(2)
        # f=open("/spool/MARIA/lock", "w+")
        # f.close()
        print("DOPO")
        pathTemp = "/spool/MARIA/" + str(codice) + "/"
        if True:  # codice == DatiAccesso.codiceSessione and dati.controlloAccesso() == True :
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="raf_db",
                allow_local_infile=True
            )

            # la parte di codice da eseguire si considera in base alla presenza o meno del condominio inserito all'interno del database
            # per controllare il modo migliore è controllare se l'id(univoco) del condominio esiste già nel database

            mycursor = mydb.cursor()
            contenutoVersione = []
            print("prima della richiesta del codice")
            codiceCondominio = CondIDFromCodSess(codice)
            IDCon = codiceCondominio
            print(codiceCondominio)
            ControlloCondQuery = "SELECT IdCONpk \nFROM condomini\nWHERE IdCONpk = \"" + str(codiceCondominio) + "\";"
            mycursor.execute(ControlloCondQuery)

            myresult = mycursor.fetchone()
            mycursor.close()
            IDcon = DatiAccesso.codiceCondominio

            if myresult != None:
                # nel database è stato già registrato questo condominio, quindi lo elimino e poi passo all'inserimento
                # print("Condominio presente nel database con id=" + DatiAccesso.codiceCondominio + ",procedere con la cancellazione e poi l'inserimento")
                mycursor = mydb.cursor()
                CondQuery = "DELETE FROM letture_modem WHERE IdCONfk = " + str(IDcon) + ";"
                # print(CondQuery)
                mycursor.execute(CondQuery)
                mydb.commit()
                mycursor.close()

            # importo i dati di lettura.xml
            XMLConPath = pathTemp + "/" + "lettura.xml"
            print(XMLConPath)
            if os.path.exists(XMLConPath):
                print("file lettura.xml trovato\n")
                try:
                    size = os.path.getsize(XMLConPath)
                    if size < 500000:
                        mycursor = mydb.cursor()
                        LetQuery = "LOAD XML LOCAL INFILE \"" + XMLConPath + "\"\nINTO TABLE letture_modem\nROWS IDENTIFIED BY '<lettura>'\nSET IdCONfk = " + str(
                            IDcon) + ";"
                        # print(LetQuery)
                        mycursor.execute(LetQuery)
                        mydb.commit()
                        mycursor.close()
                        print("file lettura.xml caricato nel db\n")
                    else:
                        # eseguo il parsing del file lettura.xml per recuperare i dati e incorporo nell'inserimento anche IDcon in IdCONfk
                        XMLConPath = "/spool/MARIA/" + str(codice) + "/lettura.xml"
                        # mycursor = mydb.cursor()
                        # print(XMLConPath)
                        tree = ET.parse(XMLConPath)
                        lettura = tree.findall("lettura")
                        # mycursor = mydb.cursor()
                        contenutoLettura = {}
                        a = 0
                        for l in lettura:
                            mycursor = mydb.cursor()
                            try:
                                F1 = l.find("F1").text
                                contenutoLettura['F1'] = F1
                            except:
                                pass
                            try:
                                F2 = l.find("F2").text
                                contenutoLettura['F2'] = F2
                            except:
                                pass
                            try:
                                F3 = l.find("F3").text
                                contenutoLettura['F3'] = F3
                            except:
                                pass
                            try:
                                F4 = l.find("F4").text
                                contenutoLettura['F4'] = F4
                            except:
                                pass
                            try:
                                F5 = l.find("F5").text
                                contenutoLettura['F5'] = F5
                            except:
                                pass
                            try:
                                F6 = l.find("F6").text
                                contenutoLettura['F6'] = F6
                            except:
                                pass
                            try:
                                F7 = l.find("F7").text
                                contenutoLettura['F7'] = F7
                            except:
                                pass
                            try:
                                F8 = l.find("F8").text
                                contenutoLettura['F8'] = F8
                            except:
                                pass
                            try:
                                F9 = l.find("F9").text
                                contenutoLettura['F9'] = F9
                            except:
                                pass
                            try:
                                F10 = l.find("F10").text
                                contenutoLettura['F10'] = F10
                            except:
                                pass
                            try:
                                F11 = l.find("F11").text
                                contenutoLettura['F11'] = F11
                            except:
                                pass
                            try:
                                F12 = l.find("F12").text
                                contenutoLettura['F12'] = F12
                            except:
                                pass
                            try:
                                F13 = l.find("F13").text
                                contenutoLettura['F13'] = F13
                            except:
                                pass
                            try:
                                F14 = l.find("F14").text
                                contenutoLettura['F14'] = F14
                            except:
                                pass
                            try:
                                F15 = l.find("F15").text
                                contenutoLettura['F15'] = F15
                            except:
                                pass
                            try:
                                F16 = l.find("F16").text
                                contenutoLettura['F16'] = F16
                            except:
                                pass
                            try:
                                F17 = l.find("F17").text
                                contenutoLettura['F17'] = F17
                            except:
                                pass
                            try:
                                F18 = l.find("F18").text
                                contenutoLettura['F18'] = F18
                            except:
                                pass
                            try:
                                F19 = l.find("F19").text
                                contenutoLettura['F19'] = F19
                            except:
                                pass
                            try:
                                F20 = l.find("F20").text
                                contenutoLettura['F20'] = F20
                            except:
                                pass
                            try:
                                F21 = l.find("F21").text
                                contenutoLettura['F21'] = F21
                            except:
                                pass
                            try:
                                F22 = l.find("F22").text
                                contenutoLettura['F22'] = F22
                            except:
                                pass
                            try:
                                F23 = l.find("F23").text
                                contenutoLettura['F23'] = F23
                            except:
                                pass
                            try:
                                F24 = l.find("F24").text
                                contenutoLettura['F24'] = F24
                            except:
                                pass
                            try:
                                F25 = l.find("F25").text
                                contenutoLettura['F25'] = F25
                            except:
                                pass
                            try:
                                F26 = l.find("F26").text
                                contenutoLettura['F26'] = F26
                            except:
                                pass
                            try:
                                F27 = l.find("F27").text
                                contenutoLettura['F27'] = F27
                            except:
                                pass
                            try:
                                F28 = l.find("F28").text
                                contenutoLettura['F28'] = F28
                            except:
                                pass
                            try:
                                F29 = l.find("F29").text
                                contenutoLettura['F29'] = F29
                            except:
                                pass
                            try:
                                F30 = l.find("F30").text
                                contenutoLettura['F30'] = F30
                            except:
                                pass
                            try:
                                F31 = l.find("F31").text
                                contenutoLettura['F31'] = F31
                            except:
                                pass
                            try:
                                F32 = l.find("F32").text
                                contenutoLettura['F32'] = F32
                            except:
                                pass
                            try:
                                F33 = l.find("F33").text
                                contenutoLettura['F33'] = F33
                            except:
                                pass
                            try:
                                F34 = l.find("F34").text
                                contenutoLettura['F34'] = F34
                            except:
                                pass
                            try:
                                F35 = l.find("F35").text
                                contenutoLettura['F35'] = F35
                            except:
                                pass
                            try:
                                F36 = l.find("F36").text
                                contenutoLettura['F36'] = F36
                            except:
                                pass
                            try:
                                F37 = l.find("F37").text
                                contenutoLettura['F37'] = F37
                            except:
                                pass
                            try:
                                F38 = l.find("F38").text
                                contenutoLettura['F38'] = F38
                            except:
                                pass
                            try:
                                F39 = l.find("F39").text
                                contenutoLettura['F39'] = F39
                            except:
                                pass
                            try:
                                F40 = l.find("F40").text
                                contenutoLettura['F40'] = F40
                            except:
                                pass
                            try:
                                F41 = l.find("F41").text
                                contenutoLettura['F41'] = F41
                            except:
                                pass
                            try:
                                F42 = l.find("F42").text
                                contenutoLettura['F42'] = F42
                            except:
                                pass
                            try:
                                F43 = l.find("F43").text
                                contenutoLettura['F43'] = F43
                            except:
                                pass
                            try:
                                F44 = l.find("F44").text
                                contenutoLettura['F44'] = F44
                            except:
                                pass
                            try:
                                F45 = l.find("F45").text
                                contenutoLettura['F45'] = F45
                            except:
                                pass
                            try:
                                F46 = l.find("F46").text
                                contenutoLettura['F46'] = F46
                            except:
                                pass
                            try:
                                F47 = l.find("F47").text
                                contenutoLettura['F47'] = F47
                            except:
                                pass
                            try:
                                F48 = l.find("F48").text
                                contenutoLettura['F48'] = F48
                            except:
                                pass
                            try:
                                F49 = l.find("F49").text
                                contenutoLettura['F49'] = F49
                            except:
                                pass
                            try:
                                F50 = l.find("F50").text
                                contenutoLettura['F50'] = F50
                            except:
                                pass
                            try:
                                F51 = l.find("F51").text
                                contenutoLettura['F51'] = F51
                            except:
                                pass
                            try:
                                F52 = l.find("F52").text
                                contenutoLettura['F52'] = F52
                            except:
                                pass
                            try:
                                F53 = l.find("F53").text
                                contenutoLettura['F53'] = F53
                            except:
                                pass
                            try:
                                F54 = l.find("F54").text
                                contenutoLettura['F54'] = F54
                            except:
                                pass
                            try:
                                F55 = l.find("F55").text
                                contenutoLettura['F55'] = F55
                            except:
                                pass
                            try:
                                F56 = l.find("F56").text
                                contenutoLettura['F56'] = F56
                            except:
                                pass
                            try:
                                F57 = l.find("F57").text
                                contenutoLettura['F57'] = F57
                            except:
                                pass
                            try:
                                F58 = l.find("F58").text
                                contenutoLettura['F58'] = F58
                            except:
                                pass
                            try:
                                F59 = l.find("F59").text
                                contenutoLettura['F59'] = F59
                            except:
                                pass
                            try:
                                F60 = l.find("F60").text
                                contenutoLettura['F60'] = F60
                            except:
                                pass
                            try:
                                F61 = l.find("F61").text
                                contenutoLettura['F61'] = F61
                            except:
                                pass
                            try:
                                F62 = l.find("F62").text
                                contenutoLettura['F62'] = F62
                            except:
                                pass
                            try:
                                F63 = l.find("F63").text
                                contenutoLettura['F63'] = F63
                            except:
                                pass
                            try:
                                F64 = l.find("F64").text
                                contenutoLettura['F64'] = F64
                            except:
                                pass
                            try:
                                F65 = l.find("F65").text
                                contenutoLettura['F65'] = F65
                            except:
                                pass
                            try:
                                F66 = l.find("F66").text
                                contenutoLettura['F66'] = F66
                            except:
                                pass
                            try:
                                F67 = l.find("F67").text
                                contenutoLettura['F67'] = F67
                            except:
                                pass
                            try:
                                F68 = l.find("F68").text
                                contenutoLettura['F68'] = F68
                            except:
                                pass
                            try:
                                CenKVal102 = l.find("CenKVal102").text
                                contenutoLettura['CenKVal102'] = CenKVal102
                            except:
                                pass
                            try:
                                ZDatEvent = l.find("ZDatEvent").text
                                contenutoLettura['ZDatEvent'] = ZDatEvent
                            except:
                                pass
                            try:
                                KKunderNr101 = l.find("KKunderNr101").text
                                contenutoLettura['KKunderNr101'] = KKunderNr101
                            except:
                                pass
                            try:
                                SFehler250 = l.find("SFehler250").text
                                contenutoLettura['SFehler250'] = SFehler250
                            except:
                                pass
                            try:
                                Durata = l.find("Durata").text
                                contenutoLettura['Durata'] = Durata
                            except:
                                pass

                            query1 = "INSERT INTO letture_modem ("
                            query2 = "VALUES ("
                            for key, value in contenutoLettura.items():
                                query1 = query1 + key + ","
                                query2 = query2 + "'" + value + "',"
                            query1 = query1 + "IdCONfk ) "
                            query2 = query2 + str(IDcon) + ");"

                            CondQuery = query1 + query2

                            mycursor.execute(CondQuery)
                            mydb.commit()
                            print("query eseguita inserimento lettura " + str(a))
                            a = a + 1
                            mycursor.close()

                        print("file lettura.xml caricato nel db\n")

                    print("PASSATO DA QUA")

                    # # collego le letture ai ripartitori in "elementi"
                    # mycursor = mydb.cursor()
                    # letQuery1 = "UPDATE letture, elementi \nSET letture.IdELEfk = elementi.IdELEpk \nWHERE elementi.Ripartitore = letture.KKunderNr101 AND letture.IdCONfk = " + str(
                    #     IDcon) + " AND elementi.IdCONfk = " + str(IDcon) + ";"
                    # # print(letQuery1)
                    # mycursor.execute(letQuery1)
                    # mydb.commit()
                    # mycursor.close()
                    # print("update letture ed elementi effettuato")



                except:
                    print("file lettura.xml non caricato nel db, errore o eccezione\n")
            else:
                print("file lettura.xml non trovato\n")

            # print("\n")

            # importo i dati di energia.xml
            # print("\n")

            # salvo tutti i files nella tabella dedicata

            nomiFiles = ["DatiCondominio", "Appartamenti", "Acqua", "Antenne", "Elementi", "Energia", "lettura",
                         "letturaacqua", "letturaacquavecchia", "LetturaCGenerali", "letturaenergia",
                         "letturaenergiavecchia", "TipoIntervento", "Versione"]
            # print("Non sono stati riscontrati errori nel caricamento dei dati, procedo con il salvataggio dei file nella tabella dedicata\n")

            # try:
            #     mycursor = mydb.cursor()
            #     CaricaFilesQuery = "INSERT INTO files_backup (Data_Salvataggio, DatiCondominio, Appartamenti, Acqua, Antenne, Elementi, Energia, lettura, letturaacqua, letturaacquavecchia, LetturaCGenerali, letturaenergia, letturaenergiavecchia, TipoIntervento, Versione) VALUES (NOW()"
            #     a = 0
            #     queryPart1 = "INSERT INTO files_backup (Data_Salvataggio, "
            #     queryPart2 = "IdCONfk) VALUES (NOW(), "
            #     queryPart3 = str(IDcon) + ");"
            #
            #     for nomeFile in nomiFiles:
            #         if os.path.exists(pathTemp + "/" + nomeFile + ".xml"):
            #             queryPart1 += nomeFile + ","
            #             queryPart2 += "LOAD_FILE(\"" + pathTemp + "/" + nomeFile + ".xml\"),"
            #             print("file " + nomeFile + ".xml caricato nel db\n")
            #
            #     CaricaFilesQuery = queryPart1 + queryPart2 + queryPart3
            #     print("\n\n\n\n\n\n" + CaricaFilesQuery + "\n\n\n\n\n\n\n")
            #     mycursor.execute(CaricaFilesQuery)
            #     mydb.commit()
            #     mycursor.close()
            #
            #     print("inserimento dei dati nel db avvenuto con successo\n")
            # except:
            #     print("errore nel caricamento dei file di backup nella tabella files_backup\n")
            #
            # mydb.close()

            if cancellaTemp(codice):
                print("cancellazione dei file temporanei avvenuta con successo\n")
                # os.remove("/spool/MARIA/lock")
                return True, "Inserimento nel db avvenuto con SUCCESSO, cancellazione dei file temporanei avvenuta con successo"
            else:
                print("errore o eccezione durante la cancellazione dei file temporanei\n")
                return False, "Inserimento nel db avvenuto con SUCCESSO, ERRORE o Eccezione trovata durante la cancellazione dei file temporanei"
    #funzione interna usata da ins_data_db() per cancellare i file temporanei dal folder predefinito

    def ins_data_db_lettura_acqua(self, codice):
        # pid = os.fork()
        # if pid > 0:
        # while  os.path.isfile("/spool/MARIA/lock"):
        # time.sleep(2)
        # f=open("/spool/MARIA/lock", "w+")
        # f.close()
        print("DOPO")
        pathTemp = "/spool/MARIA/" + str(codice) + "/"
        if True:  # codice == DatiAccesso.codiceSessione and dati.controlloAccesso() == True :
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="raf_db",
                allow_local_infile=True
            )

            # la parte di codice da eseguire si considera in base alla presenza o meno del condominio inserito all'interno del database
            # per controllare il modo migliore è controllare se l'id(univoco) del condominio esiste già nel database

            mycursor = mydb.cursor()
            contenutoVersione = []
            print("prima della richiesta del codice")
            codiceCondominio = CondIDFromCodSess(codice)
            print(codiceCondominio)
            ControlloCondQuery = "SELECT IdCONpk \nFROM condomini\nWHERE IdCONpk = \"" + str(codiceCondominio) + "\";"
            mycursor.execute(ControlloCondQuery)

            myresult = mycursor.fetchone()
            mycursor.close()
            IDcon = DatiAccesso.codiceCondominio

            if myresult != None:
                # nel database è stato già registrato questo condominio, quindi lo elimino e poi passo all'inserimento
                # print("Condominio presente nel database con id=" + DatiAccesso.codiceCondominio + ",procedere con la cancellazione e poi l'inserimento")
                mycursor = mydb.cursor()
                CondQuery = "DELETE FROM lettura_acqua_modem WHERE IdCONfk = " + str(IDcon) + ";"
                # print(CondQuery)
                mycursor.execute(CondQuery)
                mydb.commit()
                mycursor.close()

            # importo i dati di letturaacqua nella tabella d'appoggio
            XMLConPath = pathTemp + "/" + "letturaacqua.xml"
            if os.path.exists(XMLConPath):
                print("file letturaacqua.xml trovato\n")
                try:

                    mycursor = mydb.cursor()
                    SvuotaAppQuery = "DELETE FROM appoggio_letture_acqua"
                    print(SvuotaAppQuery)
                    mycursor.execute(SvuotaAppQuery)
                    mydb.commit()
                    mycursor.close()


                    mycursor = mydb.cursor()
                    LetAcquaQuery = "LOAD XML LOCAL INFILE \"" + XMLConPath + "\"\nINTO TABLE appoggio_letture_acqua\nROWS IDENTIFIED BY '<letturaacqua>'\nSET IdCONfk = " + str(
                        IDcon) + ";"
                    print(LetAcquaQuery)
                    mycursor.execute(LetAcquaQuery)
                    mydb.commit()
                    mycursor.close()

                    # print("\n")

                    mycursor = mydb.cursor()
                    EliminaValoriInvalidi = "DELETE FROM appoggio_letture_acqua\nWHERE (F1 IS NULL AND F2 IS NULL AND F3 IS NULL);"
                    print(EliminaValoriInvalidi)
                    mycursor.execute(EliminaValoriInvalidi)
                    mydb.commit()
                    mycursor.close()

                    # print("\n")

                    # collego le letture energia alla tabella Energia
                    mycursor = mydb.cursor()
                    letQuery1 = "UPDATE acqua, appoggio_letture_acqua \nSET appoggio_letture_acqua.IdACQfk = acqua.IdACQpk\nWHERE acqua.Seriale = appoggio_letture_acqua.F1 AND appoggio_letture_acqua.IdCONfk = " + str(
                        IDcon) + " AND acqua.IdCONfk = " + str(IDcon) + ";"
                    print(letQuery1)
                    mycursor.execute(letQuery1)
                    mydb.commit()
                    mycursor.close()


                    # fix letture_acqua
                    mycursor = mydb.cursor()
                    LetEnergiaQuery = "UPDATE appoggio_letture_acqua SET F3 ='' WHERE F3 is Null "
                    print(LetEnergiaQuery)
                    mycursor.execute(LetEnergiaQuery)
                    mydb.commit()
                    mycursor.close()


                    # fix letture_acqua
                    mycursor = mydb.cursor()
                    LetEnergiaQuery = "UPDATE appoggio_letture_acqua SET F2 ='' WHERE F2 is Null "
                    print(LetEnergiaQuery)
                    mycursor.execute(LetEnergiaQuery)
                    mydb.commit()
                    mycursor.close()

                    # importo i dati nella vera tabella letture_energia
                    mycursor = mydb.cursor()
                    letQuery1 = "INSERT INTO lettura_acqua_modem (SELECT DISTINCT * FROM appoggio_letture_acqua);"
                    print(letQuery1)
                    mycursor.execute(letQuery1)
                    mydb.commit()
                    mycursor.close()

                    # svuoto la tabella di appoggio
                    mycursor = mydb.cursor()
                    SvuotaAppQuery = "DELETE FROM appoggio_letture_acqua"
                    print(SvuotaAppQuery)
                    mycursor.execute(SvuotaAppQuery)
                    mydb.commit()
                    mycursor.close()
                    print("file letturaacqua.xml caricato nel db\n")
                except:
                    print("file letturaacqua.xml non caricato nel db, errore o eccezione\n")
                    pass
            else:
                print("file letturaacqua.xml non trovato\n")

            # print("\n")

            # nomiFiles = ["DatiCondominio", "Appartamenti", "Acqua", "Antenne", "Elementi", "Energia", "lettura",
            #              "letturaacqua", "letturaacquavecchia", "LetturaCGenerali", "letturaenergia",
            #              "letturaenergiavecchia", "TipoIntervento", "Versione"]
            # # print("Non sono stati riscontrati errori nel caricamento dei dati, procedo con il salvataggio dei file nella tabella dedicata\n")
            #
            # try:
            #     mycursor = mydb.cursor()
            #     CaricaFilesQuery = "INSERT INTO files_backup (Data_Salvataggio, DatiCondominio, Appartamenti, Acqua, Antenne, Elementi, Energia, lettura, letturaacqua, letturaacquavecchia, LetturaCGenerali, letturaenergia, letturaenergiavecchia, TipoIntervento, Versione) VALUES (NOW()"
            #     a = 0
            #     queryPart1 = "INSERT INTO files_backup (Data_Salvataggio, "
            #     queryPart2 = "IdCONfk) VALUES (NOW(), "
            #     queryPart3 = str(IDcon) + ");"
            #
            #     for nomeFile in nomiFiles:
            #         if os.path.exists(pathTemp + "/" + nomeFile + ".xml"):
            #             queryPart1 += nomeFile + ","
            #             queryPart2 += "LOAD_FILE(\"" + pathTemp + "/" + nomeFile + ".xml\"),"
            #             print("file " + nomeFile + ".xml caricato nel db\n")
            #
            #     CaricaFilesQuery = queryPart1 + queryPart2 + queryPart3
            #     print("\n\n\n\n\n\n" + CaricaFilesQuery + "\n\n\n\n\n\n\n")
            #     mycursor.execute(CaricaFilesQuery)
            #     mydb.commit()
            #     mycursor.close()
            #
            #     print("inserimento dei dati nel db avvenuto con successo\n")
            # except:
            #     print("errore nel caricamento dei file di backup nella tabella files_backup\n")
            #
            # mydb.close()

            if cancellaTemp(codice):
                print("cancellazione dei file temporanei avvenuta con successo\n")
                # os.remove("/spool/MARIA/lock")
                return True, "Inserimento nel db avvenuto con SUCCESSO, cancellazione dei file temporanei avvenuta con successo"
            else:
                print("errore o eccezione durante la cancellazione dei file temporanei\n")
                return False, "Inserimento nel db avvenuto con SUCCESSO, ERRORE o Eccezione trovata durante la cancellazione dei file temporanei"

    def ins_data_db_lettura_acqua_modem(self, codice):
        # pid = os.fork()
        # if pid > 0:
        # while  os.path.isfile("/spool/MARIA/lock"):
        # time.sleep(2)
        # f=open("/spool/MARIA/lock", "w+")
        # f.close()
        print("DOPO")
        pathTemp = "/spool/MARIA/" + str(codice) + "/"
        if True:  # codice == DatiAccesso.codiceSessione and dati.controlloAccesso() == True :
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="raf_db",
                allow_local_infile=True
            )

            # la parte di codice da eseguire si considera in base alla presenza o meno del condominio inserito all'interno del database
            # per controllare il modo migliore è controllare se l'id(univoco) del condominio esiste già nel database

            mycursor = mydb.cursor()
            contenutoVersione = []
            print("prima della richiesta del codice")
            codiceCondominio = CondIDFromCodSess(codice)
            print(codiceCondominio)
            ControlloCondQuery = "SELECT IdCONpk \nFROM condomini\nWHERE IdCONpk = \"" + str(codiceCondominio) + "\";"
            mycursor.execute(ControlloCondQuery)

            myresult = mycursor.fetchone()
            mycursor.close()
            IDcon = DatiAccesso.codiceCondominio

            if myresult != None:
                # nel database è stato già registrato questo condominio, quindi lo elimino e poi passo all'inserimento
                # print("Condominio presente nel database con id=" + DatiAccesso.codiceCondominio + ",procedere con la cancellazione e poi l'inserimento")
                mycursor = mydb.cursor()
                CondQuery = "DELETE FROM lettura_acqua_modem WHERE IdCONfk = " + str(IDcon) + ";"
                # print(CondQuery)
                mycursor.execute(CondQuery)
                mydb.commit()
                mycursor.close()

            # importo i dati di letturaacqua nella tabella d'appoggio
            XMLConPath = pathTemp + "/" + "letturaacqua.xml"
            if os.path.exists(XMLConPath):
                print("file letturaacqua.xml trovato\n")
                try:

                    mycursor = mydb.cursor()
                    SvuotaAppQuery = "DELETE FROM appoggio_letture_acqua"
                    print(SvuotaAppQuery)
                    mycursor.execute(SvuotaAppQuery)
                    mydb.commit()
                    mycursor.close()

                    mycursor = mydb.cursor()
                    LetAcquaQuery = "LOAD XML LOCAL INFILE \"" + XMLConPath + "\"\nINTO TABLE appoggio_letture_acqua\nROWS IDENTIFIED BY '<letturaacqua>'\nSET IdCONfk = " + str(
                        IDcon) + ";"
                    print(LetAcquaQuery)
                    mycursor.execute(LetAcquaQuery)
                    mydb.commit()
                    mycursor.close()

                    # print("\n")

                    mycursor = mydb.cursor()
                    EliminaValoriInvalidi = "DELETE FROM appoggio_letture_acqua\nWHERE (F1 IS NULL AND F2 IS NULL AND F3 IS NULL);"
                    print(EliminaValoriInvalidi)
                    mycursor.execute(EliminaValoriInvalidi)
                    mydb.commit()
                    mycursor.close()

                    # print("\n")

                    # collego le letture energia alla tabella Energia
                    mycursor = mydb.cursor()
                    letQuery1 = "UPDATE acqua, appoggio_letture_acqua \nSET appoggio_letture_acqua.IdACQfk = acqua.IdACQpk\nWHERE acqua.Seriale = appoggio_letture_acqua.F1 AND appoggio_letture_acqua.IdCONfk = " + str(
                        IDcon) + " AND acqua.IdCONfk = " + str(IDcon) + ";"
                    print(letQuery1)
                    mycursor.execute(letQuery1)
                    mydb.commit()
                    mycursor.close()


                    # fix letture_acqua
                    mycursor = mydb.cursor()
                    LetEnergiaQuery = "UPDATE appoggio_letture_acqua SET F3 ='' WHERE F3 is Null "
                    print(LetEnergiaQuery)
                    mycursor.execute(LetEnergiaQuery)
                    mydb.commit()
                    mycursor.close()



                    # fix letture_acqua
                    mycursor = mydb.cursor()
                    LetEnergiaQuery = "UPDATE appoggio_letture_acqua SET F2 ='' WHERE F2 is Null "
                    print(LetEnergiaQuery)
                    mycursor.execute(LetEnergiaQuery)
                    mydb.commit()
                    mycursor.close()

                    # importo i dati nella vera tabella letture_energia
                    mycursor = mydb.cursor()
                    letQuery1 = "INSERT INTO lettura_acqua_modem (SELECT DISTINCT * FROM appoggio_letture_acqua);"
                    print(letQuery1)
                    mycursor.execute(letQuery1)
                    mydb.commit()
                    mycursor.close()

                    # svuoto la tabella di appoggio
                    mycursor = mydb.cursor()
                    SvuotaAppQuery = "DELETE FROM appoggio_letture_acqua"
                    print(SvuotaAppQuery)
                    mycursor.execute(SvuotaAppQuery)
                    mydb.commit()
                    mycursor.close()
                    print("file letturaacqua.xml caricato nel db\n")
                except:
                    print("file letturaacqua.xml non caricato nel db, errore o eccezione\n")
                    pass
            else:
                print("file letturaacqua.xml non trovato\n")

            # print("\n")

            # nomiFiles = ["DatiCondominio", "Appartamenti", "Acqua", "Antenne", "Elementi", "Energia", "lettura",
            #              "letturaacqua", "letturaacquavecchia", "LetturaCGenerali", "letturaenergia",
            #              "letturaenergiavecchia", "TipoIntervento", "Versione"]
            # # print("Non sono stati riscontrati errori nel caricamento dei dati, procedo con il salvataggio dei file nella tabella dedicata\n")
            #
            # try:
            #     mycursor = mydb.cursor()
            #     CaricaFilesQuery = "INSERT INTO files_backup (Data_Salvataggio, DatiCondominio, Appartamenti, Acqua, Antenne, Elementi, Energia, lettura, letturaacqua, letturaacquavecchia, LetturaCGenerali, letturaenergia, letturaenergiavecchia, TipoIntervento, Versione) VALUES (NOW()"
            #     a = 0
            #     queryPart1 = "INSERT INTO files_backup (Data_Salvataggio, "
            #     queryPart2 = "IdCONfk) VALUES (NOW(), "
            #     queryPart3 = str(IDcon) + ");"
            #
            #     for nomeFile in nomiFiles:
            #         if os.path.exists(pathTemp + "/" + nomeFile + ".xml"):
            #             queryPart1 += nomeFile + ","
            #             queryPart2 += "LOAD_FILE(\"" + pathTemp + "/" + nomeFile + ".xml\"),"
            #             print("file " + nomeFile + ".xml caricato nel db\n")
            #
            #     CaricaFilesQuery = queryPart1 + queryPart2 + queryPart3
            #     print("\n\n\n\n\n\n" + CaricaFilesQuery + "\n\n\n\n\n\n\n")
            #     mycursor.execute(CaricaFilesQuery)
            #     mydb.commit()
            #     mycursor.close()
            #
            #     print("inserimento dei dati nel db avvenuto con successo\n")
            # except:
            #     print("errore nel caricamento dei file di backup nella tabella files_backup\n")
            #
            # mydb.close()

            if cancellaTemp(codice):
                print("cancellazione dei file temporanei avvenuta con successo\n")
                # os.remove("/spool/MARIA/lock")
                return True, "Inserimento nel db avvenuto con SUCCESSO, cancellazione dei file temporanei avvenuta con successo"
            else:
                print("errore o eccezione durante la cancellazione dei file temporanei\n")
                return False, "Inserimento nel db avvenuto con SUCCESSO, ERRORE o Eccezione trovata durante la cancellazione dei file temporanei"
    def ins_data_db_lettura_energia_modem(self, codice):
        print("DOPO")
        pathTemp = "/spool/MARIA/" + str(codice) + "/"
        if True:  # codice == DatiAccesso.codiceSessione and dati.controlloAccesso() == True :
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="raf_db",
                allow_local_infile=True
            )

            # la parte di codice da eseguire si considera in base alla presenza o meno del condominio inserito all'interno del database
            # per controllare il modo migliore è controllare se l'id(univoco) del condominio esiste già nel database

            mycursor = mydb.cursor()
            contenutoVersione = []
            print("prima della richiesta del codice")
            codiceCondominio = CondIDFromCodSess(codice)
            print(codiceCondominio)
            ControlloCondQuery = "SELECT IdCONpk \nFROM condomini\nWHERE IdCONpk = \"" + str(codiceCondominio) + "\";"
            mycursor.execute(ControlloCondQuery)

            myresult = mycursor.fetchone()
            mycursor.close()
            IDcon = DatiAccesso.codiceCondominio

            if myresult != None:
                # nel database è stato già registrato questo condominio, quindi lo elimino e poi passo all'inserimento
                # print("Condominio presente nel database con id=" + DatiAccesso.codiceCondominio + ",procedere con la cancellazione e poi l'inserimento")
                mycursor = mydb.cursor()
                CondQuery = "DELETE FROM lettura_energia_modem WHERE IdCONfk = " + str(IDcon) + ";"
                # print(CondQuery)
                mycursor.execute(CondQuery)
                mydb.commit()
                mycursor.close()

            # importo i dati di letturaacqua nella tabella d'appoggio
            XMLConPath = pathTemp + "/" + "letturaenergia.xml"
            if os.path.exists(XMLConPath):
                print("file letturaenergia.xml trovato\n")
                try:

                    mycursor = mydb.cursor()
                    SvuotaAppQuery = "DELETE FROM appoggio_letture_energia"
                    print(SvuotaAppQuery)
                    mycursor.execute(SvuotaAppQuery)
                    mydb.commit()
                    mycursor.close()


                    mycursor = mydb.cursor()
                    LetAcquaQuery = "LOAD XML LOCAL INFILE \"" + XMLConPath + "\"\nINTO TABLE appoggio_letture_energia\nROWS IDENTIFIED BY '<letturaenergia>'\nSET IdCONfk = " + str(
                        IDcon) + ";"
                    print(LetAcquaQuery)
                    mycursor.execute(LetAcquaQuery)
                    mydb.commit()
                    mycursor.close()

                    # print("\n")

                    mycursor = mydb.cursor()
                    EliminaValoriInvalidi = "DELETE FROM appoggio_letture_energia\nWHERE (F1 IS NULL AND F2 IS NULL AND F3 IS NULL);"
                    print(EliminaValoriInvalidi)
                    mycursor.execute(EliminaValoriInvalidi)
                    mydb.commit()
                    mycursor.close()

                    # print("\n")



                    # collego le letture energia alla tabella Energia
                    mycursor = mydb.cursor()
                    letQuery1 = "UPDATE energia, appoggio_letture_energia \nSET appoggio_letture_energia.IdENEfk = energia.IdENEpk\nWHERE energia.SerialeE = appoggio_letture_energia.F1 AND appoggio_letture_energia.IdCONfk = " + str(
                        IDcon) + " AND energia.IdCONfk = " + str(IDcon) + ";"
                    print(letQuery1)
                    mycursor.execute(letQuery1)
                    mydb.commit()
                    mycursor.close()

                    # fix letture_acqua
                    mycursor = mydb.cursor()
                    LetEnergiaQuery = "UPDATE appoggio_letture_energia SET F3 ='' WHERE F3 is Null "
                    print(LetEnergiaQuery)
                    mycursor.execute(LetEnergiaQuery)
                    mydb.commit()
                    mycursor.close()


                    # fix letture_acqua
                    mycursor = mydb.cursor()
                    LetEnergiaQuery = "UPDATE appoggio_letture_energia SET F2 ='' WHERE F2 is Null "
                    print(LetEnergiaQuery)
                    mycursor.execute(LetEnergiaQuery)
                    mydb.commit()
                    mycursor.close()

                    # importo i dati nella vera tabella letture_energia
                    mycursor = mydb.cursor()
                    letQuery1 = "INSERT INTO lettura_energia_modem (SELECT DISTINCT * FROM appoggio_letture_energia);"
                    print(letQuery1)
                    mycursor.execute(letQuery1)
                    mydb.commit()
                    mycursor.close()

                    # svuoto la tabella di appoggio
                    mycursor = mydb.cursor()
                    SvuotaAppQuery = "DELETE FROM appoggio_letture_energia"
                    print(SvuotaAppQuery)
                    mycursor.execute(SvuotaAppQuery)
                    mydb.commit()
                    mycursor.close()
                    print("file letturaenergia.xml caricato nel db\n")
                except:
                    print("file letturaenergia.xml non caricato nel db, errore o eccezione\n")
                    pass
            else:
                print("file letturaenergia.xml non trovato\n")

            # print("\n")

            # nomiFiles = ["DatiCondominio", "Appartamenti", "Acqua", "Antenne", "Elementi", "Energia", "lettura",
            #              "letturaacqua", "letturaacquavecchia", "LetturaCGenerali", "letturaenergia",
            #              "letturaenergiavecchia", "TipoIntervento", "Versione"]
            # # print("Non sono stati riscontrati errori nel caricamento dei dati, procedo con il salvataggio dei file nella tabella dedicata\n")
            #
            # try:
            #     mycursor = mydb.cursor()
            #     CaricaFilesQuery = "INSERT INTO files_backup (Data_Salvataggio, DatiCondominio, Appartamenti, Acqua, Antenne, Elementi, Energia, lettura, letturaacqua, letturaacquavecchia, LetturaCGenerali, letturaenergia, letturaenergiavecchia, TipoIntervento, Versione) VALUES (NOW()"
            #     a = 0
            #     queryPart1 = "INSERT INTO files_backup (Data_Salvataggio, "
            #     queryPart2 = "IdCONfk) VALUES (NOW(), "
            #     queryPart3 = str(IDcon) + ");"
            #
            #     for nomeFile in nomiFiles:
            #         if os.path.exists(pathTemp + "/" + nomeFile + ".xml"):
            #             queryPart1 += nomeFile + ","
            #             queryPart2 += "LOAD_FILE(\"" + pathTemp + "/" + nomeFile + ".xml\"),"
            #             print("file " + nomeFile + ".xml caricato nel db\n")
            #
            #     CaricaFilesQuery = queryPart1 + queryPart2 + queryPart3
            #     print("\n\n\n\n\n\n" + CaricaFilesQuery + "\n\n\n\n\n\n\n")
            #     mycursor.execute(CaricaFilesQuery)
            #     mydb.commit()
            #     mycursor.close()
            #
            #     print("inserimento dei dati nel db avvenuto con successo\n")
            # except:
            #     print("errore nel caricamento dei file di backup nella tabella files_backup\n")
            #
            # mydb.close()

            if cancellaTemp(codice):
                print("cancellazione dei file temporanei avvenuta con successo\n")
                # os.remove("/spool/MARIA/lock")
                return True, "Inserimento nel db avvenuto con SUCCESSO, cancellazione dei file temporanei avvenuta con successo"
            else:
                print("errore o eccezione durante la cancellazione dei file temporanei\n")
                return False, "Inserimento nel db avvenuto con SUCCESSO, ERRORE o Eccezione trovata durante la cancellazione dei file temporanei"
    #funzione che restituisce il messaggio di stato corrente delle operazioni eseguite con successo
    def statoCorrente(self, codice) :
        if codice == DatiAccesso.codiceSessione :
            return DatiAccesso.messaggioStato
        else :
            return "codice sessione non valido"

    #funzione di chiusura di sessione, se non viene utilizzata l'id sessione e l'idcondominio rimarranno invariati e istanziati fino a terminazione del processo server
    def quit(self,codice) :
        print("Deleting session " + str(codice))
        pathTemp="/spool/MARIA/" +str(codice)+ "/"
        try :
            DatiAccesso.codiceSessione = -1
            DatiAccesso.codiceCondominio = -1
            DatiAccesso.messaggioStato = ""
            DatiAccesso.indiciFiles.clear()
            os.rmdir(pathTemp)
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="raf_db",
                allow_local_infile = True
                )

            mycursor = mydb.cursor()
            mycursor.execute("DELETE FROM Sessions WHERE  Sessione="+ str(codice))
            mydb.commit()
            mydb.close()

        except:
            return False
        return True

    #funzione che recupera le righe dei files di un certo condominio, e la data di inseriemnto degli stessi
    #il messaggio restituito va stampato da client, questo poi passerà uno degli indici proposti nella lista
    #alla funzione scaricaFiles e potrà scaricare i files di una determinata data


    #da usare in coppia subito dopo a listaFiles, permette di scaricare i files proposti con listaFiles()
    #basta dare per parametro uno degli indici della lista restituita da listaFiles()


    #questa funzione permette l'inserimento di un bool, nel caso di true vengono generati gli storici degli appartamenti nel condominio che si sta inserendo, nel caso di false non viene generato alcun storico
    #tutti gli storici vengono poi posti nella tabella storici, che viene poi collegata in front end per renderla disponibile a chi deve usufruirne
    #QUESTA FUNZIONE VA USATA DOPO IL CARICAMENTO DEL CONDOMINIO INS_DATA E PRIMA DEL QUIT






#########################################################################################################################
#########################################################################################################################
#########################################################################################################################
#########################################################################################################################
#########################################################################################################################
#########################################################################################################################












class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
        pass


#in questo punto viene avviato il server e rimane in ascolto fino a interruzione volontaria
#server = SimpleXMLRPCServer(("192.168.88.84", 3060))
server =  SimpleThreadedXMLRPCServer(("192.168.88.150", 2908))#SimpleXMLRPCServer(("192.168.88.150", 3808))
#server = SimpleXMLRPCServer(("192.168.178.20", 3060))
print("Listening on port 2808...")
#print("Listening on port 3060...")
server.register_instance(MyFuncs())

try:
    print("Use Control-C per uscire")
    server.serve_forever()
except KeyboardInterrupt:
    print("Sto uscendo...")
