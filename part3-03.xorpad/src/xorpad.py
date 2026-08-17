#!/usr/bin/env python3
import sys
import socket

"""
Implement a xorpad cipher:
complete encrypt() and decrypt() functions in src/xorpad.py. Both functions are
byte arrays and should output an byte array as an output.

The pad can be significantly shorter than the message. In such a case you should
repeat the pad as long as needed.

Note that repeating short pads is highly problematic, for example, one can
deduce the pad if a short part of message is known in advance (can you figure
out how?). Thus, this should not be used in practice.
"""

def encrypt(msg, pad):
    # both msg and pad are byte arrays
    ciphertext = bytearray(len(msg))

    # write code here
    pad_length = len(pad)

    for i in range(len(msg)):
        char_bytes_message = msg[i]
        char_bytes_pad = pad[i % pad_length]

        char_bytes_cipher = char_bytes_message ^ char_bytes_pad
        ciphertext[i] = char_bytes_cipher

    return ciphertext


def decrypt(ciphertext, pad):
    # both ciphertext and pad are byte arrays
    msg = bytearray(len(ciphertext))

    # write code here
    pad_length = len(pad)
    for i in range(len(ciphertext)):
        char_bytes_ciphertext = ciphertext[i]
        char_bytes_pad = pad[i % pad_length]

        char_bytes_msg = char_bytes_ciphertext ^ char_bytes_pad
        msg[i] = char_bytes_msg

    return msg

def main(argv):
    msg = argv[1]
    pad = argv[2]

    print("Plain message:")
    print(msg)
    print("\nPad:")
    print(pad)

    cipher = encrypt(msg.encode(), pad.encode())

    print("\nCipher text (as integer array):")
    print(list(cipher))

    decoded = decrypt(cipher, pad.encode())

    print("\nDecoded text (as integer array):")
    print(list(decoded))
    print("\nDecoded plain text:")
    print(decoded.decode())

# This makes sure the main function is not called immediatedly
# when TMC imports this module
if __name__ == "__main__": 
	if len(sys.argv) != 3:
		print('usage: python %s msg pad' % sys.argv[0])
	else:
		main(sys.argv)
