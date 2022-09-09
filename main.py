import pyodbc
import pandas as pd




db = pyodbc.connect(
    'DRIVER={SQL Server};SERVER=uygunitem.com.\MSSQLSERVER2012;DATABASE=uygunite_uygunitem;UID=uygunite_admin;PWD=psw'
)
cursor = db.cursor()

cursor.execute("SELECT cekilen_isim FROM [cekilen_datalar]")
isimler = cursor.fetchall()
cursor.execute("SELECT cekilen_data_id FROM [cekilen_datalar]")
idler = cursor.fetchall()
cursor.execute("SELECT urun_isim FROM [urunler]")
topicIsimler = cursor.fetchall()
cursor.execute("SELECT urun_id FROM [urunler]")
topicIdler = cursor.fetchall()


topicIsimlerList = []
topicIdlerList =[]

for a in topicIsimler:
    i = str(a)
    i = i.replace('\'', '')
    i = i.replace('(', '')
    i = i.replace(')', '')
    i = i.replace('[', '')
    i = i.replace('+', ' ')
    i = i.replace(']', '')
    i = i.replace('.', '')
    i = i.replace(',', '')
    i = i.replace('?', '')
    i = i.replace('/', '')
    i = i.replace('!', '')
    topicIsimlerList.append(i)
for b in topicIdler:
    b = str(b)
    b = b.replace(' ','')
    b = b.replace(',','')
    b = b.replace('(','')
    b = b.replace(')','')
    topicIdlerList.append(int(b))

zipTopicler = zip(topicIsimlerList,topicIdlerList)
zipTopicler = tuple(zipTopicler)


isimlerList = []
idlerList = []

for a in isimler:
    i = str(a)
    i = i.replace('\'', '')
    i = i.replace('(', '')
    i = i.replace(')', '')
    i = i.replace('+', ' ')
    i = i.replace('[', '')
    i = i.replace(']', '')
    i = i.replace('.', '')
    i = i.replace(',', '')
    i = i.replace('?', '')
    i = i.replace('/', '')
    i = i.replace('!', '')
    isimlerList.append(i)
for b in idler:
    b = str(b)
    b = b.replace(' ','')
    b = b.replace(',','')
    b = b.replace('(','')
    b = b.replace(')','')
    idlerList.append(int(b))

zipUrunler = zip(isimlerList,idlerList)
zipUrunler = tuple(zipUrunler)

for i in zipUrunler:
    maxTopic = ""
    maxTopicId = ""
    maxScore=0
    score = 0
    ayrilmisIsim = i[0].split(" ")
    for y in zipTopicler:
        score = 0
        for z in ayrilmisIsim:
            testList = y[0].split(" ")

            for x in testList:
                if x == '':
                    testList.remove(x)
            for d in testList:
                if z == d:
                    if z.isdigit():
                        score += 5
                    elif z == "":
                        score = score
                    elif z in "+":
                        z = z.replace('+',' ')
                        ayrilanIki = z.split(' ')
                        for h in ayrilanIki:
                            if h.isdigit():
                                score +=5
                            else:
                                score +=1
                    else:
                        score += 1
        # print(score)
        # print(y[0])
        # print("")
        if score > maxScore:
            maxScore =score
            maxTopic = y[0]
            maxTopicId = y[1]

    print("Ürün: ",i[0])
    print("Ait Olduğu Topic: ",maxTopic)
    print("Max Score: ",maxScore)
    print("")
    cursor.execute("UPDATE cekilen_datalar SET cekilen_urun_id= ? WHERE cekilen_data_id= ? ",maxTopicId,i[1])
    db.commit()


