
from flask import Flask, render_template, request
from myutil import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

import csv, bitcoin
@app.route('/prepare', methods=['POST'])
def prepare():
   # verify admin password
   adminpwd = request.form['pwd']
   if not is_valid_pwd(adminpwd):
      return 'Invalid password'
   
   # create 'nameaddr' stream
   r = api.create('stream', 'energy', True)
   try:
      if r['error']:
         return str(r['error']['message'])
   except:
      api.subscribe('energy')

   # publish admin pwd to 'energy'
   api.publish('energy', 'admin', bitcoin.sha256(adminpwd))

   # read users list and publish.
   try:
      c = 0
      with open('data/users.csv') as f:
         for r in csv.DictReader(f):
            api.publish('energy', 'eligible', str_hex(r['name']))
            c += 1
##            print(r['name'])
      return 'There are %d users.' % c
   except:
      return 'Error reading users, please reset the Blockchain'

@app.route('/verifyadminpwd', methods=['POST'])
def verify_admin_pwd():
    pwd = request.form['pwd']
    return str(is_valid_admin_pwd(pwd))

@app.route('/verifyeligible', methods=['POST'])
def verify_eligible():
    name = request.form['name']
    return str(is_eligible(name))

@app.route('/verifyregistered', methods=['POST'])
def verify_registered():
    name = request.form['name']
    return str(is_registered(name))
    
#########################################################

@app.route('/registeruser', methods=['POST'])
def register_user():
   name = request.form['name']
   if not is_eligible(name):
      return 'Invalid user'

   if is_registered(name):
      return 'The voter is already registered'

   pwd = gen_pwd()
   json = {'name': name, 'pwd': bitcoin.sha256(pwd)}
   api.publish('energy', 'registered', {'json': json})
   return '{"name": %s, "pwd": %s}' % (name, pwd)

@app.route('/verifyuserpwd', methods=['POST'])
def verify_user_pwd():
    name = request.form['name']
    pwd = request.form['pwd']
    return str(is_valid_user_pwd(name, pwd))

#########################################################

@app.route('/sendtransfertx', methods=['POST'])
def send_transfer_tx():
    date = request.form['date']
    src = request.form['src']
    target = request.form['target']
    amount = request.form['amount']
    api.publish('energy', 'transfer', {'json': \
        {'date': date, 'src': src, 'target': target, 'amount': amount}})
    return 'success'

@app.route('/gettransferbydate', methods=['POST'])
def get_transfer_by_date():
    date = request.form['date']
    a = []
    for j in api.liststreamkeyitems('energy', 'transfer'):
       s = j['data']['json']
       if date == s['date']:
           a.append(str(s))
    return str(a)

@app.route('/gettransferbysrc', methods=['POST'])
def get_transfer_by_src():
    src = request.form['src']
    a = []
    for j in api.liststreamkeyitems('energy', 'transfer'):
       s = j['data']['json']
       if src == s['src']:
           a.append(str(s))
    return str(a)

#########################################################

@app.route('/sendconsumtx', methods=['POST'])
def send_consum_tx():
    date = request.form['date']
    consumer = request.form['consumer']
    etype = request.form['etype']
    amount = request.form['amount']
    api.publish('energy', 'consum', {'json': \
        {'date': date, 'consumer': consumer, 'etype': etype, 'amount': amount}})
    return 'success'

if __name__ == '__main__':
    app.run(port=8080, debug=True)


