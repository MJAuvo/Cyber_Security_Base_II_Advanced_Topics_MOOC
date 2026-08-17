#!/usr/bin/env python3
import sys
import socket

import random
from string import ascii_lowercase # string containing all lower-case alphabets letters

"""
Implement a simple frequency attack against a substitution cipher:
Complete decode() in decode.py. The function is given a string ciphertext and
dictionary frequencies, where frequencies[c] is a float indicating how frequent
is the letter. The output of the function should be a string (not byte array).

You can assume that ciphertext and the output do not use capital letters.
Non-characters (spaces, enters) are not changed.

Furthermore, you can assume that the frequency rank in frequencies matches the
frequency rank in the message. That is, the most common letter in frequencies
will be the most common letter in the message.

Hint:
string.ascii_lowercase and islower() can be handy.
"""

def dict_sorted_desc(dict):
    sorted_dict = sorted(dict.items(), key = lambda x: x[1], reverse = True)
    return sorted_dict

def decode(ciphertext, frequencies):
    # ciphertext is a string, frequencies is a dictionary with entries {letter:  float}
    clear = ''

    # write code here
    cipher_frequencies_dict = dict()

    for char in ciphertext:
        # assure that only lower case letters
        # are processed as per exercise text
        if char in ascii_lowercase:
            if char in cipher_frequencies_dict.keys():
                cipher_frequencies_dict[char] += 1
            else:
                cipher_frequencies_dict[char] = 1

    cipher_frequencies_dict_sorted = dict_sorted_desc(cipher_frequencies_dict)
    frequencies_sorted = dict_sorted_desc(frequencies)

    frequencies_list = list(map(lambda x: x[0], cipher_frequencies_dict_sorted))

    for char in ciphertext:
        try:
            clear += frequencies_sorted[frequencies_list.index(char)][0]
        except:
            clear += char

    return clear
