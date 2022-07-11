import xmlrpc.client  

with xmlrpc.client.ServerProxy("http://172.24.101.98:2808/") as proxy:
    result = proxy.getreading(13667,"202112","MeasureUnit.HCA")
    csv = "Valore;Stato:DataLettura;Indirizzo\n"
    for a in result:
        csv =  csv + str(a[0]) + ";" + str(a[1]) + ";" + str(a[2]) + ";" + str(a[3]) + "\n" 

    print(csv)
