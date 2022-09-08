import bitcoin
import random

## Private key:
# 'bitcoin' lib provides N for the max private key.
def max_prikey():
    print(bitcoin.N)
    nh = hex(bitcoin.N)[2:]  # exclude prefix '0x'.
    print(len(nh), nh)       # 64 hex-digits (32 bytes)
# max_prikey()

# A private keys is a non-negative interger that less than bitcoin.N.
seed = 'Hello'
def private_key(): # All methods result private keys as hex string.
    # Generate private key randomly.
    for _ in range(3):
        print(hex(random.randint(1, bitcoin.N))[2:])
    print()

    # bitcoin.sha256(<seed>) with a slim chance of overflow bitcoin.N.
    # But can repeatedly generated from the <seed>.
    for _ in range(3):
        print(bitcoin.sha256(seed))
    print()

    # bitcoin.random_key() results a random valid private key.
    for _ in range(3):
        print(bitcoin.random_key())
# private_key()

## Public Keys:
# G is a constant tuple (x, y) of a point on Elliptic Curve.
# print(bitcoin.G)

## A public key is a 130 hex-digits (65 bytes).
# A public key is computed from a corresponding private key.
#           <public key>  is  G * <private key>
def public_key():
    # Generate the same private key from a seed.
    hex_priv = bitcoin.sha256(seed)

    # Decoded private key: from hex to decimal.
    dec_priv = bitcoin.decode_privkey(hex_priv, 'hex')
    print(dec_priv)

    # fast_multiply() with G
    dec_pub = bitcoin.fast_multiply(bitcoin.G, dec_priv)
    print(dec_pub)      # A tuple (x, y).

    # Encode decimal to hex string.
    hex_pub = bitcoin.encode_pubkey(dec_pub, 'hex')
    print(hex_pub)

    # 'bitcoin' lib provides functions to compute public key from private key.
    print(bitcoin.privkey_to_pubkey(hex_priv))   # Alternatively: bitcoin.privtopub()
    # Public keys are prefixed with '04', try changing the seed.
# public_key()

def compressed():
    # Uncompressed private key:
    pri_key = bitcoin.sha256(seed)
    print(pri_key)
    # 185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969

    # Compressed private key:
    # Adding '01' suffix to indicate it is a compressed private key.
    comp_pri_key = pri_key + '01'
    print(comp_pri_key)
    # 185f8db32271fe25f561a6fc938b2e264306ec304eda518007d176482638196901

    # Uncompressed public key: computed from uncompressed private key.
    pub_key = bitcoin.privkey_to_pubkey(pri_key)
    print(pub_key)
    # 0468191146d1581310fb2d11caafcc87acb0fc3ce5ad7f26e17be1c3da08d1d4dabc0528e05e78fec33f6dab4c12e4ef36dd816834630ab1a31b0746762358972f

    # Compressed public key: computed from compressed private key.
    comp_pub_key = bitcoin.privkey_to_pubkey(comp_pri_key)
    print(comp_pub_key)
    # 0368191146d1581310fb2d11caafcc87acb0fc3ce5ad7f26e17be1c3da08d1d4da
    # Compressed public keys use less space thus reduce the size of tx.

    # Public keys are big even the compressed version.
    # An address is computed from a corresponding public key.
    # Uncompressed address: computed from uncompressed public key.
    print(bitcoin.pubkey_to_address(pub_key))
    # 1AFAEr2oY7HQp7L7sxyHCfXBFf7zo935sv

    # Compressed address: computed from compressed public key.
    print(bitcoin.pubkey_to_address(comp_pub_key))
    # 1P8txSS7i5CieqAgMXBBCXyDtFu5NgUwMX
# compressed()            ## Check with: bitaddress.org

## WIF and Addresses:
def wif_encode():
    ## Uncompressed private key
    pri_key = bitcoin.sha256(seed)
    print(pri_key)      ## 185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969
    ## Compressed private key
    comp_pri_key = pri_key + '01'
    print(comp_pri_key) ## 185f8db32271fe25f561a6fc938b2e264306ec304eda518007d176482638196901

    ## Decoded Private Key.
    dec_pri = bitcoin.decode_privkey(pri_key, 'hex')
    comp_dec_pri = bitcoin.decode_privkey(comp_pri_key, 'hex')

    ## Wif uncompressed Private Key (begins with 5).
    wif_pri = bitcoin.encode_privkey(dec_pri, 'wif') ## to 'wif'
    print(wif_pri)
    # 5J12ASfjmVAX7efMjvvr4h4Q19xd4wZPPEf9dqiLda8QtWAT93b

    ## Wif uncompressed Private Key (begins with K or L).
    comp_wif_pri = bitcoin.encode_privkey(comp_dec_pri, 'wif') ## to 'wif'
    print(comp_wif_pri)
    # Kx368gHymMK1vMEJYV2fZHozXgYWCPowo9HP7c1TeRDiSCsZ8t3A

    # WIF Uncompressed address:
    print(bitcoin.privkey_to_address(wif_pri))
    # 1AFAEr2oY7HQp7L7sxyHCfXBFf7zo935sv

    # WIF Compressed address:
    print(bitcoin.privkey_to_address(comp_wif_pri))
    # 1P8txSS7i5CieqAgMXBBCXyDtFu5NgUwMX
            ## Addresses are wif encoded.
# wif_encode()

#-----------------------------------------------------------------

def sign_verify():
    pri = bitcoin.random_key()
    pub = bitcoin.privkey_to_pubkey(pri)

    # Sign a msg with private key --> signature
    msg = 'Hello how do you do?'
    sig = bitcoin.ecdsa_sign(msg, pri)
    print(sig)

    # Verify a msg + signature + public key --> result (boolean)

    # Try: modify the msg.
    # msg = 'Hello how do you do.'

    # Try: invalid public key
    # pub = bitcoin.privkey_to_pubkey(bitcoin.random_key())

    print(bitcoin.ecdsa_verify(msg, sig, pub))
sign_verify()

## Any receivers that have the public key can verify the message.
##   but do not need to know the private key.
