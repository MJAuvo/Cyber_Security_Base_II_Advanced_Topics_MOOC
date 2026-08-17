import sys
import random

"""
Feistel ciphers are used as a building blocks in constructing many known block
ciphers.

In feistel cipher you are given a block cipher F that can encrypt a message of
length m. You are also given n keys (K1, ..., Kn)

Implement Feistel cipher:
Complete encrypt() and decrypt() in src/feistel.py.

The function F is a class parameter 'self.roundf', and 'keys' is an array in
class parameters 'self.keys'.

You can assume that the block size m of F is 4.
"""

class Hasher:
    def __init__(self, sbox):
        self.sbox = sbox

    def transform(self, key, data):
        # data is an array of size 4
        t = bytearray([key[i] ^ data[i] for i in range(4)])
        h = self.sbox[0][t[0]] + self.sbox[1][t[1]]
        h ^= self.sbox[2][t[2]]
        h += self.sbox[3][t[3]]
        h &= 0xFFFFFFFF # take care of overflow
        return h.to_bytes(4, 'little')

class Feistel:
    def __init__(self, keys, roundf):
        self.keys = keys
        self.roundf = roundf

    def encode(self, plain):
        # plain is an array of length 8
        cipher = bytearray(plain)

        # block size
        m = 4

        # divide into two halves
        L0 = bytearray(plain[:m])
        R0 = bytearray(plain[m:])

        # In each round, R goes through unchanged and L goes through an operation
        # that depends on R and the encryption key. R0 of the current round becomes
        # L1 for the next round. Output L0 of the current round becomes R1 for the
        # next round.
        for key in self.keys:
            L1 = R0
            enc_hash = bytearray(self.roundf(R0, key))
            R1 = bytearray(bytes([block^hash for block,hash in zip(L0, enc_hash)]))

            L0 = L1
            R0 = R1

        cipher = L0 + R0

        return cipher

    def decode(self, cipher):
		# cipher is a byte array of length 8
        plain = bytearray(cipher)

        # block size
        m = 4

        # divide into two halves
        L0 = bytearray(plain[:m])
        R0 = bytearray(plain[m:])

        # In decryption, keys used in encryption are used in reverse order
        reversed_keys = list(reversed(self.keys))

        # In each round, L goes through unchanged and R goes through an operation
        # that depends on L and the encryption key. L0 of the current round becomes
        # R1 for the next round. Output R0 of the current round becomes L1 for the
        # next round.
        for rev_key in reversed_keys:
            R1 = L0
            dec_hash = self.roundf(L0, rev_key)
            L1 = bytearray(bytes([block^hash for block,hash in zip(R0, dec_hash)]))

            L0 = L1
            R0 = R1

        plain = L0 + R0 

        return plain

def main(argv):
	sbox = [[random.getrandbits(32) for r in range(256)] for i in range(4)]
	hasher = Hasher(sbox) 

	keys = [random.getrandbits(32).to_bytes(4, 'little') for i in range(int(argv[2]))]
	f = Feistel(keys, hasher.transform)

	msg = argv[1]
	print('Message:', msg)

	cipher = f.encode(msg.encode())
	print('After encoding:', cipher)

	plain = f.decode(cipher)
	print('After decoding:', plain)

if __name__ == "__main__":
	if len(sys.argv) != 3 or len(sys.argv[1]) != 8:
		print('usage: python %s message rounds' % sys.argv[0])
		print('message should be 8 characters')
	else:
		main(sys.argv)
