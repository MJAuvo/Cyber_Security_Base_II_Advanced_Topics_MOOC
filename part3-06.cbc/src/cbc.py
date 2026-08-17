import sys
import random

"""
Complete 'Cbc' class by implementing encode and decode. Remember to add and
remove the padding. Note that you will also need the fully-implemented 'Feistel'
class from the previous exercise.

Hint:
You will probably find the xor helper function helpful. Do not forget add the
pad even if the message length is already a multiple of 8.
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

# Use class from Feistel exercise
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

# XORs two bytearrays of same legth
def xor(a, b):
	return bytearray([x ^ y for x, y in zip(a, b)])

class Cbc:
    def __init__(self, block):
        self.block = block 

    def encode(self, plain, iv):
        # plain is a byte array
        # iv is an initilization vector for cbc (byte array of length 8)
        # use self.block.encode() the blocks are length 8

        msg_length = len(plain)
        iv_length = len(iv)

        padding_length = msg_length % iv_length

        if padding_length == 0:
            padding_length = 8

        plain_padded = bytearray(plain)

        for i in range(padding_length):
            plain_padded.append(padding_length)

        cipher = bytearray()
        code_block = bytearray(iv)

        for i in range(int(len(plain_padded)/8)):
            plain_block = plain_padded[8*i:8*i+8]
            initialized_block = xor(plain_block, code_block)
            code_block = self.block.encode(initialized_block)

            cipher.extend(bytes(code_block))

        return cipher

    def decode(self, cipher, iv):
        # cipher is a byte array 
        # iv is an initilization vector for cbc (byte array of length 8)
        # use self.block.encode() the blocks are length 8

        code_block_next = bytearray(iv)
        plain_padded = bytearray()
        padding_length = 0

        for i in range(int(len(cipher)/8)):
            code_block_init = cipher[8*i:8*i+8]
            initialized_block = self.block.decode(code_block_init)
            plain_block = xor(initialized_block, code_block_next)
            code_block_next = code_block_init

            plain_padded.extend(plain_block)

        padding_length = int(plain_padded[-1])
        plain = plain_padded[:-padding_length]

        return plain

def main(argv):
	sbox = [[random.getrandbits(32) for r in range(256)] for i in range(4)]
	hasher = Hasher(sbox) 

	keys = [random.getrandbits(32).to_bytes(4, 'little') for i in range(int(argv[2]))]
	f = Feistel(keys, hasher.transform)

	cbc = Cbc(f)

	iv = bytearray(8)
	msg = argv[1]
	print('Message:', msg)

	cipher = cbc.encode(msg.encode(), iv)
	print('After encoding:', cipher)

	plain = cbc.decode(cipher, iv)
	print('After decoding:', plain)

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print('usage: python %s message rounds' % sys.argv[0])
	else:
		main(sys.argv)
