import meterbus
import mysql.connector
csv = "Rip;Stato;ValoreAttuale;Unita;SetDay;ValoreAlSetDay;UltimaRicezione;DataLettura\n"
condID = 14894
today = "202201"
fieldallowd = ["MeasureUnit.HCA" , "MeasureUnit.DATE"]
mydb = mysql.connector.connect(
    host="192.168.88.150",
    user="root",
    password="1!Cscsql",
    database="raf_db",
    allow_local_infile=True
)
mycursor = mydb.cursor()
mycursor.execute("SELECT Telegram , ReadDate, SecAddr From Telegrams WHERE idCONfk = " + str(condID) + " AND Units = 'MeasureUnit.HCA'   ORDER BY SecAddr DESC ")
# + " AND ReadDate ='" + str(today) + "'")
result = mycursor.fetchall()
mydb.close()
for res in result:
    csv = ""
    # print(res[1])
    strtl = bytes.fromhex(res[0])
    try:
        tg = meterbus.TelegramLong(strtl)
    except:
        print("Error")
        continue
    dataread = '.'.join(res[1][i:i+4] for i in range(0, len(res[1]), 4))

    csv = csv + str(dataread) + ";"
    a = tg.body.interpreted['header']
    identification = a["identification"]
    identification = identification.replace("0x" , "")
    identification = identification.replace(",","")
    identification =  identification.replace(" ","")

    status = a["status"]
    status = status.replace("0x" , "")
    status = status.replace(",","")
    status =  status.replace(" ","")

    csv = csv + identification + ";" + status  +";"
    
 
    b = tg.body.interpreted["records"]
    for k in b:
       
        for r in k:
            if k["unit"] in fieldallowd:
                csv = csv + r + ";"
                csv = csv + str(k[r]) +";"
    print( csv )
