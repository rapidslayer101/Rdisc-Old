import enclib as enc
import enclib as enc_old
from random import randint
import time

#timer = time.time()
#loop = 0
#while True:
#    loop += 1
#    seed_key = enc.pass_to_seed(enc.hex_gens(randint(5, 1000)))
#    seed_data = enc.seed_to_data(seed_key)
#    if loop % 100 == 0:
#        print(loop, time.time()-timer)

seed_key = enc.pass_to_seed("hello")
print(seed_key)


alpha1, alpha2, num2, seed3 = enc.seed_to_data(seed_key)
print(enc.encrypt("1111", alpha1, alpha2, num2, seed3))
print(enc.encrypt_key("1111", "hello"))
print(enc.decrypt_key(enc.encrypt_key("1111", "hello"), "hello"))
x = enc.encrypt(1111, alpha1, alpha2, num2, seed3)
print(x)
print(enc.encrypt(b"1111", alpha1, alpha2, num2, seed3))
print(enc.decrypt(x, alpha1, alpha2, num2, seed3))

input()
enc.encrypt_file("C:/Users/rapidslayer101/Downloads/muted.quicktime", alpha1, alpha2, num2, seed3, "enc.renc")
#enc.encrypt_file("user_agents.zip", alpha1, alpha2, num2, seed3, "user_agents.renc")
#enc.encrypt_file("C:/Users/rapidslayer101/Downloads/BetterDiscord-Windows.exe", alpha1, alpha2, num2, seed3, "muted.renc")
#enc.encrypt_file("ui.exe", alpha1, alpha2, num2, seed3, "a_file.renc")
#enc.encrypt_file("gateway.txt", alpha1, alpha2, num2, seed3, "a_file.renc")

input("Now decrypt")

print(enc.decrypt_file("enc.renc", alpha1, alpha2, num2, seed3, "file.dec"))
