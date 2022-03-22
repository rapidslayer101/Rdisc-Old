import datetime, re
from time import time
from os import path
from random import choices
from base64 import b64encode as b64enc, b64decode as b64dec
from hashlib import sha512
from zlib import compress, decompress
from multiprocessing import Pool, cpu_count
from binascii import a2b_base64, b2a_base64

# enc 10.0.3 - CREATED BY RAPIDSLAYER101 (Scott Bree)
block_size = 1000000  # modifies the chunking size
b64set = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/"
b96set = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/¬`!\"£$%^&*()- =[{]};:'@#~\\|,<.>?"


def rand_b96_string(num):
    return "".join(choices(b96set, k=int(num)))


def to_hex(base_fr, base_to, hex_to_convert):
    decimal = 0
    power = len(hex_to_convert)-1
    for digit in hex_to_convert:
        decimal += b96set.index(digit)*base_fr**power
        power -= 1
    hexadecimal = ""
    while decimal > 0:
        hexadecimal = b96set[decimal % base_to]+hexadecimal
        decimal = decimal // base_to
    return hexadecimal


def to_number(hex_to_convert):
    return "".join([str(b96set.index(x)) for x in hex_to_convert])


def get_hex_base(hex_to_check):  # this is only a guess
    for i in range(96):
        if to_hex(i+2, i+2, hex_to_check) == hex_to_check:
            return i+2


def pass_to_seed(password, salt):
    salt = sha512(sha512(salt.encode()).hexdigest().encode()).hexdigest()
    return to_hex(16, 96, sha512(sha512((salt+password).encode()).hexdigest().encode()).hexdigest())


def seed_to_alpha(seed):  # this function requires 129 numbers
    alpha_gen = b64set
    counter, alpha = [0, ""]
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


def b64pad(master_key):
    while len(master_key) % 4 != 0:
        master_key += "="
    return master_key


def shift_gen(amount, shift_num):
    shift_value = ""
    while len(shift_value) < amount:
        shift_num1 = sha512(shift_num.encode()).digest()
        shift_num = b64enc(shift_num1).decode()[:-2]
        shift_value += shift_num+b64enc(shift_num1[::-1]).decode()[:-2]
    return shift_value


def shifter(plaintext, shift_num, al, forwards):
    alx3 = [x for x in al*3]
    pln_txt = plaintext.replace("=", "")
    if forwards:
        return a2b_base64(b64pad("".join([alx3[al.index(x)+ord(y)] for x, y in zip(pln_txt, shift_num)])+"z"*8))
    else:
        return decompress(b64dec(b64pad("".join([alx3[al.index(x)-ord(y)] for x, y in zip(pln_txt, shift_num)]))))


def get_file_size(file):
    size = path.getsize(file)
    power = 2 ** 10
    n = 0
    power_labels = {0: '', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)}{power_labels[n]}"


def encrypt_block(enc, data, alpha, block_seed, send_end=None):
    shift_num = shift_gen(int(block_size*1.4), str((to_hex(96, 10, str(block_seed)))))
    if enc.lower() in ["e", "en", "enc", "encrypt"]:
        if type(data) != bytes:
            data = data.encode()
        block = shifter(b64enc(compress(data, 9)).decode(), shift_num, alpha, True)
    else:
        block = shifter(data, shift_num, alpha, False)
        try:
            block = block.decode()
        except UnicodeDecodeError:
            pass
    if send_end:
        send_end.send(block)
    else:
        return block


def block_process(blk):
    blk = b64pad(b2a_base64(blk).decode())
    return blk[:-12]+blk[-12:].replace("zzzzzzzw", "z"*8).replace("\n", "")


def encrypt(enc, text, alpha, shift_seed, salt, join_dec=None):
    if enc.lower() in ["e", "en", "enc", "encrypt", "d", "de", "dec", "decrypt"]:
        if enc.lower() in ["e", "en", "enc", "encrypt"]:
            e_chunks = [text[i:i+block_size] for i in range(0, len(text), block_size)]
        else:
            if type(text) == list:
                e_chunks = [block_process(block) for block in text]
            else:
                text = block_process(text)
                if type(text) == bytes:
                    e_chunks = text.split(b"  ")
                if type(text) == str:
                    e_chunks = text.split("  ")

        if len(e_chunks) == 1:
            shift_seed = to_hex(96, 10, str(shift_seed))
            if enc.lower() in ["e", "en", "enc", "encrypt"]:
                if type(text) != bytes:
                    text = text.encode()
                plaintext = b64enc(compress(text, 9)).decode()
                return shifter(plaintext, shift_gen(len(plaintext), shift_seed), alpha, True)
            else:
                output_end = shifter(text, shift_gen(len(text), shift_seed), alpha, False)
                try:
                    return output_end.decode()
                except UnicodeDecodeError:
                    return output_end
        else:
            print(f"Launching {len(e_chunks)} threads")
            block_seeds = []
            for i in range(len(e_chunks)+1):
                shift_seed = pass_to_seed(shift_seed, salt)
                block_seeds.append(shift_seed)
            pool = Pool(cpu_count())
            result_objects = [pool.apply_async(encrypt_block, args=(enc, e_chunks[x], alpha, block_seeds[x]))
                              for x in range(0, len(e_chunks))]
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
            file_name = file.split("/")[-1].split(".")[:-1]  # file_type = file.split("/")[-1].split(".")[-1:]
            print(f"{file_name} is {get_file_size(file)}, should take {round(path.getsize(file)/32345903.7288, 2)}s")
            alpha, shift_num = seed_to_data(pass_to_seed(key, salt))
            if enc.lower() in ["e", "en", "enc", "encrypt"]:
                with open(file, 'rb') as hash_file:
                    result_list = encrypt(enc, hash_file.read(), alpha, shift_num, salt)
                with open(file_output, "wb") as f:
                    for e_block in result_list:
                        f.write(b"  ")
                        f.write(e_block)
                print(f"ENCRYPTION COMPLETE OF {get_file_size(file)} IN {round(time()-start, 2)}s")
            else:
                with open(file, "rb") as hash_file:
                    d_data = encrypt(enc, hash_file.read().split(b"  ")[1:], alpha, shift_num, salt)
                if type(d_data[0]) == bytes:
                    with open(f"{file_output}", "wb") as f:
                        for block in d_data:
                            f.write(block)
                if type(d_data[0]) == str:
                    with open(f"{file_output}", "w", encoding="utf-8") as f:
                        for block in d_data:
                            f.write(block.replace("\r", ""))
                print(f"DECRYPTION COMPLETE OF {get_file_size(file)} IN {round(time()-start, 2)}s")
        else:
            return "File not found"
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
