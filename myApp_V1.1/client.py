import requests as rq
a = [{'date': '01/01/2022', 'src': 'john', 'target': 'jack', 'amount': 100},
     {'date': '01/01/2022', 'src': 'john', 'target': 'joe', 'amount': 200},
     {'date': '02/01/2022', 'src': 'john', 'target': 'jack', 'amount': 300},
     {'date': '03/01/2022', 'src': 'joe', 'target': 'jack', 'amount': 400},
     {'date': '04/01/2022', 'src': 'john', 'target': 'joe', 'amount': 500},
]
def transfer():
    for j in a:
        rq.post('http://127.0.0.1:8080/sendtransfertx', data=j)
##transfer()

import json
def transfer_by_date(d):
    res = rq.post('http://127.0.0.1:8080/gettransferbydate', \
                    data={'date': d}).text
    for j in json.loads(res):
        print(j)
##transfer_by_date('01/01/2022')

def transfer_by_src(s):
    res = rq.post('http://127.0.0.1:8080/gettransferbysrc', \
                    data={'src': s}).text
    for j in json.loads(res):
        print(j)
##transfer_by_src('john')
        
