# pip install bitcoin
from myutil import api

## Off-Wallet Keys:
# Multichain nodes may perform wallet functionality.
# It allows creating private/public keys but not stored in the node.
#       multichain-cli chain1 createkeypairs <count>=1
# <count> defines the number of pairs to be generated.
# Try:
#     mc createkeypairs
#     mc createkeypairs 2
def mc_keys():
    r = api.createkeypairs()
    # print(r)
    pri = r[0]['privkey']
    pub = r[0]['pubkey']
    addr = r[0]['address']
    print(len(pri), pri)    ## (56 char) wif private key
    print(len(pub), pub)    ## (66 char) compressed hex public key
    print(len(addr), addr)  ## (38 char) wif compressed address
# mc_keys()

# Multichain key system is a modified version of Bitcoin keys.
import bitcoin as bc
def bc_key():
    # Bitcoin keys:
    bc_pri = bc.random_key()    ## uncompressed private key
    print(len(bc_pri), bc_pri)  ## 64 774ac32fea92cf596a552b9d906383130a2615164f6062d25b9355e683b54ed6
    comp_bc_pri = bc_pri + '01' ## compressed private key
    dec_comp_bc_pri = bc.decode_privkey(comp_bc_pri, 'hex')
    wif_comp_bc_pri = bc.encode_privkey(dec_comp_bc_pri, 'wif')
    print(len(wif_comp_bc_pri), wif_comp_bc_pri)  ## (26 bytes) Bitcoin WIF private key
                                ## 52 L1DbhMh2GuZX7UPjgfFfEqU7gy7mBaTjBAm6uD7kQFgpD3P2LWfe
    # Multichain Keys:
    kp = api.createkeypairs()
    mc_pri = kp[0]['privkey']   ## (28 bytes) Multichain WIF private key
    print(len(mc_pri), mc_pri)  ## 56 V5W7rx6foPm5ydgVENjezjHkTQucKSbFeLHNcQ4J5pt52rLT9hsYsQzQ

    # Bitcoin keys are not valid on Multichain by default.
    # Validate Multichain keys or addresses (in the mode):
    #      multichain-cli chain1 validateaddress <key|address>
    print(api.validateaddress(bc_pri))  ## {'isvalid': False}
    print(api.validateaddress(mc_pri))
    # {'isvalid': True, 'address': '1AJPppxvkY35vpGuHUE6NDz2zpxgbSuGGsF6A1', 'ismine': False}
    # 'ismine' indicates the <key|address> is registered to the node.
# bc_key()

## Sign and Verify Message:
#   multichain-cli chain1 signmessage <private key> <message>
#   multichain-cli chain1 verifymessage <address> <signature> <message>
def sign_verify():
    r = api.createkeypairs()
    pri = r[0]['privkey']
    addr = r[0]['address']

    # Sign message with private key:
    msg = 'Hello how do you do?'
    sig = api.signmessage(pri, msg)
    print(sig)

    # Verify message and sigature with address:
    # msg = 'Hello how do you do.'              Try: modify msg
    print(api.verifymessage(addr, sig, msg))    ## True
# sign_verify()

#-----------------------------------------------------------

## In-Wallet Address:
# Get New Address: (Its private key is stored in the node, 'ismine' is True).
#      multichain-cli chain1 getnewaddress
# addr = api.getnewaddress(); print(addr)
# Try:      mc getnewaddress

# Get Addresses: all addresses in the node as a list of str.
#      multichain-cli chain1 getaddresses
# print(api.getaddresses())
# Try:      mc getaddresses

# List Addresses: provides more info of all addresses in the node
#  as list of json('ismine' is True).
#      multichain-cli chain1 listaddresses
# print(api.listaddresses())
# Try:      mc listaddresses

##--------------------------------------------------------------------

# Import Address:
#      multichain-cli chain1 importaddress <addr> <scan>
# The <addr> is an off-wallet address which may created on other node
# It is imported to be handled in the node but 'ismine' is still False.
# <scan> is a str to specify tracking the transactions of that <addr>.
def import_test():
    # Create an off-wallet key.
    keys = api.createkeypairs()
    addr = keys[0]['address']
    print(addr)

    [print(a) for a in api.listaddresses()]  # The 'addr' is not shown.

    # The importer must have the permissions to import.
    try:
        r = api.importaddress(addr, 'True')   # 'True' is a str.
        if r == None:                         # Success return None.
            print('Success')
        else:
            print(r['error']['message'])
    except:
        print('Import fails.')
        return

    [print(a) for a in api.listaddresses()]  # 'addr' is shown but 'ismine': False.
 import_test()


######################################################################

#      https://www.multichain.com/developers/address-key-format
# Multichain private keys have extra 4 bytes prefix (for representing
#  nodes) and 4 bytes modified chacksun. That allows 2**64 more spaces
#  over Bitcoin private keys. And ensures that keys generated in a node
#  will never be the same as generated on other nodes.

# By default these values are generated randomly when a new chain is created
#  which can be between 1 and 4 bytes in length, but they must all be the same length.
#      multichain-cli chain1 getblockchainparams
def params():
    r = api.getblockchainparams()
    print('address-pubkeyhash-version: ', r['address-pubkeyhash-version'])
    print('address-scripthash-version: ', r['address-scripthash-version'])
    print('private-key-version: ', r['private-key-version'])
    print('address-checksum-value: ', r['address-checksum-value'])
params()

# If we want to use Bitcoin keys on Multichain, set the following values:
#      address-pubkeyhash-version=00
#      address-scripthash-version=05
#      private-key-version=80
#      address-checksum-value=00000000
# Which would be easiser with creating a new chain.
#    multichain-util create chain2 -address-pubkeyhash-version=00 -address-scripthash-version=05 -private-key-version=80 -address-checksum-value=00000000
# start multichaind chain2 -daemon
#    multichain-cli chain2 createkeypairs
# Check with: bitaddress.org
