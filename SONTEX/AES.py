import binascii
import sys
from Crypto.Cipher import AES
from pprint import pprint
sys.path.insert(1,"../")
import commonfunctions
def initialvector(telegram):
    vct =  telegram[22:26]  + telegram[14:22] + telegram[26:30] + telegram[30:32] * 8
    return vct
    pass

def getencriptedblocks(telegram):
    result = []
    pos = telegram.find("A0C5") + 4 
    
    result.append(telegram[pos:pos+32])
    offset = 2
    #print(str(len(telegram)) + str(pos + offset*36))
    while len(telegram) >(pos + offset*32) :
        result.append(telegram[pos  + (offset-1)*32 : pos   + offset*32])
        offset = offset+1

    return result






#pprint(INITVECT)
#INITVECT = "ee4d6612422016081919191919191919".upper()
#pprint(INITVECT)
#exit(0)



def decrypt566(telegram,key):
    debug = 0
    AESK=binascii.unhexlify(key)
    AESBLK = getencriptedblocks(telegram)
    INITVECT = initialvector(telegram)
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
    

def getreadings(bloks):
    debug = 0
    setdayhex = bloks[0][22:24] +  bloks[0][20:22] 
    currenthex = bloks[1][8:10] + bloks[1][6:8]
    if debug == 1:
        print(int(setdayhex,16))
        print(int(currenthex,16))
    return int(setdayhex,16),int(currenthex,16)
    pass

bloks = []
key = "52494343494152444920333156696120"
TELEGRAM = "68BABA6808FE7267124220EE4D16081900A0C5343D3ABCFCBD60035AE01A428FCC29214D67D083CF2E07505F3A7B5C38BA056EAB8166CDF8DC364BDFFAED0F44218320A67CC9D1B9AF8B058B7D8B0ED2B07D70FAE5C84248A610C87CDB1B34F9EBB3A61ABC127EA615FDCFC19245987D046300ECE7DB9AF1D2BF8DD3FFD46C8AF2077F9ED1F2D95347B491204A8269E1D586EFEC01EFE9FF518FAF9B6BBC21B529ADA7F160FA4F6E8833CDDA8E0E266B577DBF01FF2B000C78671242200F2F16"
meter = commonfunctions.extractmeterfromtelegram(TELEGRAM)
bloks =  decrypt566(TELEGRAM,key)
current,setday = getreadings(bloks)
print(current)
print(setday)
print(meter)
pprint(bloks)

bloks = []
key = "4C454F504152444920313039202D204D"
TELEGRAM = "68BABA6808FE7292727918EE4D16083D00A0C59130DE3ACBB676B98A82B0B07CA42EDE105E58CE9BC7A8E061650B701A37F552FBF542BB9A0F68B143D5BD2CA7F1CEA26B9843292FF716B5F8FE42A3728E324D53EACAF474BDFAC58F7ABE380FE49C0DBFF47DDDC434C0B868C5203CA0A05868D00B540726C17584A4C82E40238BC1B2B072341E2DCB47A2741632E4DE6831CD7B1B68E6AEF8040D058190E4102912CC6D67061F981057C3A630C40EC50EDDFF01FF2B000C78927279180FD916"
decrypt566(TELEGRAM,key)
meter = commonfunctions.extractmeterfromtelegram(TELEGRAM)
bloks =  decrypt566(TELEGRAM,key)
current,setday = getreadings(bloks)
print(current)
print(setday)
print(meter)
pprint(bloks)