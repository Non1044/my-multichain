from myutil import api

## MultiChain Permissions:
#  - Low Risk:
#      'connect' to other blockchains.
#      'send' and 'receive' transactions.
#  - Medium Risk:
#      'issue' assets
#      'create' streams
#      'activate' manage other address’s low risk permissions.
#  - High Risk:
#      'admin' modify all other addresses permissions.
#      'mine' participate in consensus race.
# The first address of the first node is the 'root' address,
#  which has all permissions.

# List permissions: (of addresses that have any permissions)
#      multichain-cli chain1 listpermissions
# Try: mc listpermissions

# Initially there is only the 'root' address.
# All addresses created later do not have any permissions.
# The first address on other nodes should be granted 'admin' permission by the 'root'.
def list_perms():
    for j in api.listpermissions():
        print(j['address'] , j['type'])
# list_perms()

# 'params.dat' defines default permissions for other users.
# Check anyone-can-* in the 'params.dat':
#      multichain-cli chain1 getblockchainparams
def anyone_can():
    for (k, v) in api.getblockchainparams().items():
        if k.startswith('anyone-can'):
            print('%s:\t %s' % (k, v))
# anyone_can()

# Set the 'root' address to be 'add0'.
#       mc getaddresses
add0 = '1MiG6rERgGATedrvSSPsi8WDD858mTew8PoCBk'

# Create 3 new addresses for variables 'add1', 'add2' and 'add3'
#       mc getnewaddress
# Set Python variables:
add1 = '1PtESTMDYJ4fM7Rqz5FavoXe9B1wSC5ua6NJEG'
add2 = '16rcH5pFMVZ5uxVvF9GYUTPb8Vs193hyJGsdcN'
add3 = '12vjrfEmDVHafD8x219KaSDvKcjCZdoxXfTEtj'

## Set Windows Environment variables:
'''
set add0=1MiG6rERgGATedrvSSPsi8WDD858mTew8PoCBk
set add1=1PtESTMDYJ4fM7Rqz5FavoXe9B1wSC5ua6NJEG
set add2=16rcH5pFMVZ5uxVvF9GYUTPb8Vs193hyJGsdcN
set add3=12vjrfEmDVHafD8x219KaSDvKcjCZdoxXfTEtj
'''

## List Permissions: of all addresses hat have some permissions:
#      multichain-cli chain1 listpermissions <perm>
# <perm> may be a list, separated by ','.
# Try:
#   mc listpermissions send
#   mc listpermissions send,receive

## List specified permissions of addresses:
#      multichain-cli chain1 listpermissions <perm> <addr>
# <perm> and <addr> may be lists, separated by ','.
# Try:
#       mc listpermissions send %add0%
#       mc listpermissions receive,send %add0%,%add1%
def list_perm(perm, addr=None):
    for j in api.listpermissions(perm, addr):
        print(j['address'], j['type'])
# list_perm('send')
# list_perm('send', add1)
# list_perm('send,receive')
# list_perm('send,connect', add0 + ',' + add1)

#----------------------------------------------------------------

## Grant permissions to addresses:
#      multichain-cli chain1 grant <addr> <perm>
# Permissions are properties of individual address.
# <addr> and <perm> may be lists, separated by ','.
# The granter must be the 'root'.
# Try:
#       mc grant %add1% connect
#       mc grant %add2%,%add3% receive,send
# Return the 'txid' that creates the permissions.
def grant(addr, perm):
    print(api.grant(addr, perm))
# grant(add1, 'connect')
# grant(add2 + ',' + add3, 'receive,send')

## Grant permissions from specified address to another address:
#   multichain-cli chain1 grantfrom <from_addr> <to_addr> <perm>
# <to_addr> and <perm> may be lists, separated by ','.
# <from_add> may be the 'root' or has 'admin' or 'activate' permission.
# Try:
#       mc grantfrom %add0% %add1% admin
#       mc grantfrom %add1% %add2% activate
#       mc grantfrom %add2% %add3% connect

#-------------------------------------------------------------------

## Revoke permissions:
#   multichain-cli chain1 revoke <addr> <perm>
#   multichain-cli chain1 revokefrom <from_add> <to_add> <perm>
# <perm> and <perm> may be lists, separated by ','.
# Return the 'txid' that revokse the permissions.
# Try:
#      mc revokefrom %add0% %add3% connect

## 'admin' VS 'activate':
# The 'admin' address may grant 'activate' permission to other
#  nodes for managing their own address permissions.
# An address with 'activate' permission may manage its own
#  and other address’s low risk permissions.
# Suppose 'add1' does not have 'activate' permission.
# Try:
#       mc grantfrom %add1% %add2% send      # fail
#       mc grantfrom %add0% %add1% activate
# Then try granting 'send' permission from 'add1' again.

# An address with 'activate' permission may modify its low risk
#  permissions, but not medium nor high risk permissions.
# Try:
#       mc grantfrom %add1% %add1% issue     # fail
#       mc grantfrom %add0% %add1% issue

# The 'admin' and 'activate' permissions are not forever,
#   they will last to the 'endblock' only.

#-----------------------------------------------------------

## Setup Period:
# When a node is started up, the administrator rules are not applied
#   for the period of 'setup-first-blocks' which is called setup period.
# The default setup period is defined in 'params.dat'.
# Try:
#       mc getblockchainparams      # 'setup-first-blocks' is 60.
# Or:   mc getblockchaininfo        # 'setupblocks' is 60
# That means the administrator rules will be effective after 60 blocks.
# If we do not want to wait for 60 blocks,
#   we can change the 'setup-first-blocks' value.

## Approve Factors:
# 'params.dat' defines some of 'admin-consensus-*'
# The default 'admin-consensus-admin' is 0.5
# That means any change to the 'admin' permission must be approved by number
#  of admin at least 0.5*(the current number of administrators) rounded up.

# If there is 1 admin, we need at least (0.5*1 ->) 1 admin to
#  approve 'admin' permission to the second address.

# Try: Create another Multichain with setup parameters:
# multichain-util create chain2 -setup-first-blocks=1 -admin-consensus-admin=0.6

## Verify params.dat
#          setup-first-blocks = 1
#          admin-consensus-admin = 0.6
# Try:
#       start multichaind chain2 -daemon
#       multichain-cli chain2 getblockchainparams
#       multichain-cli chain2 getblockchaininfo

# If there is 2 admin, we need at least (0.6*2 ->) 2 admin to
#  approve the 'admin' permission to the thrid address.
# Try:
#       multichain-cli chain2 listpermissions admin
#       set add1=1LK4wSTzVck1fUvxFbDVExvX2iNrTqjmrhwdS2
#       multichain-cli chain2 getnewaddress
#       set add2=15hDjYrioSV8MpH3Wa6a7bykLbJWc82TyTwtNM
# Grant 'admin' permission to add2.
#       multichain-cli chain2 grantfrom %add1% %add2% admin
# List addresses that have 'admin' permission.
#       multichain-cli chain2 listpermissions admin

#       multichain-cli chain2 getnewaddress
#       set add3=15r3oN2GZ3df3KYKHkABMrwCGsZPjB81p9UojX
# Grant 'admin' permission to add3.
#       multichain-cli chain2 grantfrom %add1% %add3% admin
# The transaction was success but only the add1 and add2 have the 'admin' permission.
#       multichain-cli chain2 listpermissions admin
# The 'admin' permission of add3 is pending.
# Grant 'admin' permission from add2 to add3.
#       multichain-cli chain2 grantfrom %add2% %add3% admin
#       multichain-cli chain2 listpermissions admin

# The same logic applies for the 'issue', 'create', 'activate'
#   and 'mine' permissions, each of which has a corresponding
#   'admin-consensus-*' blockchain parameter.
# Ex. If there are 3 admins and admin-consensus-issue=0.8, we need
#  0.8*3 -> 3 admin to approve 'issue' permission to the fourth address.
