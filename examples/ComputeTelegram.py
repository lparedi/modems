import binascii
from commonfunctions import *


def ascii_to_hex(ascii_str):
    hex_str = binascii.hexlify(ascii_str.encode())
    return hex_str


CondID = "13603"
TeleType = "SELECT_FD"
prefix = "680B0B6873FD52"
buff = ""
counter = 0
fcount = 0
meterslist = getmeterslist(CondID)
for hca in meterslist:
    idreversed = str(hca[0])
    if TeleType == "SELECT_FD":
        meterid = ""
        for i in range(8, 0, -2):
            # print ( i )
            # print (idreversed[i -2 :i])
            idrev = idreversed[i - 2:i]
            meterid = meterid + idrev
        print(idreversed + " -> " + meterid)
        Telegram = prefix + meterid + "FFFFFFFF" + "XX" + "16"
        print(Telegram)
        print(mbcheksum(Telegram))
        print(Telegram.replace("XX", mbcheksum(Telegram).upper()))
