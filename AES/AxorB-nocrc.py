import binascii
from Crypto.Cipher import AES
from pprint import pprint
def initialvector(telegram):
    vct = telegram[4:8] +  telegram[8:16]+  telegram[16:20] +  8*telegram[22:24]
    return vct
    pass

def getencriptedblocks(telegram):
    result = []
    pos = telegram.find("6085") +4
    
    result.append(telegram[pos:pos+32])
    offset = 2
    #print(str(len(telegram)) + str(pos + offset*36))
    while len(telegram) >(pos + offset*32) :
        result.append(telegram[pos  + (offset-1)*32 : pos   + offset*32])
        offset = offset+1

    return result


fin = open("Telegrams.txt","r")
telegrams = fin.read()
#print(telegrams)
for TELEGRAM in telegrams.split("\n"):
    #print(TELEGRAM)
    if len (TELEGRAM) < 10:
        continue
    AESBLK = getencriptedblocks(TELEGRAM)
    #print("Blocchi cifrati:")
    #pprint(AESBLK)
    INITVECT = initialvector(TELEGRAM)
    #print("Vettore di inizializzazione: " + INITVECT)

    AES1=binascii.unhexlify("BC3273D12CCAA1039CF9ADEA242AAAA4")
    AESK=binascii.unhexlify("00000000000000000000000000000000")
    if False:
        rijn = AES.new(AESK, AES.MODE_ECB)
        decripted = rijn.decrypt(AES1)
        #print(binascii.hexlify(decripted).decode('utf-8'))
        A1 = binascii.hexlify(decripted).decode('utf-8')
        #print("Primo Blocco Decriptato: " + A1)
        #B1="01069205000005073737373737373737"
        B1 = INITVECT
        C1= hex(int(A1, 16) ^ int(B1, 16))
        print( "Blocco Decriptato: " + C1.replace("0x","").upper())


        AES2=binascii.unhexlify("8B52E0062B5DF4B26D16C28187ABC90A")
        decripted = rijn.decrypt(AES2)
        A2= binascii.hexlify(decripted).decode('utf-8')
        B2= "BC3273D12CCAA1039CF9ADEA242AAAA4"
        C2= hex(int(A2, 16) ^ int(B2, 16))
        print( "Blocco Decriptato: " + C2.replace("0x","").upper())

        AES3 = binascii.unhexlify("81039A14A6FD13BEE73B73B81EDB104D")
        rijn = AES.new(AESK, AES.MODE_ECB)
        decripted = rijn.decrypt(AES3)
        A3= binascii.hexlify(decripted).decode('utf-8')
        B3= "8B52E0062B5DF4B26D16C28187ABC90A"
        C3= hex(int(A3, 16) ^ int(B3, 16))
        print( "Blocco Decriptato: " + C3.replace("0x","").upper())

        AES4 = binascii.unhexlify("235E787F7AA61B0DD7485B5A3EF24F06")
        rijn = AES.new(AESK, AES.MODE_ECB)
        decripted = rijn.decrypt(AES4)
        A4= binascii.hexlify(decripted).decode('utf-8')
        B4= "81039A14A6FD13BEE73B73B81EDB104D"
        C4= hex(int(A4, 16) ^ int(B4, 16))
        print( "Blocco Decriptato: " + C4.replace("0x","").upper())

    print("********************************************")
    firsttime = True
    blkpos = 0
    print("SecAddr:" + TELEGRAM[8:16])
    for BLK in AESBLK:
        
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
        print( "Blocco Decriptato: " + C.replace("0x","").upper())
        
        pass



