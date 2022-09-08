## pip install savoir
from Savoir import Savoir

rpcuser = 'multichainrpc'
rpcpasswd = '52TH6uU5onYPrwGoZzMittjoEjg9iZS6rDi8i3aVQjNi'
rpchost = '127.0.0.1'
rpcport = '1234'
chainname = 'chain1'
api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
