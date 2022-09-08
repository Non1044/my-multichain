import bitcoin
import hashlib     # A standard Python's lib
# print(hashlib.algorithms_available)

msg = 'Hello! how are you today.'
msg_bin = msg.encode()      # bytes array
def hash_test():
    # Md5
    md5 = hashlib.md5(msg_bin) # Md5 hashed object
    md5_str = md5.hexdigest()       # str
    print(len(md5_str), md5_str)    # 32 chars (16 bytes)

    # Sha1
    sha1 = hashlib.sha1(msg_bin)
    sha1_str = sha1.hexdigest()
    print(len(sha1_str), sha1_str)  # 40 chars (20 bytes)

    # Sha256.
    sha256 = hashlib.sha256(msg_bin)
    sha256_str = sha256.hexdigest()
    print(len(sha256_str), sha256_str)  # 64 chars (32 bytes)

    # Bitcoin uses Sha256.
    # 'bitcoin' Python lib provides easy to used hash functions.
    print(bitcoin.sha256(msg))
# hash_test()              # Must be consistence on all runs.

# Tamper Proof: verification to check that data had been modified.
def tamper_proof():
    # Store a message and hash.
    hash = bitcoin.sha256(msg)
    # print(hash)

    # Verify the message
    new_hash = bitcoin.sha256('Hello! how are you today?')
    if hash != new_hash:        ## Try: modify the message.
        print('Invalid')
    else:
        print('Valid')
# tamper_proof()

# To verify if a file had been modified.
def hash_file(infile, outfile):
    try:
        with open(infile, 'r') as df:
            data = df.read()
            with open(outfile, 'w') as hf:
                hf.write(bitcoin.sha256(data))
        return 'Success'
    except FileNotFoundError as er:
        return er
# print(hash_file('hash.py', 'tmp'))

# Return True if the file is not modified.
def varify_file(infile, outfile):
    try:
        with open(infile, 'r') as df:
            dh = bitcoin.sha256(df.read())
            with open(outfile, 'r') as hf:
                return dh == hf.read()
    except FileNotFoundError as er:
        return er
# print(varify_file('hash.py', 'tmp'))

#-------------------------------------------------

# Password Hashing:
# User passwords should never be directly saved in any machines.
def pwd_hash():
    def name_pwd_hash(name, pwd):
        return bitcoin.sha256((name+pwd))

    # For simplicity we use a dict instead of file or database.
    d = {}
    def register(name, pwd):
        d[name] = name_pwd_hash(name, pwd)

    # Return True if the name and pwd is valid.
    def login(name, pwd):
        return d.get(name) == name_pwd_hash(name, pwd)

    register('John', 'hello123')
    print(login('John', 'hello124'))
    print(login('john', 'hello123'))
    print(login('John', 'hello123'))
# pwd_hash()

# Hash References:
def hash_ref():
    # Create an empty dict to store <key>:<value>.
    d = { }

    ## Store a value using the value hash as key.
    v = 'Hello'
    k = bitcoin.sha256(v)
    d[k] = v        #  <dict>[<key>] = <value>

    ## If key is modified.
    # k = bitcoin.sha256('Hi')

    # Get value by key
    print(d.get(k, None))

    # If the value (in dict) is modified.
    # d[k] = 'Hello'
    print(k == bitcoin.sha256(d[k]))
# hash_ref()

# Blockchain Ex:
# Assume that a block is an item of the form [<previous block hash>, <data>].
def blockchain_ex():
    d = { }
    last = None

    ## Add blocks to the blockchian, suppose a block data is just a name.
    for data in ['John', 'Jack', 'Joe', 'Jame', 'Jim']:
        hash = bitcoin.sha256(data)
        d[hash] = [last, data]
        last = hash

    def print_all_blocks():
        h = last
        while h != None:
            print(d[h])
            h = d[h][0]
        print()
    # print_all_blocks()

    # To verify the blockchain
    def verify():
        if last != bitcoin.sha256(d[last][1]):
            print('last block error')
            return
        h = last
        while h != None:
            previous_hash = d[h][0]
            if previous_hash != None and previous_hash != bitcoin.sha256(d[previous_hash][1]):
                print('broken link')
                return
            h = d[h][0]
        print('valid')
    # verify()

    ## Get Joe's block reference
    jim_k = last; jame_k = d[jim_k][0]; joe_k = d[jame_k][0];
    # Modify Joe's block
    d[joe_k][1] = 'joe'  ## change Joe's name
    # verify()
# blockchain_ex()

## Proof of Work:
# Suppose 'diff' is the number of preceeding zeros .
def pow(diff):
    target = '0'*diff
    nonce = 0
    while True:
        h = bitcoin.sha256(msg+str(nonce))
        if h.startswith(target):
            print('%d: %d\t%s' % (diff, nonce, h))
            break
        nonce += 1
def pow_test():
    for i in range(1, 4):
        pow(i)
# pow_test()

# There are two alternatives to define the target.
# Ex. Get a block from the Blockchain.
# bitcoin-cli getblockhash 277316
# bitcoin-cli getblock 0000000000000001b6b9a13b095e96db41c4a928b97ef2d944a9b31b2cc7bdc4
#      "bits"       : "1903a30c"
#      "difficulty" : 1180923195.25802612

# bits -> target:
# bits is <EE><CCCCCC>  that means <cof><exp>
# target = cof * (2**(8 * (exp -3)))   (64 hex digits with 0 left filled)
def bits(exp, cof):
    t = cof * (2**(8 * (exp -3)))   ## int
    h = '{:x}'.format(t)            ## int to hex string
    # print(len(h), h)

    # fill left zero until the length is 64 digits
    while len(h) < 64:
        h = '0' + h
    print(len(h), h)
# bits(0x19, 0x03a30c)  ## "bits": "1903a30c"

# difficulty is max_target/target
max_target = 0x00000000FFFF0000000000000000000000000000000000000000000000000000
def difficulty(d):
    target = max_target / d         ## float
    t = str(hex(int(target))[2:])
    # print(len(t), t)

    while len(t) < 64:
        t = '0' + t
    print(len(t), t)
# difficulty(1180923195.25802612)
