import socket, os, time, re, random, base64, zlib, asyncio, datetime
from hashlib import sha512, sha256
from threading import Thread

import discord
from colorama import Fore, Back, Style, init
init()

#todo add encrypted text size output for sending messages

try:
    block_size = 65536
    hash_ = sha512()
    with open("rdisc.py", 'rb') as hash_file:
        buf = hash_file.read(block_size)
        while len(buf) > 0:
            hash_.update(buf)
            buf = hash_file.read(block_size)
    hashed = hash_.hexdigest()

    with open("sha.txt", "r", encoding="utf-8") as f:
        latest_sha, type, version, tme, bld_num, run_num = f.readlines()[-1].split(" ")
        print("prev", latest_sha, type, version, tme, bld_num, run_num)
        release_major, major, build, run = version.replace("V", "").split(".")

    if latest_sha != hashed:
        run = int(run) + 1
        with open("sha.txt", "a+", encoding="utf-8") as f:
            tme = str(datetime.datetime.now()).replace(" ", "_")
            print(f"crnt {hashed} RUN V{release_major}.{major}.{build}.{run} TME-{tme}"
                  f" BLD_NM-{bld_num[7:]} RUN_NM-{int(run_num[7:])+1}")
            f.write(f"\n{hashed} RUN V{release_major}.{major}.{build}.{run} TME-{tme}"
                    f" BLD_NM-{bld_num[7:]} RUN_NM-{int(run_num[7:])+1}")
        print(f"Running rdisc V{release_major}.{major}.{build}.{run}")
except FileNotFoundError:
    block_size = 65536
    hash_ = sha512()
    with open("rdisc.exe", 'rb') as hash_file:
        buf = hash_file.read(block_size)
        while len(buf) > 0:
            hash_.update(buf)
            buf = hash_file.read(block_size)
    hashed = hash_.hexdigest()


with open("exiter.txt", "w") as f:
    f.write("--")

if not os.path.isfile("restart.bat"):
    with open("restart.bat", "w", encoding="utf-8") as f:
        f.write("rchat.exe")


def quit_check():
    with open("exiter.txt") as f:
        force_quit_ = str(f.readlines())[2:-2]
        if force_quit_.startswith("FQ"):
            if force_quit_ == "FQ":
                return "FQ"
            if force_quit_ == "FQU":
                return "FQU"
        else:
            return "--"


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


client_sockets = set()
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", 8079))

print(" -> Launching ui.exe")
try:
    os.startfile("ui.exe")
except FileNotFoundError:
    print(Fore.YELLOW, ">> Attempting to download missing/broken file", Fore.RESET)
    from mega import Mega
    mega = Mega()
    m = mega.login("theretards909@gmail.com", "smokester1/")
    file = m.find('ui.exe')
    try:
        m.download(file)
    except PermissionError:
        print(Fore.GREEN, " << Missing file successfully downloaded", Fore.RESET)
        try:
            os.startfile("ui.exe")
        except:
            print(Fore.RED, "[!] CRITICAL ERROR. ui.exe could not be launched", Fore.RESET)
print(Fore.GREEN, "<- ui.exe launched", Fore.RESET)

print(" -> Listening for ui.exe internal socket connection")
s.listen(10)


def to_c(text):
    for client_sock in client_sockets:
        client_sock.send(text.encode(encoding="utf-16"))


def warn(text):
    to_c(f"\n🱫[COLOR THREAD][RED] [!] [{date_now()}] {text}")


def search(data, filter_fr, filter_to):
    data = str(data)
    m = re.search(f"""{filter_fr}(.+?){filter_to}""", data)
    if m:
        output = m.group(1)
    else:
        output = None
    return output


def date_now():
    return datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')


cooldown_data = {"x": (str(datetime.datetime.utcnow()))}


class cooldown():
    def check(self, msg_to_fast):
        last_msg_time = datetime.datetime.strptime(cooldown_data["x"], '%Y-%m-%d %H:%M:%S.%f')
        time_since_insertion = datetime.datetime.utcnow() - last_msg_time
        if time_since_insertion.seconds < 0.35:
            msg_to_fast += 1
        if time_since_insertion.seconds > 3:
            msg_to_fast = 0
        cooldown_data.update({"x": (str(datetime.datetime.utcnow()))})
        return msg_to_fast


client_socket, client_address = s.accept()
client_sockets.add(client_socket)
print(f" Connected to ui.exe via socket {client_address}")
to_c("\n🱫[COLOR THREAD][GREEN] <- Internal socket connected\n")


def get_links(data):
    a = (re.findall(r'(https?://[^\s]+)', str(data)))
    b = (re.findall(r'(http?://[^\s]+)', str(data)))
    c = ('\n'.join(a))
    d = ('\n'.join(b))
    e = c + d
    return e


# jump

# implemented code:
# rchat 0.7.119.14 (process build 119, rchat GUI build 14)
# enc 6.4.0

# 0.1 code rewrite and code foundations/framework
# 0.2 enc 6.4.0 implemented and seed key switching added
# 0.3 the auth server framework, sha versioning and updating
# 0.4 the client setup, server version checks, some UI elements updated
# 0.5 time_key server syncing

# 0.5 server auth and data exchange


# ports 8079
# Made by rapidslayer101
# Testers: James Judge


def roundTime(dt=None, round_to=30):
    if not dt:
        dt = datetime.datetime.now()
    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds + round_to / 2) // round_to * round_to
    return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)


def listen_for_client(cs, loop):
    asyncio.set_event_loop(loop)

    def receive():
        #allow_send = True  # todo cooldown features
        #msg_to_fast = cooldown.check(0, msg_to_fast)
        #if msg_to_fast > 10:
        #    warn(f"YOU'RE SENDING MESSAGES TOO FAST! (cooldown 3s)")
        #    allow_send = 0
        #if allow_send == 1:
        #    print(to_send)
        #    to_send = f"\n{to_send}"
        #    to_c(to_send)

        output = cs.recv(1024).decode(encoding="utf-16")
        if output.lower() == '-restart':
            os.startfile("restart.bat")

        if output.lower() == '-quit':
            with open("exiter.txt", "w") as f:
                f.write("FQ")

        return output

    if not os.path.isfile("auth.txt"):
        to_c("\n You have not yet setup this device")
        time.sleep(0.1)
        to_c("🱫[INPUT SHOW] ")
        time.sleep(0.1)
        while True:
            to_c("\n🱫[COLOR THREAD][YELLOW] Please enter a password")
            password_entry_1 = receive()
            to_c(f"\n Entered ({len(password_entry_1)}chrs): "+"*"*len(password_entry_1))
            time.sleep(0.1)
            to_c("\n🱫[COLOR THREAD][YELLOW] Please re-enter password")
            password_entry_2 = receive()
            if password_entry_1 == password_entry_2:
                break
            else:
                to_c("\n🱫[COLOR THREAD][RED] PASSWORDS DO NOT MATCH!")
        to_c("\n🱫[COLOR THREAD][GREEN] Passwords match")
        seed_data.change(0, password_entry_2)

        to_c("\n FOLLOW THE STEPS BELOW\n 1 - Click this link --> https://discord.com/developers/applications"
             "\n 2 - Click new application in the top right"
             "\n 3 - Enter 'Rdisc' as the name and click create"
             "\n 4 - Inside the settings for the rdisc app, on the left panel click bot"
             "\n 5 - Click add bot on the right and then yes"
             "\n 6 - In the bots settings turn on presence intent and server members intent"
             "\n 7 - Click the copy button under reveal token")
        time.sleep(0.1)
        while True:
            to_c("\n🱫[COLOR THREAD][YELLOW] Paste the copied token below")
            bot_token = receive()
            if len(bot_token) > 59:
                to_c("\n🱫[COLOR THREAD][RED] Token is to long (should be 59 chars)")
            if len(bot_token) < 59:
                to_c("\n🱫[COLOR THREAD][RED] Token is to short (should be 59 chars)")
            if len(bot_token) == 59:
                to_c("\n >> Testing token")
                to_c("🱫[INPUT HIDE] ")
                break

        client = discord.Client()

        @client.event
        async def on_ready():
            print('Logged in as {0.user}'.format(client))
            to_c("\n🱫[COLOR THREAD][GREEN] << Login success, Logged in as {0.user}".format(client))
            await client.close()
        try:
            client.run(bot_token)
        except discord.errors.LoginFailure:
            to_c("\n🱫[COLOR THREAD][RED] The entered token was invalid, rdisc will now restart")
            os.startfile("restart.bat")
            with open("exiter.txt", "w") as f:
                f.write("FQ")
            while True:
                input()

        with open("auth.txt", "w", encoding="utf-8") as f:
            f.write(encrypt(bot_token))

        to_c("\n 8 - Go to general information on the left panel"
             "\n 9 - Click the copy button under the application id"
             "\n 10 - Send the copied application id to Scott"
             "\n\n There is nothing more for you to do here until scott activates your token"
             "\n As your token can be found by logging into your discord account it is suggested "
             "\n that you enable 2 factor auth on your account"
             "\n\n Close rdisc once you're finished and re-open it once your token has been activated")
        while True:
            receive()
    else:
        to_c("🱫[INPUT SHOW] ")
        time.sleep(0.1)

        while True:
            with open("auth.txt", encoding="utf-8") as f:
                auth_data = f.read()
                try:
                    enc_bot_token, enc_loaded_version, enc_time_key = auth_data.split("\n")
                    time_key_present = True
                    print("3 load")
                except ValueError:
                    try:
                        enc_bot_token, enc_loaded_version = auth_data.split("\n")
                        time_key_present = False
                        print("2 load")
                    except ValueError:
                        enc_loaded_version = ""
                        enc_bot_token = auth_data
                        time_key_present = False
                        print("1 load")

            try:
                to_c("\n🱫[COLOR THREAD][YELLOW] Please enter your password")
                password = receive()
                seed_data.change(0, password)
                bot_token = decrypt(enc_bot_token)
                if enc_loaded_version != "":
                    loaded_version = decrypt(enc_loaded_version)
                    to_c(f"Loaded version is {loaded_version} (UNVERIFIED)")
                    time.sleep(0.1)

                break
            except ValueError:
                to_c("\n Incorrect password")
        to_c("\n🱫[COLOR THREAD][GREEN] Correct password")
        time.sleep(0.1)
        to_c("🱫[INPUT HIDE] ")

        client = discord.Client()
        to_c("\n >> Logging in")

        def client_login():
            if not time_key_present:
                while True:
                    to_c("🱫[INPUT SHOW] ")
                    time.sleep(0.1)
                    to_c("\n🱫[COLOR THREAD][YELLOW] Enter your sign up code")
                    sign_up_code = receive()
                    to_c(f"\n You entered: {sign_up_code}")
                    time.sleep(0.1)
                    to_c(f"\n🱫[COLOR THREAD][YELLOW] Is this correct (y/n)?")
                    choice = receive()
                    if choice.lower() == "y":
                        break
                    else:
                        to_c(f"🱫[MNINPTXT] {sign_up_code}")
                return encrypt(f"[SIGN UP] {hashed}{sign_up_code}",
                                           "HHk4itWVGs5MkTSVTKxbUel1oLqLcVOCiwdGTfY2MPBphJHZc8dseTXMmKdE")
            else:
                return encrypt(f"[SIGN UP] {hashed}",
                                           "HHk4itWVGs5MkTSVTKxbUel1oLqLcVOCiwdGTfY2MPBphJHZc8dseTXMmKdE")

        @client.event
        async def on_ready():
            to_c("\n🱫[COLOR THREAD][GREEN] << Login success, Logged in as {0.user}".format(client))
            channel = client.get_channel(883425805756170283)
            if not channel:
                to_c("\n🱫[COLOR THREAD][RED] Could not post to channel. Token not yet activated"
                     "\n Please wait for Scott to activate your token then try again (please close rdisc)")
                while True:
                    receive()
            await channel.send(client_login())

        @client.event
        async def on_message(ctx):
            if ctx.author.id == 509330868301594624:
                content = decrypt(ctx.content, "HHk4itWVGs5MkTSVTKxbUel1oLqLcVOCiwdGTfY2MPBphJHZc8dseTXMmKdE")
                print(content)
                update = False
                if content.startswith("NOTREAL"):
                    to_c("\n🱫[COLOR THREAD][RED] <> INVALID VERSION DETECTED, downloading replacements"
                         " in 5 seconds")
                    update = True
                if content.startswith("INVALID-"):
                    to_c(f"\n <> Updating rdisc {content[8:]} in 5 seconds")
                    update = True
                    with open("auth.txt", "w", encoding="utf-8") as f:
                        f.write(f"{enc_bot_token}\n{encrypt(content[8:].split('->')[0])}")

                if content.startswith("VALID-"):
                    to_c(f"\n << RESPONSE FROM AUTH RECEIVED\n << {content}")

                    to_c(f"Verified version is {content[6:].split('-')[0]} (VERIFIED)")
                    if (content[6:].split('+')[1])[10:11] == " ":
                        print("Sign up")
                        with open("auth.txt", "w", encoding="utf-8") as f:
                            f.write(f"{enc_bot_token}\n{encrypt(content[6:].split('-')[0])}"
                                    f"\n{encrypt(content[6:].split('+')[1])}")
                    else:
                        current_server_tme_key_hash = content[6:].split('+')[1]
                        current_server_tme_key_tme = roundTime()
                        try:
                            current_key_time, current_key = decrypt(enc_time_key).split("=")
                        except zlib.error:
                            to_c("\n🱫[COLOR THREAD][RED] Invalid time_key loaded.")  # todo time_key change fail_code
                            while True:
                                receive()

                        with open("auth.txt", "w", encoding="utf-8") as f:  # temp removal of the key to stop errors
                            f.write(f"{enc_bot_token}\n{enc_loaded_version}")

                        date_format_str = '%Y-%m-%d %H:%M:%S'
                        current_key_time = datetime.datetime.strptime(str(current_key_time), date_format_str)

                        curr_tme_fmt = datetime.datetime.strptime(str(current_key_time), date_format_str)
                        diff = datetime.datetime.strptime(str(current_server_tme_key_tme), date_format_str)-curr_tme_fmt
                        iterations = int(diff.total_seconds()) / 30

                        if iterations > 0:
                            to_c(f"\n Updating time_key from {curr_tme_fmt}-->{current_server_tme_key_tme}"
                                 f" via an estimated {int(iterations)} iterations")

                        start = time.time()
                        last_update = time.time()
                        loop = 0
                        while sha256(str(current_key).encode()).hexdigest() != current_server_tme_key_hash:
                            loop += 1
                            current_key = pass_to_seed(str(current_key))
                            if time.time() - last_update > 1:
                                print(loop, current_key, time.time()-start)  # todo estimate time left
                                to_c(f"\n{round((loop / iterations) * 100, 2)}% complete ({loop}/{int(iterations)}) "
                                     f"Est time left: {round((iterations-loop)/122.33,2)}s")
                                last_update = time.time()

                        with open("auth.txt", "w", encoding="utf-8") as f:
                            xxx = encrypt(f"{current_server_tme_key_tme}={current_key}")
                            f.write(f"{enc_bot_token}\n{enc_loaded_version}\n{xxx}")

                        to_c("\n🱫[COLOR THREAD][GREEN] Key upto-date!")

                    def time_key_update():
                        while True:
                            date_format_str = '%Y-%m-%d %H:%M:%S'
                            with open("auth.txt", encoding="utf-8") as f:
                                auth_data = f.read()
                                try:
                                    current_key_time, old_key = decrypt(auth_data.split("\n")[2]).split("=")
                                    current_key_time = datetime.datetime.strptime(str(current_key_time), date_format_str)
                                    desired_time = roundTime()

                                    loop = 0
                                    current_key = old_key
                                    while current_key_time != desired_time:
                                        loop += 1
                                        current_key = pass_to_seed(str(old_key))
                                        current_key_time += datetime.timedelta(seconds=30)

                                    if str(current_key) != str(old_key):
                                        with open("auth.txt", "w", encoding="utf-8") as f:
                                            print(f"{current_key_time}={current_key}")
                                            xxx = encrypt(f"{current_key_time}={current_key}")
                                            f.write(f"{enc_bot_token}\n{enc_loaded_version}\n{xxx}")
                                except Exception as e:
                                    print(e)
                            time.sleep(2)

                    t = Thread(target=time_key_update)
                    t.daemon = True
                    t.start()

                if update:
                    await client.close()
                    time.sleep(5)
                    with open("exiter.txt", "w") as f:
                        f.write("FQU")
        try:
            client.run(bot_token)
        except discord.errors.LoginFailure:
            to_c("\nToken change detected. No fail_code added")  # todo token change fail_code


loop = asyncio.new_event_loop()
t = Thread(target=listen_for_client, args=(client_socket, loop,))
t.daemon = True
t.start()


while True:
    if quit_check().startswith("FQ"):
        if quit_check() == "FQU":
            if not os.path.isfile("installer.exe"):
                from mega import Mega
                mega = Mega()
                m = mega.login("theretards909@gmail.com", "smokester1/")
                file = m.find('installer.exe')
                try:
                    m.download(file)
                except PermissionError:
                    os.startfile("installer.exe")
            else:
                os.startfile("installer.exe")
        break
    time.sleep(1)
