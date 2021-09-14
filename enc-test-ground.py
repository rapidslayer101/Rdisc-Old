import random, datetime, hashlib
import enc6
#import enc5, enc4#, enc3
import enc4#, enc3
#import matplotlib.pyplot as plt

text = "why hello there"
print(f"TEXT {text}")
#print("ENC3", enc3.encrypt(text))

enc4_e = enc4.shorte(text)
if enc4.shortd(enc4_e) == text:
    print("ENC4", enc4_e)
else:
    print("ENC4 FAIL")


#    enc5_e = enc5.encrypt(text)
#    if enc5.decrypt(enc5_e) == text:
#        print("ENC5", enc5_e)
#    else:
#        print("ENC5 FAIL")

enc_e = enc6.encrypt(text)
if enc6.decrypt(enc_e) == text:
    print("ENC6", enc_e )
else:
    print("ENC6 FAIL")

enc_dec = False

if enc_dec:
    block_size = 65536
    bytes = b""
    with open('C:/Users/rapidslayer101/Downloads/EI-PrimaryandSecondarySchoolNames.pdf', 'rb') as hash_file:
        buf = hash_file.read(block_size)
        while len(buf) > 0:
            bytes += buf
            buf = hash_file.read(block_size)

        start = datetime.datetime.now()
        e_data = enc6.encrypt(bytes)
        print(datetime.datetime.now() - start)

        with open(input("Encrypted File name: "), "w", encoding="utf-8") as f:
            f.write(e_data)

        print(type(e_data))
        start = datetime.datetime.now()
        data_ = enc6.decrypt(e_data)
        print(datetime.datetime.now() - start)

        print(datetime.datetime.now() - start)
        with open(input("Decrypted file name: "), "wb") as f:
            f.write(data_)


file_loop = False

if file_loop:
    while True:
        enc_dec = input("Enc or Dec: ")
        if enc_dec.lower().startswith("e"):
            file_to_encrypt = input("File to encrypt: ")
            file_output = input("Output file name: ")
            enc6.encrypt_file(file_to_encrypt, file_output)
        if enc_dec.lower().startswith("d"):
            file_to_decrypt = input("File to encrypt: ")
            file_output = input("Output file name: ")
            enc6.decrypt_file(file_to_decrypt, file_output)

        if enc_dec.lower().startswith("c"):
            block_size = 65536
            hash_ = hashlib.sha512()
            with open(input("File1: "), 'rb') as hash_file:
                buf = hash_file.read(block_size)
                while len(buf) > 0:
                    hash_.update(buf)
                    buf = hash_file.read(block_size)
            print(hash_.hexdigest())
            with open(input("File2: "), 'rb') as hash_file:
                buf = hash_file.read(block_size)
                while len(buf) > 0:
                    hash_.update(buf)
                    buf = hash_file.read(block_size)
            print(hash_.hexdigest())


alphagens = "`1234567890-=¬!\"£$%^&*()_+qwertyuiop[]QWERTYUIOP{}asdfghjkl;'#ASDFGHJKL:@~\zxcvbnm,.|ZXCVBNM<>?/"

# enc 5.5.3 does a char between 0.00003177847110 (20 mill chars measured)
# enc 6.1.0 does a char between 0.00002196053635 (20 mill chars measured)

# speed test number 1
import time, base64


def sha_to_data(sha):
    num_ = ""
    letters_ = ""
    for char in sha:
        if char in "1234567890":
            num_ += char
        else:
            letters_ += char
    return num_, letters_


def pass_to_seed(password):
    block_size = 65536
    hash_ = hashlib.sha512()
    with open('enc6.py', 'rb') as hash_file:
        buf = hash_file.read(block_size)
        while len(buf) > 0:
            hash_.update(buf)
            buf = hash_file.read(block_size)
    hash_disrupt, salt = sha_to_data(hash_.hexdigest())
    salt = salt.replace("a", "2").replace("b", "3").replace("c", "5") \
        .replace("d", "7").replace("e", "9").replace("f", "1")

    inp = str(int(hash_disrupt[::-1]) / 2) + password
    sha = hashlib.sha512(hashlib.sha512(base64.b85encode(inp.encode())).hexdigest().encode()).hexdigest()
    num, letters = sha_to_data(sha)
    sha2 = hashlib.sha512(letters.encode()).hexdigest()
    num2_, letters2 = sha_to_data(sha2)
    letters2 = letters2.replace("a", "2").replace("b", "3").replace("c", "5") \
        .replace("d", "7").replace("e", "9").replace("f", "1")

    if not len(str(int(((num + num2_[::-1])[::-1])[:128])-int(salt[:16])+int(salt[-16:]))) > 127:
        int_seed = int((num+letters2[-(128-len(str(num+num2_))):]+num2_[::-1])[::-1])-int(salt[:16])+int(salt[-16:])
    else:
        int_seed = int(((num+num2_[::-1])[::-1])[:128])-int(salt[:16])+int(salt[-16:])
    return int(int_seed)


with open("seed_key.txt", encoding="utf-8") as f:
    seed_key = ""
    for line in f.readlines():
        seed_key += line
seed = pass_to_seed(seed_key)

thing = False

if thing:
    start = time.time()
    last_update = time.time()
    value_prev = 1000000
    values = []
    values_time = []
    run = 0
    new_num = seed
    #while len(str(new_num)) < len(plaintext)*3+100:  # todo revise more precise with analysed char data
    while len(str(new_num)) < 40000000:  # todo revise more precise with analysed char data
        run += 1
        new_num = str(int(str(new_num)[:512])//2)+str(new_num)+str(int(str(new_num)[:512])*2)
        if time.time() - last_update > 0.25:
            #print(f"Generating shifter {round(len(str(new_num))/(len(plaintext)*3+100)*100, 2)}%")
            print("")
            print(f"{len(str(new_num))} {50000000}")
            value = len(str(new_num))/(time.time()-start)
            print(value)
            print(value_prev - value)
            print(value/value_prev)
            values.append(len(str(new_num)))
            values_time.append(time.time()-start)
            value_prev = value
            last_update = time.time()
        else:
            if time.time() - last_update > 0.25:
                value = len(str(new_num)) / (time.time() - start)
                value_prev = value
                last_update = time.time()

    import matplotlib.pyplot as plt
    print(values)
    print(values_time)
    plt.plot(values_time, values, label="text len")
    plt.legend()
    plt.draw()
    plt.show()

    input()

test_infinite = True

if test_infinite:
    hexlen_ = 100
    success = True
    run = 0
    start = datetime.datetime.now()
    while True:
        run += 1
        hexgens = ""
        while len(hexgens) != hexlen_:
            hexgens_add = random.choice(alphagens)
            hexgens += hexgens_add
        encrypted = enc6.encrypt(hexgens)
        if run % 1000 == 0:
            print(run*100, datetime.datetime.now()-start)
        #print(run, hexgens, encrypted)
        if not enc6.decrypt(encrypted) == hexgens:
            success = False
            print(hexgens)
            print("FALIURE", enc6.decrypt(encrypted))
            input()

input()

x = []
z = []
enc_ = []
enc5_ = []
enc4_ = []
hexlen_ = 0
while True:
    for i in range(250):
        hexgens = ""
        hexlen_ += 1
        x.append(hexlen_)
        z.append(hexlen_)
        print(hexlen_)

        #for i in range(3):  # test enc 5.5.2
        hexgens = ""
        while len(hexgens) != hexlen_:
            hexgens_add = random.choice(alphagens)
            hexgens += hexgens_add

        print(hexgens)
        encrypted = enc6.encrypt(hexgens)
        enc_.append(len(encrypted))

        encrypted = enc5.encrypt(hexgens)
        enc5_.append(len(encrypted))

        encrypted = enc4.shorte(hexgens)
        enc4_.append(len(encrypted))

        # test enc 6.0.0 here

    plt.plot(x, z, label="text len")
    plt.plot(x, enc_, label="enc6")
    plt.plot(x, enc5_, label="enc5")
    plt.plot(x, enc4_, label="enc4")
    plt.legend()
    plt.draw()
    plt.show()