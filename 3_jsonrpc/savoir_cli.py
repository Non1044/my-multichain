from myutil import *

addr = '1MDLPJrwyEbDg6xk8JiuTr33ZCPtT2BNTtoMx1'
def savoir_test():
    res = api.getinfo()
##    res = api.listaddresses()
##    res = api.validateaddress(addr)
    pp.pprint(res)
##savoir_test()

def getinfo():
    r = api.getinfo()
    for (k,v) in r.items():
        print(k ,': ', v)
    
    print(type(r))
    print(r.get('nodeaddress'))
    print(r['blocks'])
##getinfo()

def list_addresses():
    r = api.listaddresses()
    print(r)                    ## array of jsons(which is a dict).
    print(r[0]['address'])
##list_addresses()

def validate_address(addr):
    r = api.validateaddress(addr)
    print(r['isvalid'])
##validate_address(addr)
    


