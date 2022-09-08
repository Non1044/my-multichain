
## Binary Encoding: (0-1)
# Most programs handle data by bytes or characters.
# But a Unicode character may be one to four bytes.
def bin_encode():
    s1 = 'ABC'
    s2 = 'กขค'
    # By default Python iterates str by character.
    for c in s1:
        print(c, end=',')       # A,B,C,
    print()
    for c in s2:
        print(c, end=',')       # ก,ข,ค,
    print()

    # Python supports binary encoding.
    # encode() converts str to byte array.
    # decode() converts byte array to str.
    # Byte array literals are preceded by 'b'.
    se = s1.encode()
    print(se)           ## b'ABC'
    print(se.decode())  ## ABC

    # encode() is used for iterating by bytes.
    for c in s1.encode():       ## 65,66,67,
        print(c, end=',')
    print()
    for c in s2.encode():
        print(c, end=',')       ## 224,184,129,224,184,130,224,184,132,
# bin_encode()

data = 'Hello'

## Decimal Encoding: (0-9)
# The problem is a byte may be two or three digits.
def dec_encode():
    for b in data:
        print(str(ord(b)), end=', ')
        ## '72', '101', '108', '108', '111'
    print()
    a =['72', '101', '108', '108', '111']
    print(''.join(a))   ## 72101108108111
# dec_encode()

## Hexadecimal Encoding: (0-9 and A-F)
# All bytes are two hex digits.
def hex_encode():
    for b in data:
        print(hex(ord(b)), end=', ')  # 0x48, 0x65, 0x6c, 0x6c, 0x6f,
    print()

    # hex() converts byte array to hex_string.
    hs = data.encode().hex()
    print(hs)                           # 48656c6c6f

    # bytes.fromhex() converts hex_string to byte array.
    print(bytes.fromhex(hs).decode())   # Hello
# hex_encode()

## Base64 Encoding: (a-z, A-Z, 0-9, =, /)
# Using more symbols, the result is shorter than equivalent hexadecimal.
import base64
def base64_encode():
    b64 = base64.b64encode(data.encode())
    print(b64.decode())                     # SGVsbG8=
    print(base64.b64decode(b64).decode())   # Hello
# base64_encode()

## Base58 Encoding: (base64, exclude 0, o, O, I, =, /)
# Less error prone but may be slightly longer than equivalent base64.
# pip install base58
import base58
def base58_encode():
    b58 = base58.b58encode(data) ## accepts str but returns bytes array.
    print(b58.decode())                     # 9Ajdvzr
    print(base58.b58decode(b58).decode())   # Hello
# base58_encode()

## Base58Check: (base58 + Checksum) allows error-checking.
# A checksum is 4 bytes.
def base58check_encode():
   b58c = base58.b58encode_check(data)
   print(b58c.decode())                         # vSxRbq6XzDhP
   print(base58.b58decode_check(b58c).decode()) # Hello
# base58check_encode()
