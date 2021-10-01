import zlib, base64, random

# ENC V5.5.4

# encrypt def stuff
# the manual setup version of this is found within enc 5.x versions
config_key = "c-k{jF#Rxp+l&N5BV!X&Gjj_|16|ugYZMQyKeSjyHBL=SLo;5xuspS>q_Q+KzaTm`Fx)jLBr?>~KcKocu{" \
             "b3yJtHeS$68(4G1$e;-NVb<$I78Drm7;jEGaKnN3SL-!a2;z&)3GzULRzQp@D&drGbF~0LUgO5d"
c_key = zlib.decompress(base64.b85decode(config_key)).decode('utf-8').split("🶘")
hex_head, hex_tail = c_key[0].split(" ")
hexlen_ = random.randint(int(hex_head), int(hex_tail))
alphagens = c_key[1]
key_p1_head, key_p1_tail = c_key[2].split(" ")
key_p1 = random.randint(int(key_p1_head), int(key_p1_tail))
alphalen = len(alphagens)


def generator():
    run = 0
    while True:
        run += 1
        if run % 5 == 0 or run == 1:
            hexgens = ""
            while len(hexgens) != hexlen_:
                hexgens_add = random.choice(alphagens)
                if hexgens_add not in hexgens:
                    hexgens += hexgens_add
        try:
            rand_base_alpha = ''
            while len(rand_base_alpha) != hexlen_:
                alpha_new_char = random.choice(hexgens)
                if alpha_new_char not in rand_base_alpha:
                    rand_base_alpha += alpha_new_char

            conversion_table = []
            for i in rand_base_alpha:
                conversion_table.append(i)

            decimal = key_p1
            old_decimal = key_p1
            hexadecimal = ''

            while decimal > 0:
                hexadecimal = conversion_table[decimal % hexlen_] + hexadecimal
                decimal = decimal // hexlen_

            conversion_table = {}
            cvtable_counter = 0
            for i in rand_base_alpha:
                conversion_table.__setitem__(i, cvtable_counter)
                cvtable_counter += 1

            hexadecimal = hexadecimal.strip().upper()
            decimal = 0
            power = len(hexadecimal) - 1

            for digit in hexadecimal:
                decimal += conversion_table[digit] * hexlen_ ** power
                power -= 1

            if decimal == old_decimal:
                break
        except: xx = 0

    master_key = rand_base_alpha + hexadecimal

    conversion_table = {}
    cvtable_counter = 0
    for i in master_key[:hexlen_]:
        conversion_table.__setitem__(i, cvtable_counter)
        cvtable_counter += 1

    hexadecimal = master_key[hexlen_:].strip().upper()
    num1 = 0
    power = len(hexadecimal) - 1

    for digit in hexadecimal:
        num1 += conversion_table[digit] * hexlen_ ** power
        power -= 1

    if num1 == key_p1:
        def alpha_make():
            rand_base_alpha_ = ''
            while True:
                alpha_new_char_ = random.choice(alphagens)
                if alpha_new_char_ not in rand_base_alpha_:
                    rand_base_alpha_ = rand_base_alpha_ + alpha_new_char_
                elif len(rand_base_alpha_) == alphalen:
                    break
            return rand_base_alpha_

        master_key = f"{alpha_make()}{str(hexlen_).replace('4', 'a').replace('5', 'b')}{master_key}{alpha_make()}"
        master_key = base64.b85encode(zlib.compress(master_key.encode('utf-8'), 9)).decode('utf-8')
    return master_key


def shifter_gen_loop(e_text):  # num 1
    new_num = ""
    while len(new_num) < len(e_text) * 3 + 100:
        new_num = str(new_num) + str(next(prime_numbers))
    return new_num


def fib_iter(text, num2_):  # num 2
    a = 1
    b = 1
    c = 1
    while len(str(b)) < len(text) * 3 + 100:
        total = (a + b * num2_) * c
        c = b
        b = a
        a = total
    return b


def shifter(plaintext, newnum, num, num2, alphabet, replace, forwards):
    output_enc = ""
    counter = 0
    for msg in plaintext:
        counter = counter + 2
        if msg in alphabet:
            key = int(newnum[counter:counter + 2])
            if key > alphalen:
                key = num2
            if not forwards:
                key = key * (-1)
            if key == 0:
                new_alphabet = alphabet
            elif key > 0:
                new_alphabet = alphabet[key:] + alphabet[:key]
            else:
                new_alphabet = alphabet[(alphalen + key):] + alphabet[:(alphalen + key)]
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

    if replace:
        num = str(num).replace("0", "g").replace("1", "e").replace("2", "k").replace("3", "i").replace("4", "u") \
            .replace("5", "d").replace("6", "r").replace("7", "w").replace("8", "q").replace("9", "p")
        return num + output_enc
    if not replace:
        return output_enc


def get_prime_number(candidate):
    prime_numbers_ = []
    while True:
        if candidate <= 3:
            prime_numbers_.append(candidate)
            yield candidate
        is_prime = True
        for prime_num in prime_numbers_:
            if candidate % prime_num == 0:
                is_prime = False
                break
        if is_prime:
            prime_numbers_.append(candidate)
            yield candidate
        candidate += 1


def convert(m_key):
    m_key = zlib.decompress(base64.b85decode(m_key)).decode('utf-8')
    p0_alpha = m_key[:alphalen]
    if m_key[alphalen:alphalen+1] == "a":
        hexlen = 4
    if m_key[alphalen:alphalen+1] == "b":
        hexlen = 5
    p1_key = m_key[alphalen:alphalen+1+hexlen]
    p1_e = m_key[alphalen+1+hexlen:-alphalen]
    p3_alpha = m_key[-alphalen:]

    conversion_table = {}
    cvtable_counter = 0
    for i in p1_key:
        conversion_table.__setitem__(i, cvtable_counter)
        cvtable_counter += 1

    hexadecimal = p1_e.strip().upper()
    num1 = 0
    power = len(hexadecimal) - 1

    for digit in hexadecimal:
        num1 += conversion_table[digit] * hexlen ** power
        power -= 1

    return p0_alpha, p3_alpha, num1


try:
    with open("settings/enc-key.txt", encoding="utf-8") as f:
        master_key = str(f.readlines())[2:-2]
except:
    print(f"Input an encrypt key below, leave blank to autogenerate a key")
    while True:
        master_key = input(" > ")
        if not master_key == "":
            try:
                convert(master_key)
                break
            except:
                print("key convert error")
        else:
            master_key = generator()
            break
    with open("settings/enc-key.txt", "w", encoding="utf-8") as f:
        f.write(master_key)


while True:
    try:
        with open("settings/enc-key.txt") as f:
            for line in f.readlines():
                alpha1, alpha2, num2 = convert(line)
        break
    except:
        with open("settings/enc-key.txt", "w", encoding="utf-8") as f:
            f.write(generator())

print(f"ENCRYPTION KEY:\n{master_key}\n\nSETTINGS KEY:\n{config_key}\n")


def encrypt(text):
    plaintext = base64.b85encode(zlib.compress(text.encode('utf-8'), 9)).decode('utf-8')
    global prime_numbers
    prime_numbers = get_prime_number(random.randint(100000, 800000))
    num = next(prime_numbers)

    new_num = shifter_gen_loop(plaintext)
    e_text = shifter(plaintext, new_num, num, num2, alpha1, True, True)
    content = str(e_text[:6]).replace("g", "0").replace("e", "1").replace("k", "2").replace("i", "3") \
        .replace("u", "4").replace("d", "5").replace("r", "6").replace("w", "7").replace("q", "8").replace("p", "9")

    prime_numbers = get_prime_number(int(content))
    while True:
        x = next(prime_numbers)
        if x == int(content):
            num = x
            break

    b = str(fib_iter(e_text, num2))
    return shifter(e_text, b, num, num2, alpha2, False, True)


def decrypt(e_text):
    try:
        b = str(fib_iter(e_text, num2))
        num = 0
        d_txt = shifter(e_text, b, num, num2, alpha2, False, False)
        content = str(d_txt[:6]).replace("g", "0").replace("e", "1").replace("k", "2").replace("i", "3") \
            .replace("u", "4").replace("d", "5").replace("r", "6").replace("w", "7").replace("q", "8").replace("p", "9")

        prime_numbers = get_prime_number(int(content))
        while True:
            x = next(prime_numbers)
            if x == int(content):
                num = x
                break

        newnum = ""
        run = 0
        while len(newnum) < len(d_txt) * 2 + 100:
            run += 1
            newnum = str(newnum) + str(next(prime_numbers))
            if run % 1000 == 0:
                print(run, len(d_txt), len(str(newnum)))

        output_end = shifter(d_txt[6:], newnum, num, num2, alpha1, False, False).replace(" ", "")
        return zlib.decompress(base64.b85decode(output_end)).decode('utf-8')
    except:
        print("[CND] " + e_text)
        return "[CND]"