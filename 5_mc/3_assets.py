from myutil import api

# Reset the Blockchain.
# python prepare.py    # Create 3 new addresses, create addr.bat, grant permissions.
# addr.bat             # set environment variables.

# Load addresses to Python variables.
a = api.getaddresses()  # set all addresses into the 'a' list.
# print(a)            # a[0] is 'add0', a[1] is 'add1', ...

#---------------------------------------------------------

# List assets:  (all issued assets)
#      multichain-cli chain1 listassets
def list_assets():
    for j in api.listassets():
        print(j['name'] , j['issueqty'])
# list_assets()         ## Initially there is no assets.

## Issue: asset to address
#      multichain-cli chain1 issue <addr> <asset> <amount> <subdivide>
# The issuer must be the 'root' or has 'admin' permission.
# <addr> is address of the receiver that has 'receive' permission.
# Return the 'txid' that issues the asset if success.
# By default the asset is 'closed', that means cannot be issued more.
# Issuing a closed asset more than once would fail.
def issue(recv, asset, amount, subd=1):
    r = api.issue(recv, asset, amount, subd)
    print(r)
# issue(a[1], 'as1', 100)  ## 'add0' issues 100 'as1' asset to 'add1'.
# issue(a[2], 'as2', 1000, 0.01)
# Try: list_assets() again.

## Get Asset Info of an asset:
#      multichain-cli chain1 getassetinfo <asset> <versbose>=false
# Try:
#      mc getassetinfo as1
#      mc getassetinfo as2 true
def get_asset_info(asset, versbose=False):
    r = api.getassetinfo(asset, versbose)
    print(r['name'], r['issueqty'])
# get_asset_info('as1')

## Get Address Balance of an address:
#      multichain-cli chain1 getaddressbalances <addr>
def get_addr_bal(addr):
    for x in api.getaddressbalances(addr):
        print(x['name'], x['qty'])
# get_addr_bal(a[1])
# get_addr_bal(a[2])


## Issue Form: allows issuing from an address that is
#   'non-root' nor 'admin' but have 'issue' permission.
#   multichain-cli chain1 issuefrom <from_addr> <to_addr> <asset> <amount> <subdivide>
# Try:
#       mc grant %add1% issue
#       mc issuefrom %add1% %add2% as3 3000 1
# get_addr_bal(a[2])

# By default, 'admin' address has 'issue' premission.
# Initially 'admin' does not own any asset but can issue assets to itself.
# get_addr_bal(a[0])         # empty
# issue(a[0], 'as0', 10)
# get_addr_bal(a[0])           # as0 10

## Get Total Balances of all addresses in the node:
#     multichain-cli chain1 gettotalbalances
def get_total_balances():
    for j in api.gettotalbalances():
        print(j['name'], j['qty'])
# get_total_balances()

#-------------------------------------------------------

## Send Asset:
#      multichain-cli chain1 sendasset <addr> <asset> <amount>
# <addr> is address of the receiver that has 'receive' permission.
# The sender is the 'root' or 'admin' that must have enough asset.
# Return 'txid' that send the asset if success.
def send_asset(recv, asset, amount):
    r = api.sendasset(recv, asset, amount)
    print(r)
# send_asset(a[1], 'as0', 3)    ## send 3 'as0' from add0 to add1

# Multichain handles the balances for both sender and receiver.
# The wallet take cares of sign and verify transactions.
# get_addr_bal(a[0])
# get_addr_bal(a[1])

## Send Asset Form: allows sending from an address that have 'send' permission.
#   multichain-cli chain1 sendassetfrom <from_addr> <to_addr> <asset> <amount>
def send_asset_form(from_addr, to_addr, asset, amount):
    print(api.sendassetfrom(from_addr, to_addr, asset, amount))
# send_asset_form(a[1], a[2], 'as1', 10)
# get_addr_bal(a[1])
# get_addr_bal(a[2])

# If the sender and receiver addresses are belong to the same node,
#  the total balances of the node does not change.
# get_total_balances()

#--------------------------------------------------------

## Send: allows sending a json in the form of {<asset>:<amount>} which may
#   contains more than one assets.
#   multichain-cli chain1 send <addr> <json>
#   multichain-cli chain1 sendfrom <from_addr> <to_addr> <json>
# Sending json allows more than one assets in a tx.
# Try:
#      mc sendfrom %add1% %add2% "{\"as0\":1, \"as1\":2}"
# get_addr_bal(a[1])
def send_from(from_addr, to_addr, json):
    print(api.sendfrom(from_addr, to_addr, json))
# send_from(a[1], a[2], {"as0":1, "as1":2})
# get_addr_bal(a[1])
# get_addr_bal(a[2])

## Sending Asset along with Metadata:
#   multichain-cli chain1 sendwithdata <addr> {<asset>:<amount>} <metadata>
#   multichain-cli chain1 sendwithdatafrom <from_addr> <to_addr> {<asset>:<amount>} <metadata>

# If <metadata> is just a text it much be a hex-string:
# Try:
#   mc sendwithdata %add2% "{\"as1\":1}" 123a
def send_with_data(addr, asset_amount, mdata):
    print(api.sendwithdata(addr, asset_amount, mdata))
from myutil import str_hex
# send_with_data(a[3], {'as0': 1}, str_hex('Hello'))

# <metadata> may be a json in the form of:  {"text": "<value>"}
# Try:
#   mc sendwithdata %add2% "{\"as1\":1}" "{\"text\": \"Hello how do you do?\"}"
#send_with_data(a[3], {'as0': 2}, {'text': 'Hi how do you do?'})

# <metadata> may be a json object:  {"json": {"id":"123", "name":"john"}}
# Try:
#   mc sendwithdata %add2% "{\"as1\":1}" "{\"json\": {\"id\":\"123\", \"name\":\"john\"}}"
#send_with_data(a[3], {'as0': 3}, {'json': {'id': 123, 'name': 'john'}})

# The metadata is stored in the tx, not the receiver address, so they
#   must be retrieved from the txs of a receiver address.

#-----------------------------------------------------------------

## List the last <n> transactions of an <addr>:
#          multichain-cli chain1 listaddresstransactions <addr> <n>
# Try:
#   mc listaddresstransactions %add3% 3
#   mc listaddresstransactions %add1% 1
# 'data' contains the metadata.
import myutil
def read_data(addr, n):
    for t in api.listaddresstransactions(addr, n):
        d = t['data'][0]
        if type(d) == str:
            print(myutil.hex_str(d))
        else:
            print(d)
# read_data(a[3], 1)

#-----------------------------------------------------------------

## Issuing 'open' asset:  (can be reissued more)
# The asset is described as json, with 'open' is true.
#   multichain-cli chain1 issue <recv> "{\"name\":<asset_name>, \"open\": true }" <amount> <subdivide>
#   multichain-cli chain1 issueform <form_addr> <to_addr> "{\"name\":<asset_name>, \"open\": true }" <amount> <subdivide>

# Try: Issue 'ax' asset to add1 as an opened asset:
#   mc issue %add1% "{\"name\":\"ax\", \"open\":true}" 100 1

## Issuing More:
#      multichain-cli chain1 issuemore <recv> <asset> <amount>
#      multichain-cli chain1 issuemoreform <form_addr> <to_addr> <asset> <amount>
# Try:
#          mc issuemore %add1% ax 200
# Check:
#          mc getaddressbalances %add1%
