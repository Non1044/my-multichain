from requests import post, get

def do_get(path):
   return get(path).content.decode()

def do_post(path, data):
   return post(path, data=data).content.decode()

print(do_get('http://127.0.0.1:8080/getinfo'))
print(do_post('http://127.0.0.1:8080/verifyaddr', data={'addr': '1MDLPJrwyEbDg6xk8JiuTr33ZCPtT2BNTtoMx1'}))





