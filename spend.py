from argparse import ArgumentParser
from binascii import a2b_hex
from struct import unpack
from functions import *
from bitcoin import scriptaddr, deserialize, serialize, \
                    multisign, mktx

# Arguments
p = ArgumentParser(description='Transaction puzzle creator (OP_SHA256)')
p.add_argument('solution', help='Puzzle solution')
p.add_argument('address', help='Send to address')
args = p.parse_args()

def main():
    scriptSig = getScriptPubKey(args.solution)
    addrP2SH = scriptaddr(scriptSig, 50)
    solution = b2a_hex(args.solution.encode()).decode('utf-8')

    ins, balance = getBalance(addrP2SH)
    len_inputs = len(ins)

    tx = ''

    if balance > 0:
        # Fee
        fee = round(base_fee + fee_per_input * len_inputs, 8)

        # Output
        out_value = int((balance - fee) * COIN)
        outs = [{'address' : args.address, 'value' : out_value}]

        # Make unsigned transaction
        tx = mktx(ins, outs)

        # sign inputs
        unpacked = deserialize(tx)
        unpacked['ins'][0]['script'] = getHexLen(solution) + solution
        unpacked['ins'][0]['script'] += getHexLen(scriptSig) + scriptSig
        tx = serialize(unpacked)

        if len(tx) > 0:
            txid = broadcast(tx)
            print('> Transaction broadcasted, %s' % txid.text)
    else:
        print('> No funds :C')


if __name__ == '__main__':
    main()
