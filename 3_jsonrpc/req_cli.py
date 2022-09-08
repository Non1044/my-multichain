## pip install requests

import requests
url = 'http://localhost:1234'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
user = "multichainrpc"
password = "52TH6uU5onYPrwGoZzMittjoEjg9iZS6rDi8i3aVQjNi"

method = 'getinfo'; param = []
##method = 'listaddresses'; param = []
##method = 'validateaddress'; param = '["13DX7WcdS1GKnWeKdYTYJcyXNYG8oLPqA266qr"]'
data = '{"method": "%s","params": %s, "id": 1, \
	 "chain_name":"chain1"}' % (method, param)
res = requests.post(url, data=data, headers=headers, auth=(user,password))
# print(res.text)

from myutil import *
print_json(res.text)


