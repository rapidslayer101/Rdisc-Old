import zlib, base64, random, hashlib, os, datetime, time

# ENC V6.4.0

# todo, logging system with % and optional
# todo, check and optimise the 2 new_nums/b
# todo, further improve file support


def hex_gens(num):
    hex_gens_ = ""
    while len(hex_gens_) != num:
        alphagens = "`1234567890-=¬!\"£$%^&*()_+qwertyuiop[]QWERTYUIOP{}asdfghjkl;'#ASDFGHJKL:@~\zxcvbnm,.|ZXCVBNM<>?/"
        hex_gens_add = random.choice(alphagens)
        hex_gens_ += hex_gens_add
    return hex_gens_


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


if not os.path.isfile("seed_key.txt"):
    open("seed_key.txt", "w").close()
with open("seed_key.txt", encoding="utf-8") as f:
    seed_key = ""
    for line in f.readlines():
        seed_key += line

if seed_key == "":
    seed_key = input("Enter seed_key or leave blank: ")
    if seed_key == "":
        seed_key = hex_gens(128)
    with open("seed_key.txt", "w", encoding="utf-8") as f:
        f.write(seed_key)

seed = pass_to_seed(seed_key)
seed_ = pass_to_seed(str(seed))
seed2 = str(pass_to_seed((str(seed)[32:]+str(seed)[:32])[::-1]))
seed2_ = str(pass_to_seed(str(seed2)[::-1]))
seed2 = seed2_ + seed2
seed = int(str(seed)+str(seed_))


def seed2_to_alpha(seeds):
    alphagens = "`1234567890-=¬!\"£$%^&*()_+qwertyuiop[]QWERTYUIOP{}asdfghjkl;'#ASDFGHJKL:@~\zxcvbnm,.|ZXCVBNM<>?/"
    counter = 0
    alpha = ""
    while len(alphagens) > 1:
        counter += 3
        value = int(str(seeds)[counter:counter+1]) + int(str(seeds)[counter:counter+1])
        while value > len(alphagens)-1:
            value = value // 2
        if len(str(seeds)[counter:]) < 2:
            alpha += alphagens
            alphagens = alphagens.replace(alphagens, "")
        else:
            choosen = alphagens[value]
            alpha += choosen
            alphagens = alphagens.replace(choosen, "")
    return alpha


alpha1 = seed2_to_alpha(seed)
alpha2 = seed2_to_alpha(seed2)
num2 = int(str(seed_)+str(seed2_))
if num2 > 8999:
    num2 -= 2500

print(f"\nSEED KEY:\n{seed_key}\n")


def fib_iter(text, num2_):
    a = int(str(num2_)[32:96])
    b = int(str(num2_)[:32])
    c = int(str(num2_)[160:])
    d = int(str(num2_)[96:160])
    total = ""
    last_update = time.time()
    while len(str(total)) < len(text) * 3 + 100:
        total += str(int(str(a)+str(b-c).replace("-", ""))-d)
        a = str(int(str(a)[:1024])*6)+str(c//3)
        if time.time() - last_update > 0.25:
            print(f"Generating shifter {round(len(str(total))/(len(text)*3+100)*100, 2)}%")
            last_update = time.time()
    print(f"Generating shifter 100%")
    return total


def shifter(plaintext, new_num_, num2_, alphabet, forwards):
    output_enc = ""
    counter = 0
    last_update = time.time()
    for msg in plaintext:
        counter = counter + 2
        if time.time() - last_update > 0.25:
            print(f"Shifting {round((counter//2)/len(plaintext)*100, 2)}%")
            last_update = time.time()
        if msg in alphabet:
            key = int(new_num_[counter:counter + 2])
            if key > 96:
                key = int(str(num2_)[:2])
            if not forwards:
                key = key * (-1)
            if key == 0:
                new_alphabet = alphabet
            new_alphabet = alphabet[key:] + alphabet[:key]
            encrypted = ""
            for message_index in range(0, len(msg)):
                if msg[message_index] == " ":
                    encrypted += " "
                for alphabet_index in range(0, len(new_alphabet)):
                    if msg[message_index] == alphabet[alphabet_index]:
                        encrypted += new_alphabet[alphabet_index]
            output_enc += encrypted
        else:
            output_enc += msg
    print(f"Shifting 100%")
    return output_enc


def encrypt(text):
    print("Compressing")
    if type(text) == str or int:
        plaintext = base64.b85encode(zlib.compress(str(text).encode('utf-8'), 9)).decode('utf-8')
    if type(text) == bytes:
        plaintext = base64.b85encode(zlib.compress(text, 9)).decode('utf-8')
    new_num = seed
    last_update = time.time()
    while len(str(new_num)) < len(plaintext)*3+100:  # todo revise more precise with analysed char data
        new_num = str(int(str(new_num)[:512])//2)+str(new_num)+str(int(str(new_num)[:512])*2)
        if time.time() - last_update > 0.25:
            print(f"Generating shifter {round(len(str(new_num))/(len(plaintext)*3+100)*100, 2)}%")
            last_update = time.time()
    print(f"Generating shifter 100%")
    e_text = shifter(plaintext, str(new_num), num2, alpha1, True)
    b = str(fib_iter(e_text, num2))
    return shifter(e_text, b, num2, alpha2, True)


def decrypt(e_text):
    try:
        b = str(fib_iter(e_text, num2))
        d_txt = shifter(e_text, b, num2, alpha2, False)
        new_num = seed
        last_update = time.time()
        while len(str(new_num)) < len(d_txt)*3+100:  # todo revise more precise with analysed char data
            new_num = str(int(str(new_num)[:512])//2)+str(new_num)+str(int(str(new_num)[:512])*2)
            if time.time() - last_update > 0.25:
                print(f"Generating shifter {round(len(str(new_num))/(len(d_txt)*3+100)*100, 2)}%")
                last_update = time.time()
        print(f"Generating shifter {round(len(str(new_num))/(len(d_txt)*3+100)*100, 2)}%")
        output_end = shifter(d_txt, str(new_num), num2, alpha1, False).replace(" ", "")
        print("Decompressing")
        try:
            output_end = zlib.decompress(base64.b85decode(output_end)).decode('utf-8')
        except:
            output_end = zlib.decompress(base64.b85decode(output_end))
        return output_end
    except Exception as e:
        return "[CND]" + e


def encrypt_file(file_to_enc, file_output):
    block_size = 65536
    bytes = b""
    try:
        with open(file_to_enc, 'rb') as hash_file:
            buf = hash_file.read(block_size)
            while len(buf) > 0:
                bytes += buf
                buf = hash_file.read(block_size)

        start = datetime.datetime.now()
        e_data = encrypt(bytes)
        print(datetime.datetime.now() - start)

        with open(f"enc/{file_output}", "w", encoding="utf-8") as f:
            f.write(e_data)
    except:
        print("Error")


def decrypt_file(file_to_dec, file_output):
    data = ""
    with open(file_to_dec, encoding="utf-8") as dec_file:
        for line_ in dec_file.readlines():
            data += line_
    start = datetime.datetime.now()
    d_data = decrypt(data)
    print(datetime.datetime.now() - start)
    print(type(d_data))
    if type(d_data) == str:
        print("Str file")
        with open(f"enc/{file_output}", "w", encoding="utf-8") as f:
            print(d_data)
            f.write(d_data.replace("\r", ""))
    else:
        if type(d_data) == bytes:
            print("Byte file")
            with open(f"enc/{file_output}", "wb") as f:
                f.write(d_data)
        else:
            print("?? file")
            with open(f"enc/{file_output}", "wb") as f:
                f.write(d_data)
