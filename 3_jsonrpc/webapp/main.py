## pip install flask

from flask import Flask, render_template, request
from myutil import api

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getinfo')
def getinfo():
    result = api.getinfo()
    d = dict()
    d['nodeaddress'] = result['nodeaddress']
    d['blocks'] = result['blocks']
    d['connections'] = result['connections']
    return str(d)

@app.route('/verifyaddr', methods=['POST'])
def verify_addr():
    addr = request.form['addr']
    result = api.validateaddress(addr)
    return str(result['isvalid'])

if __name__ == '__main__':
    app.run(port=8080, debug=True)
