import sys
import hashlib
import base64

"""
In this exercise you are given a hash and a list of candidate passwords, 
and your task is to write a password guesser that finds the password in
the candidates that was used to generate the hash.

The hash follows a common format used for storing hashed password

    procotol$salt$hash

Here, the protocol will always be set to 42, so you can ignore it. For
hashing we will use SHA-384. In this exercise, the hash is constructed
by hashing a message containing the salt followed by the actual password.
In practice, the combination of salt and the password is significantly
more convoluted.

The salt and the password hash are both base64 encoded in the hash string,
and need to be decoded.

Hints:
- You will find hashlib and base64 libraries useful.
- The hash and the candidates are all text strings but the above libraries
  operate with byte arrays. Use encode('utf-8') to get a byte array from a
  text string.
"""

def base64_to_utf8(string):
    string_utf8 = base64.b64decode(string.encode('utf8')).decode('utf8')
    return string_utf8

def utf8_to_base64(string):
    string_b64 = base64.b64encode(string)
    return string_b64

def string_to_bytes(string):
    byte_array = string.encode('utf-8')
    return byte_array

def bytes_to_string(bytes):
    string = bytes.decode('utf-8')
    return string

def bytes_to_hash(bytes):
    hash_function = hashlib.sha384()
    hash_function.update(bytes)
    hashed_bytes = hash_function.digest()
    return hashed_bytes

def test_password(passhash, candidates):
    protocol, salt_b64, password_hash = passhash.split('$')

    for password_candidate in candidates:
        salt_utf8 = base64_to_utf8(salt_b64)
        hash_candidate = salt_utf8 + password_candidate
        hash_candidate_bytes = string_to_bytes(hash_candidate)
        candidate_bytes_hash = bytes_to_hash(hash_candidate_bytes)
        candidate_hash_base64 = utf8_to_base64(candidate_bytes_hash)
        candidate_hash = bytes_to_string(candidate_hash_base64)

        if password_hash == candidate_hash:
            return password_candidate

def main(argv):
	passhash = argv[1]
	print('Given hash:', passhash)
	fname = argv[2]
	candidates = [p.strip() for p in open(fname)]
	print(test_password(passhash, candidates))


# This makes sure the main function is not called immediatedly
# when TMC imports this module
if __name__ == "__main__": 
	if len(sys.argv) != 3:
		print('usage: python %s hash filename' % sys.argv[0])
	else:
		main(sys.argv)
