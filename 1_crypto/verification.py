import bitcoin as bc

pri = bc.random_key()
pub = bc.privkey_to_pubkey(pri)
addr = bc.pubkey_to_address(pub)

### Sign and Verify:
def sign_verify():
    ## Sign: msg with private key --> signature
    msg = 'Hello how do you do?'
    sig = bc.ecdsa_sign(msg, pri)
    print(sig)

    ## Verify: msg + signature + public key --> result (boolean)
    
    ## Try: modify the msg.
    # msg = 'Hello how do you do.'
    
    ## Try: invalid public key
    # pub = bc.privkey_to_pubkey(bc.random_key())
    
    print(bc.ecdsa_verify(msg, sig, pub))
##sign_verify()
    
## Any receivers that have the public key can verify the message.
##   but do not need to know the private key.
