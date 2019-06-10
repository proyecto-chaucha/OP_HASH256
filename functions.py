from hashlib import new
from requests import get, post
from binascii import b2a_hex

OP_EQUAL = '87'
OP_HASH256 = 'aa'
OP_PUSHDATA1 = '0a'

COIN = 100000000
ADDRESS_PREFIX = 50

def broadcast(tx):
    url = 'https://explorer.cha.terahash.cl/api/tx/send'
    return post(url, data={'rawtx' : tx})

def getHexLen(s):
    return '{:02x}'.format(int(len(s)/2))

def getScriptPubKey(s):
    hash = new('sha256', new('sha256', s.encode()).digest()).hexdigest()
    return OP_HASH256 + getHexLen(hash) + hash + OP_EQUAL

def getBalance(addr):
    url = 'http://insight.chaucha.cl/api/addr/'
    unspent = get(url + addr + '/utxo').json()

    inputs = []
    balance = 0

    for i in unspent:
        if i['confirmations'] >= 1:
            input = {'output' : i['txid'] + ':' + str(i['vout']),
                     'value' : i['satoshis'],
                     'address' : i['address']}
            balance += i['satoshis']
            inputs.append(input)

    return [inputs, round(balance/COIN, 8)]
