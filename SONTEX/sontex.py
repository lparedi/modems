import meterbus
from meterbus import  wtelegram_body
import pprint
import base64
import sys
a="aLq6aAj+cmcSQiDuTRYIGQCgxTQ9Orz8vWADWuAaQo/MKSFNZ9CDzy4HUF86e1w4ugVuq4FmzfjcNkvf+u0PRCGDIKZ8ydG5r4sFi32LDtKwfXD65chCSKYQyHzbGzT567OmGrwSfqYV/c/BkkWYfQRjAOzn25rx0r+N0//UbIryB3+e0fLZU0e0kSBKgmnh1Ybv7AHv6f9Rj6+ba7whtSmtp/Fg+k9uiDPN2o4OJmtXfb8B/ysADHhnEkIgDy8W"
b = base64.b64decode(a).hex()
print(b)
c=bytes.fromhex(b)
print(c)
data = list(c)
tg = meterbus.load(c)
pprint.pprint(tg.interpreted)