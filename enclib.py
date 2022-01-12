import datetime, re
from time import time
from os import path
from random import choice
from base64 import b85encode, b64encode, b64decode
from hashlib import sha512
from zlib import compress, decompress
from multiprocessing import Pool, cpu_count
from binascii import a2b_base64, b2a_base64

# enc 9.5.0 - CREATED BY RAPIDSLAYER101 (Scott Bree)
ascii_set = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"  # base64
block_size = 2000000  # todo smart block size allocation


def hex_gens(num):
    hex_gens_ = ""
    while len(hex_gens_) != int(num):
        hex_gens_ += choice(ascii_set)
    return hex_gens_


conv_dict = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'a',
             11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f', 16: "g", 17: "h", 18: "i", 19: "j", 20: "k",
             21: "l", 22: "m", 23: "n", 24: "o", 25: "p", 26: "q", 27: "r", 28: "s", 29: "t", 30: "u",
             31: "v", 32: "w", 33: "x", 34: "y", 35: "z", 36: "A", 37: 'B', 38: 'C', 39: 'D', 40: 'E',
             41: 'F', 42: "G", 43: "H", 44: "I", 45: "J", 46: "K", 47: "L", 48: "M", 49: "N", 50: "O",
             51: "P", 52: "Q", 53: "R", 54: "S", 55: "T", 56: "U", 57: "V", 58: "W", 59: "X", 60: "Y",
             61: "Z", 62: "¬", 63: "`", 64: "!", 65: "\"", 66: "£", 67: "$", 68: "%", 69: "^", 70: "&",
             71: "*", 72: "(", 73: ")", 74: "-", 75: " ", 76: "=", 77: "+", 78: "[", 79: "{", 80: "]",
             81: "}", 82: ";", 83: ":", 84: "'", 85: "@", 86: "#", 87: "~", 88: "\\", 89: "|", 90: ",",
             91: "<", 92: ".", 93: ">", 94: "/", 95: "?"}

conv_dict_back = {v: k for k, v in conv_dict.items()}


def to_hex(base_fr, base_to, hex_to_convert):
    decimal = 0
    power = len(hex_to_convert)-1
    for digit in hex_to_convert:
        decimal += conv_dict_back[digit]*base_fr**power
        power -= 1
    hexadecimal = ""
    while decimal > 0:
        hexadecimal = conv_dict[decimal % base_to]+hexadecimal
        decimal = decimal // base_to
    return hexadecimal


def to_number(hex_to_convert):
    decimal = ""
    for digit in hex_to_convert:
        decimal += str(conv_dict_back[digit])
    return decimal


def get_hex_base(hex_to_check):  # this is only a guess
    for i in range(96):
        if to_hex(i+2, i+2, hex_to_check) == hex_to_check:
            return i+2


def pass_to_seed(password, salt):
    salt = sha512(sha512(b85encode(salt.encode())).hexdigest().encode()).hexdigest()
    inp = f"{salt[:64]}{password}{salt[64:]}"
    return to_hex(16, 96, sha512(sha512(b85encode(inp.encode())).hexdigest().encode()).hexdigest())


def seed_to_alpha(seed):  # this function requires 129 numbers
    alpha_gen = ascii_set
    counter = 0
    alpha = ""
    while len(alpha_gen) > 0:
        counter += 2
        value = int(str(seed)[counter:counter+2]) << 1
        while value > len(alpha_gen)-1:
            value = value // 2
        if len(str(seed)[counter:]) < 2:
            alpha += alpha_gen
            alpha_gen = alpha_gen.replace(alpha_gen, "")
        else:
            chosen = alpha_gen[value]
            alpha += chosen
            alpha_gen = alpha_gen.replace(chosen, "")
    return alpha


def seed_to_data(seed):
    return seed_to_alpha(int(to_hex(96, 16, seed), 36)), to_hex(10, 96, str(int(to_hex(96, 16, seed), 36)))


def b64echeck(master_key):
    while len(master_key) % 4 != 0:
        master_key += "="
    return master_key


def shifter(plaintext, shift_num, alphabet, forwards):
    alphabet2 = alphabet*3
    output_enc = ""
    counter = 0
    if forwards:
        for char in plaintext:
            counter += 2
            output_enc += alphabet2[alphabet.index(char)+int(shift_num[counter:counter+2])]
        output_enc += "zzzzzzzz"
        return a2b_base64(b64echeck(output_enc))
    else:
        for char in plaintext.replace("=", ""):
            counter += 2
            output_enc += alphabet2[alphabet.index(char)-int(shift_num[counter:counter+2])]
    return output_enc


def get_file_size(file):
    file_size_kb = path.getsize(file)/1024
    if file_size_kb > 9999:
        file_size_mb = file_size_kb/1024
        if file_size_mb > 2999:
            return f"{round(file_size_mb/1024,2)}GB"
        else:
            return f"{round(file_size_mb,2)}MB"
    else:
        return f"{round(file_size_kb,2)}KB"


def encrypt_block(enc, data, block_num, alpha, block_seed, send_end=None):
    print(f"Block {block_num} launched")
    shift_num = str(int(to_hex(96, 10, str(block_seed)), 36))
    while len(str(shift_num)) < block_size*3:
        shift_num += f"{int(str(shift_num)[-512:], 24)}"
    if enc.lower() in ["e", "en", "enc", "encrypt"]:
        if type(data) == bytes:
            block = shifter(b64encode(compress(data, 9)).decode('utf-8').replace("=", ""), str(shift_num), alpha, True)
        else:
            block = shifter(b64encode(compress(data.encode('utf-8'), 9)).decode('utf-8').replace("=", ""),
                            str(shift_num), alpha, True)
    else:
        block = decompress(b64decode(b64echeck(shifter(data, str(shift_num), alpha, False))))
        try:
            block = block.decode('utf-8')
        except UnicodeDecodeError:
            pass
    print(f"Block {block_num} complete")
    if send_end:
        send_end.send(block)
    else:
        return block


def encrypt(enc, text, alpha, shift_num, salt, join_dec=None):
    if enc.lower() in ["e", "en", "enc", "encrypt", "d", "de", "dec", "decrypt"]:
        if enc.lower() in ["e", "en", "enc", "encrypt"]:
            e_chunks = [text[i:i+block_size] for i in range(0, len(text), block_size)]
        else:
            if type(text) == list:
                e_chunks = []
                for block in text:
                    block = b64echeck(b2a_base64(block).decode("utf-8"))
                    block = block[:-12]+block[-12:].replace("zzzzzzzw", "z"*8).replace("\n", "").replace("=", "")
                    e_chunks.append(block)
            else:
                try:
                    text = b64echeck(b2a_base64(text).decode("utf-8"))
                except TypeError:
                    text = b64echeck(b2a_base64(text))
                text = text[:-16]+text[-16:].replace("zzzzzzzw", "z"*8).replace("\n", "")
                if type(text) == bytes:
                    e_chunks = text.split(b"\\BLOCK\\")
                if type(text) == str:
                    e_chunks = text.split("\\BLOCK\\")

        if len(e_chunks) == 1:
            shift_num = str(int(to_hex(96, 10, str(shift_num)), 36))
            if enc.lower() in ["e", "en", "enc", "encrypt"]:
                if type(text) == bytes:
                    plaintext = b64encode(compress(text, 9)).decode('utf-8').replace("=", "")
                else:
                    plaintext = b64encode(compress(text.encode('utf-8'), 9)).decode('utf-8').replace("=", "")
                while len(str(shift_num)) < len(plaintext) << 1:
                    shift_num += f"{int(str(shift_num)[-512:], 24)}"
                return shifter(plaintext, str(shift_num), alpha, True)
            else:
                while len(str(shift_num)) < len(text) << 1:
                    shift_num += f"{int(str(shift_num)[-512:], 24)}"
                output_end = shifter(text, str(shift_num), alpha, False)
                output_end = decompress(b64decode(b64echeck(output_end)))
                try:
                    output_end = output_end.decode('utf-8')
                except UnicodeDecodeError:
                    pass
                return output_end
        else:
            print(f"Launching {len(e_chunks)} threads")
            block_seeds = []
            for i in range(len(e_chunks)+1):
                block_seed = pass_to_seed(shift_num, salt)
                block_seeds.append(block_seed)
                shift_num = block_seed
            pool = Pool(cpu_count())
            result_objects = [pool.apply_async(encrypt_block, args=(enc, e_chunks[x-1], x, alpha, block_seeds[x-1]))
                              for x in range(1, len(e_chunks)+1)]
            pool.close()
            if join_dec:
                d_data = b""
                for x in result_objects:
                    new_data = x.get()
                    try:
                        d_data += new_data
                    except TypeError:
                        d_data = ""
                        d_data += new_data
            else:
                d_data = [x.get() for x in result_objects]
            pool.join()
            return d_data
    else:
        print("ENCRYPTION CANCELLED! Enc type not in 'e', 'en', 'enc', 'encrypt', 'd', 'de', 'dec', 'decrypt'")


def encrypt_key(text, key, salt):
    alpha, shift_num = seed_to_data(pass_to_seed(key, salt))
    return encrypt("enc", text, alpha, shift_num, salt)


def encrypt_file(enc, file, key, salt, file_output):
    start = time()
    if enc.lower() in ["e", "en", "enc", "encrypt", "d", "de", "dec", "decrypt"]:
        if path.exists(file):
            file_name, file_type = file.split("/")[-1].split(".")
            print(f"{file_name} is {get_file_size(file)}")
            alpha, shift_num = seed_to_data(pass_to_seed(key, salt))
            if enc.lower() in ["e", "en", "enc", "encrypt"]:
                with open(file, 'rb') as hash_file:
                    data_chunks = hash_file.read()
                result_list = encrypt(enc, data_chunks, alpha, shift_num, salt)
                with open(file_output, "wb") as f:
                    for e_block in result_list:
                        f.write(b"\\BLOCK\\")
                        f.write(e_block)
                print(f"ENCRYPTION COMPLETE OF {get_file_size(file)} ({block_size}*{len(result_list)})"
                      f" IN {round(time()-start, 2)}s")  # todo show new "compressed" size
            else:
                with open(file, "rb") as hash_file:
                    e_text = hash_file.read().split(b"\\BLOCK\\")
                d_data = encrypt(enc, e_text[1:], alpha, shift_num, salt)
                if type(d_data[0]) == bytes:
                    with open(f"{file_output}", "wb") as f:
                        for block in d_data:
                            f.write(block)
                if type(d_data[0]) == str:
                    with open(f"{file_output}", "w", encoding="utf-8") as f:
                        for block in d_data:
                            f.write(block.replace("\r", ""))
                print(f"DECRYPTION COMPLETE OF {get_file_size(file)} ({block_size}*{len(e_text)-1})"
                      f" IN {round(time()-start, 2)}s")  # todo show new "compressed" size
        else:
            return "File not found"  # todo smart find alternative
    else:
        print("ENCRYPTION CANCELLED! Enc type not in 'e', 'en', 'enc', 'encrypt', 'd', 'de', 'dec', 'decrypt'")


def decrypt_key(e_text, key, salt):
    alpha1, shift_num = seed_to_data(pass_to_seed(key, salt))
    return encrypt("dec", e_text, alpha1, shift_num, salt, "join_dec")


def search(data, filter_fr, filter_to):
    m = re.search(f"""{filter_fr}(.+?){filter_to}""", str(data))
    if m:
        return m.group(1)
    else:
        return None


def get_links(data):
    return ('\n'.join((re.findall(r'(https?://[^\s]+)', str(data))))) + \
           ('\n'.join((re.findall(r'(http?://[^\s]+)', str(data)))))


def round_tme(dt=None, round_to=30):
    if not dt:
        dt = datetime.datetime.now()
    seconds = (dt.replace(tzinfo=None)-dt.min).seconds
    return dt+datetime.timedelta(0, (seconds+round_to/2)//round_to*round_to-seconds, -dt.microsecond)


def hash_a_file(file):
    hash_ = sha512()
    with open(file, 'rb') as hash_file:
        buf = hash_file.read(262144)
        while len(buf) > 0:
            hash_.update(buf)
            buf = hash_file.read(262144)
    return to_hex(16, 96, hash_.hexdigest())
