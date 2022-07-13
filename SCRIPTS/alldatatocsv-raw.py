import meterbus
import mysql.connector
csv = "Rip;Stato;ValoreAttuale;Unita;SetDay;ValoreAlSetDay;UltimaRicezione;DataLettura\n"
condID = 101050
today = "202201"
mydb = mysql.connector.connect(
    host="192.168.88.150",
    user="",
    password="",
    database="",
    allow_local_infile=True
)
mycursor = mydb.cursor()
mycursor.execute("SELECT Telegram , ReadDate, SecAddr From Telegrams WHERE idCONfk = " + str(condID) + " ORDER BY SecAddr DESC ")
# + " AND ReadDate ='" + str(today) + "'")
result = mycursor.fetchall()
mydb.close()
for res in result:
    print("*********************************************************************************************")
    print("data for meter " + str(res[2]) + " readed: " + str(res[1]))
    print("*********************************************************************************************")
    print("")
    # print(res[1])
    strtl = bytes.fromhex(res[0])
    try:
        tg = meterbus.TelegramLong(strtl)
    except:
        print("Error")
        continue
    a = tg.body.interpreted['header']

    for k in a:
        print(k + " -> " + str(a[k]))
    print("")
    print("Records:")
    b = tg.body.interpreted["records"]
    for k in b:
        print("")
        for r in k:
            print(r + " -> " + str(k[r]))
    print("\n")
