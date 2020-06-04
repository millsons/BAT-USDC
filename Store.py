global Log
Log = ""
def StoreInfo(data):
    file1 = open(Log+".txt", 'a')
    file1.write(str(data) + "\n")
    file1.close()
    print(data)