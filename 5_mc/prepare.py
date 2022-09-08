from myutil import api

## Create 3 addresses.
api.getnewaddress()
api.getnewaddress()
api.getnewaddress()

# Save the addresses to 'addr.bat' file.
a = api.getaddresses()
with open('addr.bat', 'w') as f:
    for i in range(0, 4):
        print('add%s = %s' % (i, a[i]))
        f.write('set add%s=%s\n' % (i, a[i]))
print()

# Grant 'receive,send' permissions to the addresses.
api.grant(a[1] + ',' + a[2] + ',' + a[3], 'receive,send')
for p in api.listpermissions():
    print(p['address'] , p['type'])
