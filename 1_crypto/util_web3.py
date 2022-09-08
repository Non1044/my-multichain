# These are offline utility.

from web3 import Web3
url = 'http://127.0.0.1:8545'
w3 = Web3(Web3.HTTPProvider(url))

def to_hex():
    print(w3.toHex(False), w3.toHex(True))  # 0x0 0x1
    print(w3.toHex(0), w3.toHex(1))         # 0x0 0x1
    print(w3.toHex(0x000f))                 # 0xf.

    print(w3.toHex(b'\x00\x0f'))            # 0x000f
    print(w3.toHex(text='abc'))             # 0x616263
    print(w3.toHex(hexstr='616263'))        # 0x616263
# to_hex()

def to_bytes():
    print(w3.toBytes(False), w3.toBytes(True))  # b'\x00' b'\x01'
    print(w3.toBytes(0), w3.toBytes(1))         # b'\x00' b'\x01'
    print(w3.toBytes(0x000f))                   # b'\x0f'
    print(w3.toBytes(b'\x00\x0f'))              # b'\x00\x0f'
    print(w3.toBytes(text='abc'))               # b'abc'
    print(w3.toBytes(hexstr='616263'))          # b'abc'
# to_bytes()

def to_text():  # decoded as UTF-8
    print(w3.toText(b'abc'))                # abc
    print(w3.toText(hexstr='616263'))       # abc
# to_text()

def to_Int():
    print(w3.toInt(False), w3.toInt(True))          # 0 1
    print(w3.toInt(0x000F), w3.toInt(b'\x00\x0F'))  # 15 15
    print(w3.toInt(hexstr='000F'))                  # 15
# to_Int()

def to_json():
    print(w3.toJSON(1))                 # 1
    d = {'one': 1}
    print(type(d), w3.toJSON(d))        # <class 'dict'> {"one": 1}
    print(w3.toJSON([{'one': 1}]))      # [{"one": 1}]
# to_json()

from decimal import Decimal
def wei():
    print(w3.toWei(1, 'ether'))         # 1000000000000000000
    print(w3.fromWei(1000000000000000000, 'ether'))   # 1

    print(w3.toWei(Decimal('0.000000005'), 'ether')) # 5000000000
    print(w3.fromWei(5000000000, 'gwei'))            # 5

    print(w3.fromWei(12345678900000000001, 'ether')) # 12.345678900000000001
    print(w3.toWei(Decimal('12.345678900000000001'), 'ether')) # 12345678900000000001
# wei()

# Keccak-256:
def keccak():
    h = w3.keccak(text='Hello')  # bytes array
    print(h)
        # b'\x06\xb3\xdf\xae\xc1H\xfb\x1b\xb2\xb0f\xf1\x0e\xc2\x85\xe7\xc9\xbf@*\xb3*\xa7\x8a]8\xe3Ef\x81\x0c\xd2'
    print(w3.toHex(h))           # str
        # 0x06b3dfaec148fb1bb2b066f10ec285e7c9bf402ab32aa78a5d38e34566810cd2
# keccak()
