import enclib as enc
from random import randint
from os import path
if not path.exists("validation_keys.txt"):
    with open("validation_keys.txt", "w", encoding="utf-8") as f:
        f.write("")
key_drive = input("Enter key drive: ")
activation_key = enc.pass_to_key(enc.rand_b96_str(10000), enc.rand_b96_str(10000), randint(9999, 99999))
print(f"Using activation key: {activation_key}")
key_file = enc.rand_b96_str(1048576)
print(f"Key file hash: {enc.sha512(key_file.encode()).hexdigest()}")
with open("validation_keys.txt", "a+", encoding="utf-8") as f:
    f.write(f"{activation_key}🱫{enc.sha512(key_file.encode()).hexdigest()}\n")
with open(f'{key_drive}key', 'wb') as f:
    f.write(enc.enc_from_key(key_file, activation_key))
print("Key file created")
