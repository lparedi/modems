import http.client
from commonfunctions import *
def aa(number,telegram):


  conn = http.client.HTTPSConnection("olivettiiot.tim.it")
  payload = "{\n  \"m2m:cin\": {\n\t\"lbl\": [ \"proto:udp\", \"port:5685\" ],\n    \"cnf\": \"text/plain:0\",\n    \"con\": \"" + telegram + "\"\n  }\n}"
  headers = {
    'X-M2M-RI': 'CIN_1631194038',
    'X-M2M-Origin': 'CCEDB769A-ad46824a',
    'Content-Type': 'application/vnd.onem2m-res+json;ty=4',
    'Accept': 'application/vnd.onem2m-res+json',
    'Authorization': 'Q0NFREI3NjlBLWFkNDY4MjRhOjVlNjNjYWI5OTdjZDQ2MjNhYzBkMTU5N2I4MWM3MzRl'
  }
  conn.request("POST", "/onem2m/" + number + "/nbiot/outbox", payload, headers)
  res = conn.getresponse()
  data = res.read()
  print(data.decode("utf-8"))


number = "393688441940"
telegram = "23232341542b5752534e3d31302c312d39333434353839342d39333434353930352d39333434353930362d39333434353930372d39333434353930382d32363834373535332d32363834373535342d32363834373535352d32363834373535362d32363834373535373b"
sendprecomputed(telegram,number)
