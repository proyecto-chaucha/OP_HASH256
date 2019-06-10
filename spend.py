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

    if balance > 0:
        # Output
        outs = [{'address' : args.address, 'value' : int(balance*COIN)}]

        # Make unsigned transaction
        tx = mktx(ins, outs)

        # Calculate fee
        size = len(a2b_hex(tx))
        fee = int((size/1024)*0.01*COIN) 
        
        # MAX FEE = 0.1 CHA
        fee = 1e7 if fee > 1e7 else fee

        # sign inputs + apply fee
        unpacked = deserialize(tx)
        
        for puzzle_input in unpacked['ins']:
            puzzle_input['script'] = getHexLen(solution) + solution
            puzzle_input['script'] += getHexLen(scriptSig) + scriptSig
        
        unpacked['outs'][0]['value'] -= fee
        
        tx = serialize(unpacked)

        if len(tx) > 0:
            txid = broadcast(tx)
            print('> Transaction broadcasted, %s' % tx)
    else:
        print('> No funds :C')


if __name__ == '__main__':
    main()
