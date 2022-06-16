import enclib as enc
from random import randint
key_drive = input("Enter key drive: ")
activation_key = enc.pass_to_key(enc.rand_b96_str(10000), enc.rand_b96_str(10000), randint(9999, 99999))
print(f"Using activation key: {activation_key}")
key_file = enc.rand_b96_str(1048576)
print(f"Key file hash: {enc.sha512(key_file.encode()).hexdigest()}")
with open(f'{key_drive}key', 'wb') as f:
    f.write(enc.enc_from_key(key_file, activation_key))
input()