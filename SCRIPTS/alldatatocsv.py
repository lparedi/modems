import meterbus
import mysql.connector
csv = "Rip;Stato;ValoreAttuale;Unita;SetDay;ValoreAlSetDay;UltimaRicezione;DataLettura\n"
condID = 101050
today= "202201"
mydb = mysql.connector.connect(
    host="192.168.88.150",
    user="root",
    password="1!Cscsql",
    database="raf_db",
    allow_local_infile=True
)
mycursor = mydb.cursor()
mycursor.execute("SELECT Telegram , ReadDate, SecAddr From Telegrams WHERE idCONfk = " + str(condID) +" ORDER BY SecAddr DESC " )
#+ " AND ReadDate ='" + str(today) + "'")
result = mycursor.fetchall()
mydb.close()
for res in result:
    #print(res[1])
    strtl = bytes.fromhex(res[0])
    try:
        tg = meterbus.TelegramLong(strtl)
    except:
        print("Error")
        pass
    ID = str(tg.body.interpreted['header']['identification'])
    ID = ID.replace(",", "")
    ID = ID.replace("0x", "")
    ID = ID.replace(" ", "")
    csv = csv + ID + ";"
    Status = str(int(tg.body.interpreted["header"]["status"], 16))
    csv = csv + Status + ";"
    CurrentValue = str(tg.body.interpreted["records"][3]["value"])
    try:
        a=float(CurrentValue)
        a=round(a,3)
    except:
        continue
    CurrentValue=str(a)
    csv = csv + CurrentValue +";"
    Units = str(tg.body.interpreted["records"][0]["unit"])
    csv = csv + Units + ";"
    SetDay = str(tg.body.interpreted["records"][0]["value"])
    csv = csv + SetDay + ";"
    ValueAtSetday = str(tg.body.interpreted["records"][4]["value"])
    csv = csv + ValueAtSetday + ";"
    LastRecived = str(tg.body.interpreted["records"][6]["value"])
    csv = csv + LastRecived +";"
    Date = res[1]
    csv = csv + Date + "\n"
print(csv)





