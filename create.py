from argparse import ArgumentParser
from bitcoin import scriptaddr
from binascii import b2a_hex
from functions import *

# Arguments
p = ArgumentParser(description='Transaction puzzle creator (OP_SHA256)')
p.add_argument('solution', help='Puzzle solution')
args = p.parse_args()

def main():
    scriptpubkey = getScriptPubKey(args.solution)
    addrP2SH = scriptaddr(scriptpubkey, 50)
    print('> P2SH Address: %s' % addrP2SH)


if __name__ == '__main__':
    main()
