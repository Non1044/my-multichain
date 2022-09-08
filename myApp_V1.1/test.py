from myutil import *
import bitcoin

def gen_pwd_test():
    for _ in range(10):
        pwd = gen_pwd()
        print(gen_pwd(), is_valid_pwd(pwd), bitcoin.sha256(pwd))
##gen_pwd_test()

def hex_test():
    en = str_hex('john')
    print(en)
    print(hex_str(en))
##hex_test()

def encode_test():
    admin_addr = '1ZAHSRHpJFtXQLLeWw1Z2D1XEQyFuMaRHxXrFN'
    pwd = 'hi234'
    ena = encode(admin_addr, pwd)
    sh_ena = str_hex(ena)
    print(sh_ena)
    hs_ena = hex_str(sh_ena)
    print(decode(hs_ena, pwd))
##encode_test()

#------------------------------------------------------
    
def list_streams():
    for s in api.liststreams():
        print(s['name'])
##list_streams()

def list_items():
   for j in api.liststreamitems('energy'):
       print(j['keys'][0], j['data'])
list_items()

##print(is_valid_admin_pwd('hi234'))
##print(is_eligible('john'))
##print(is_registered('jack'))
##print(is_valid_user_pwd('jack', 'eGKD'))

def list_transfer():
   for j in api.liststreamkeyitems('energy', 'transfer'):
       print(j['data'])
##list_transfer()
