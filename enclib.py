import random, os, base64, datetime, zlib, re, time
from hashlib import sha512

# enc 7.0.0
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


def pass_to_seed(password):
    if not os.path.exists("rdisc.salt"):
        print("salt file missing")
        exit()
    salt = hash_a_file("rdisc.salt")
    inp = f"{salt[:64]}{password}{salt[64:]}"
    sha = sha512(sha512(base64.b85encode(inp.encode())).hexdigest().encode()).hexdigest()
    return sha


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
    seed = int(seed, 36)
    seed2 = pass_to_seed(str(seed))
    return seed2_to_alpha(int(str(int(str(seed), 36)), 36)), seed2_to_alpha(int(str(int(str(seed2), 36)), 36)),\
        int(str(seed), 36), int(str(seed2), 36)


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


def fib_iter_log(text, num2_):
    a = int(str(num2_)[32:96])
    b = int(str(num2_)[:32])
    c = int(str(num2_)[160:])
    d = int(str(num2_)[96:160])
    total = ""
    timer = time.time()
    last_update = time.time()
    while len(str(total)) < len(text) * 3 + 100:
        total += str(int(str(a)+str(b-c).replace("-", ""))-d)
        a = str(int(str(a)[:1024])*6)+str(c//3)
        if time.time() - last_update > 0.25:
            print(f"Generating shifter {round(len(str(total))/(len(text)*3+100)*100, 2)}% {time.time()-timer}")
            last_update = time.time()
    print(f"Generating shifter 100%")
    return total


def shifter(plaintext, new_num_, num2_, alphabet, forwards):
    output_enc = ""
    counter = 0
    for msg in plaintext:
        counter += 2
        if msg in alphabet:
            key = int(new_num_[counter:counter+2])
            if key > 96:
                key = int(str(num2_)[:2])
            if not forwards:
                key = key * (-1)
            if key == 0:
                new_alphabet = alphabet
            new_alphabet = alphabet[key:]+alphabet[:key]
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


def shifter_log(plaintext, new_num_, num2_, alphabet, forwards):
    output_enc = ""
    counter = 0
    last_update = time.time()
    for msg in plaintext:
        counter += 2
        if time.time() - last_update > 0.25:
            print(f"Shifted {counter//2} {round((counter//2)/len(plaintext)*100, 2)}%")
            last_update = time.time()
        if msg in alphabet:
            key = int(new_num_[counter:counter+2])
            if key > 96:
                key = int(str(num2_)[:2])
            if not forwards:
                key = key*(-1)
            if key == 0:
                new_alphabet = alphabet
            new_alphabet = alphabet[key:]+alphabet[:key]
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
    print(f"Shifted 100%")
    return output_enc


def encrypt(text, alpha1, alpha2, num2, seed3):
    text_type = type(text)
    if text_type == int:
        text = str(text)
    if text_type == bytes:
        plaintext = base64.b85encode(zlib.compress(text, 9)).decode('utf-8')
    else:
        plaintext = base64.b85encode(zlib.compress(text.encode('utf-8'), 9)).decode('utf-8')
    new_num = seed3
    while len(str(new_num)) < len(plaintext)*3+100:  # todo revise more precise with analysed char data
        new_num = str(int(str(new_num)[:512])//2)+str(new_num)+str(int(str(new_num)[:512])*2)
    e_text = shifter(plaintext, str(new_num), num2, alpha1, True)

    b = str(fib_iter(e_text, num2))
    return shifter(e_text, b, num2, alpha2, True)


def encrypt_key(text, key):
    alpha1, alpha2, num2, seed3 = seed_to_data(pass_to_seed(key))
    return encrypt(text, alpha1, alpha2, num2, seed3)


def decrypt(e_text, alpha1, alpha2, num2, seed3):
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


def decrypt_key(e_text, key):
    alpha1, alpha2, num2, seed3 = seed_to_data(pass_to_seed(key))
    return decrypt(e_text, alpha1, alpha2, num2, seed3)


def get_file_size(file, file_name):
    file_size_kb = os.path.getsize(file)/1024
    if file_size_kb > 9999:
        file_size_mb = file_size_kb/1024
        if file_size_mb > 100:
            print("This file is not supported due to its large size, the max is 100MB")
            return "NOTSUP"
        else:
            print(f"{file_name} is {round(file_size_mb,2)}MB")
    else:
        print(f"{file_name} is {round(file_size_kb,2)}KB")


def encrypt_file(file_to_enc, alpha1, alpha2, num2, seed3, file_output=None):
    if os.path.exists(file_to_enc):
        file_name = file_to_enc.split("/")[-1]
        if get_file_size(file_to_enc, file_name) == "NOTSUP":
            return "File to large"
    else:
        return "File not found"  # todo smart find alternative
    block_size = 262144
    bytes_to_enc = f"{file_name}:FH".encode("utf-8")
    try:
        with open(file_to_enc, 'rb') as hash_file:
            buf = hash_file.read(block_size)
            read = 0
            loop = 0
            while len(buf) > 0:
                read += len(buf)
                loop += 1
                if loop % 50 == 0:
                    print(read/os.path.getsize(file_to_enc))
                bytes_to_enc += buf
                buf = hash_file.read(block_size)

        start = time.time()
        print("Compressing")
        plaintext = base64.b85encode(zlib.compress(bytes_to_enc, 9)).decode('utf-8')
        print("Compressed")
        new_num = str(seed3)
        last_update = time.time()
        timer = time.time()
        while len(str(new_num)) < len(plaintext)*3+100:
            new_num += f"{int(str(new_num)[-16384:], 36)}"
            if time.time() - last_update > 0.25:
                print(f"Generating shifter {round(len(str(new_num))/(len(plaintext)*3+100)*100, 2)}% {time.time()-timer}")
                last_update = time.time()
        print(f"Generating shifter 100%")
        for i in range(1):
            timer = time.time()
            e_text = shifter_log(plaintext, str(new_num), num2, alpha1, True)
            print(time.time()-timer)
        b = str(fib_iter_log(e_text, num2))
        e_data = shifter_log(e_text, b, num2, alpha2, True)
        print(time.time() - start)

        if file_output:
            with open(f"{file_output}", "w", encoding="utf-8") as f:
                f.write(e_data)
            return "Complete"
        else:
            return e_data
    except Exception as e:
        print("Error", e)


def decrypt_file(file_to_dec, alpha1, alpha2, num2, seed3, file_output=None):
    if os.path.exists(file_to_dec):
        file_name, file_type = file_to_dec.split("/")[-1].split(".")
        if file_type != "renc":
            return "This is not a renc file"
        else:
            get_file_size(file_to_dec, file_name)
    else:
        return "File not found"  # todo smart find alternative

    with open(file_to_dec, encoding="utf-8") as dec_file:
        e_text = dec_file.read()
    start = datetime.datetime.now()

    b = str(fib_iter_log(e_text, num2))
    d_txt = shifter_log(e_text, b, num2, alpha2, False)
    new_num = str(seed3)
    last_update = time.time()
    timer = time.time()
    while len(str(new_num)) < len(d_txt) * 3 + 100:
        new_num += f"{int(str(new_num)[-16384:], 36)}"
        if time.time() - last_update > 0.25:
            print(
                f"Generating shifter {round(len(str(new_num))/(len(d_txt)*3+100)*100, 2)}% {time.time()-timer}")
            last_update = time.time()
    print(f"Generating shifter 100%")

    output_end = shifter_log(d_txt, str(new_num), num2, alpha1, False).replace(" ", "")
    try:
        d_data = zlib.decompress(base64.b85decode(output_end)).decode('utf-8')
    except:
        d_data = zlib.decompress(base64.b85decode(output_end))

    print(type(d_data))
    print(datetime.datetime.now() - start)

    if file_output == "Original":
        file_output = file_name.decode("utf-8")

    if type(d_data) == bytes:
        file_name_data, d_data = d_data.split(b":FH")
        file_name, file_type = file_name_data.split(b".")
        with open(f"{file_output}.{file_type.decode('utf-8')}", "wb") as f:
              f.write(d_data)
    if type(d_data) == str:
        file_name_data, d_data = d_data.split(":FH")
        file_name, file_type = file_name_data.split(".")
        with open(f"{file_output}.{file_type}", "w", encoding="utf-8") as f:
            f.write(d_data.replace("\r", ""))


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
