import binascii
def ascii_to_hex(ascii_str):
    hex_str = binascii.hexlify(ascii_str.encode())
    return hex_str


CondID = "13667"
prefix = "###AT+WRSN="
buff = ""
counter = 0
fcount = 0
fin = open(CondID + "/LIST/list", "r")
for rip in fin:
    print(rip.rstrip())
    counter = counter + 1
    buff = buff + "-" + rip.rstrip()
    if counter % 10 == 0:
        fout = open((CondID + "/LIST/" + str(fcount) + ".hex"), "w")
        hexstring = ascii_to_hex(prefix + "10" + buff + ";")
        fout.write(hexstring.decode(("utf-8")))
        fout.close()
        buff = ""
        counter = 0
        fcount = fcount + 1

if len(buff) != 0:
    fout = open((CondID + "/LIST/" + str(fcount) + ".hex"), "w")
    hexstring = ascii_to_hex(prefix + str(counter) + buff + ";")
    fout.write(hexstring.decode("utf-8"))
    fout.close()




