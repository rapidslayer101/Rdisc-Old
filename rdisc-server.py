import discum, re, datetime, random, base64, zlib, os, time
from hashlib import sha512, sha256

bot = discum.Client(token="mfa.ZiR5m0U02bkR3mo_WkRdRbcVX-1zYxo1eGOdQI78"
                          "jiZFW1pHpY4M3nZUjpOgSF_aFYG43f9xtnR56wnrPdDo", log=False)

# V0.3.7.0 the first version with auto update
# V0.3.8.0 broke the first auto updater as the server system changed

# V0.3.10.0 is first version with working auto update
# V0.5.0.0 the first version with time_key and the standard_key
min_version = "V0.5.0.0"  # CHANGE MIN CLIENT REQ VERSION HERE

default_key = "HHk4itWVGs5MkTSVTKxbUel1oLqLcVOCiwdGTfY2MPBphJHZc8dseTXMmKdE"


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
    block_size_ = 65536
    hash__ = sha512()
    with open("user_agents.zip", 'rb') as hash_file_:  #todo change
        buf_ = hash_file_.read(block_size_)
        while len(buf_) > 0:
            hash__.update(buf_)
            buf_ = hash_file_.read(block_size_)
    hash_disrupt, salt = sha_to_data(hash__.hexdigest())
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


def seed_to_data(seed):
    seed_ = pass_to_seed(str(seed["SEED KEY"]))
    seed2 = str(pass_to_seed((str(seed)[32:] + str(seed)[:32])[::-1]))
    seed2_ = str(pass_to_seed(str(seed2)[::-1]))
    seed2 = seed2_ + seed2
    seed3 = int(str(seed["SEED KEY"]) + str(seed_))

    def seed2_to_alpha(seeds):
        alpha_gen = "`1234567890-=¬!\"£$%^&*()_+qwertyuiop[]QWERTYUIOP{}asdfghjkl;'#ASDFGHJKL:@~\zxcvbnm,.|ZXCVBNM<>?/"
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

    alpha1 = seed2_to_alpha(seed3)
    alpha2 = seed2_to_alpha(seed2)
    num2 = int(str(seed_) + str(seed2_))
    if num2 > 8999:
        num2 -= 2500

    return alpha1, alpha2, num2, seed3


seed_key = {}


class seed_data:
    def get(self):
        return seed_key

    def change(self, password):
        seed_key.update({"SEED KEY": pass_to_seed(password)})


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


def encrypt(text, password=None):
    if password:
        alpha1, alpha2, num2, seed3 = seed_to_data({"SEED KEY": pass_to_seed(password)})
    else:
        alpha1, alpha2, num2, seed3 = seed_to_data(seed_data.get(0))
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


def decrypt(e_text, password=None):
    if password:
        alpha1, alpha2, num2, seed3 = seed_to_data({"SEED KEY": pass_to_seed(password)})
    else:
        alpha1, alpha2, num2, seed3 = seed_to_data(seed_data.get(0))
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


def get_server_key_from_file():
    with open("server_time_key.txt", encoding="utf-8") as f:
        cur_ky_tm, old_ky = decrypt(f.read(), default_key).split("=")
    return cur_ky_tm, old_ky, old_ky


def write_server_key_to_file(sver_key_tme, sver_tme_key):
    with open("server_time_key.txt", "w", encoding="utf-8") as f:
        f.write(encrypt(f"{sver_key_tme}={sver_tme_key}", default_key))


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


def version_info(hashed, sign_up, sign_up_code=None):
    real_version = False
    with open("sha.txt", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if hashed in line:
                real_version = True
                version_data = line
    if not real_version:
        return "NOTREAL"
    else:
        latest_sha, type, version, tme, bld_num, run_num = version_data.split(" ")
        print(latest_sha, type, version, tme, bld_num, run_num)
        release_major, major, build, run = version.replace("V", "").split(".")
        req_release_major, req_major, req_build, req_run = min_version.replace("V", "").split(".")
        valid_version = False
        if int(release_major) > int(req_release_major) - 1:
            if int(major) > int(req_major) - 1:
                if int(build) > int(req_build) - 1:
                    if int(run) > int(req_run) - 1:
                        valid_version = True
                        print(f"{version} is valid for the {min_version} requirement")
        if not valid_version:
            return f"INVALID-{version}->{min_version}"
        else:
            if sign_up:
                print("AUTH SYSTEM WIP")
                print(sign_up_code)
                # if sign up key valid here
                current_key_time, current_key, old_key = get_server_key_from_file()
                print(current_key_time, current_key)
                print("valid key, time_key sending")
                return f"VALID-{version}-{tme}-{bld_num}-{run_num}+{current_key_time}={current_key}"
            else:
                time_key_hashed = sha256(get_server_key_from_file()[1].encode()).hexdigest()
                return f"VALID-{version}-{tme}-{bld_num}-{run_num}+{time_key_hashed}"


def roundTime(dt=None, round_to=30):
    if not dt:
        dt = datetime.datetime.now()
    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds + round_to / 2) // round_to * round_to
    return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)


if os.path.exists("server_time_key.txt"):
    date_format_str = '%Y-%m-%d %H:%M:%S'
    current_key_time, current_key, old_key = get_server_key_from_file()
    current_key_time = datetime.datetime.strptime(str(current_key_time), date_format_str)

    desired_time = roundTime()
    curr_tme_fmt = datetime.datetime.strptime(str(current_key_time), date_format_str)
    diff = datetime.datetime.strptime(str(desired_time), date_format_str) - curr_tme_fmt
    iterations = int(diff.total_seconds()) / 30

    if iterations > 0:
        print(f"Updating time_key from {curr_tme_fmt}-->{desired_time} via {iterations} iterations")

    loop = 0
    while current_key_time != desired_time:
        loop += 1
        current_key = pass_to_seed(str(current_key))
        current_key_time += datetime.timedelta(seconds=30)
        if loop % 20 == 0:
            print(loop, current_key_time, current_key)

    write_server_key_to_file(current_key_time, current_key)
    print("Key upto-date!")
else:
    time_key_entry = input("Time_key entry point: ")
    current_key_time = roundTime()
    print(f"Entry point: {time_key_entry}={current_key_time}")
    current_key = pass_to_seed(time_key_entry)
    current_key_time += datetime.timedelta(seconds=30)
    print(f"Entry point 2: {current_key_time}={current_key}")
    write_server_key_to_file(current_key_time, current_key)


def update_server_time_key():
    while True:
        date_format_str = '%Y-%m-%d %H:%M:%S'
        current_key_time, current_key, old_key = get_server_key_from_file()
        try:
            current_key_time = datetime.datetime.strptime(str(current_key_time), date_format_str)
            desired_time = roundTime()
            curr_tme_fmt = datetime.datetime.strptime(str(current_key_time), date_format_str)
            diff = datetime.datetime.strptime(str(desired_time), date_format_str) - curr_tme_fmt
            iterations = int(diff.total_seconds()) / 30

            if iterations > 1:
                print("CRITICAL ERROR THIS SHOULD NOT HAVE OCCURED")

            loop = 0
            while current_key_time != desired_time:
                loop += 1
                current_key = pass_to_seed(str(old_key))
                current_key_time += datetime.timedelta(seconds=30)

            if str(current_key) != str(old_key):
                print(f"{current_key_time}={current_key}")
                write_server_key_to_file(current_key_time, current_key)
        except Exception as e:
            print("error", e)
            xx = 0
        time.sleep(1)


from threading import Thread
t = Thread(target=update_server_time_key)
t.daemon = True
t.start()


@bot.gateway.command
def processing(resp):
    m = resp.event.response

    if resp.event.ready_supplemental:  # ready_supplemental is sent after ready
        user = bot.gateway.session.user
        print(f"logged in as {user['username']}#{user['discriminator']}")
        print("---")

    if resp.event.message:
        m = resp.parsed.auto()
        guildID = m['guild_id'] if 'guild_id' in m else "DM"  # because DMs are technically channels too
        channelID = m['channel_id']
        username = m['author']['username']
        discriminator = m['author']['discriminator']
        content = m['content']

        type = m['type']
        tts = m['tts']
        time_created = m['timestamp']
        try:
            reply = m['referenced_message']
        except:
            reply = "Null"
        mentions = m['mentions']
        mention_roles = m['mention_roles']
        mention_everyone = m['mention_everyone']

        id = m['id']
        embeds = m['embeds']
        attachments = m['attachments']

        if channelID == "883425805756170283":
            if username+"#"+discriminator != "HELLOTHERE#9406":
                print(m)

                seed_data.change(0, "HHk4itWVGs5MkTSVTKxbUel1oLqLcVOCiwdGTfY2MPBphJHZc8dseTXMmKdE")
                try:
                    content = decrypt(content)
                    print(content)
                    if content[138:] == "":
                        version_response = version_info(content[10:138], False)
                    else:
                        version_response = version_info(content[10:138], True, content[138:])
                    bot.sendMessage(channelID="883425805756170283", message=encrypt(version_response))
                except Exception as e:
                    print(e)

        if channelID == "883425805756170283" and username+"#"+discriminator == "HELLOTHERE#9406":
            bot.deleteMessage(channelID=f"{channelID}", messageID=f"{id}")


bot.gateway.run(auto_reconnect=True)
