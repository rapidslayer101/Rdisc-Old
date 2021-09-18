import socket, os, time, zlib, asyncio, datetime
from hashlib import sha256
from threading import Thread

import aiohttp.client_exceptions
from mega import Mega

import discord
from colorama import Fore, Back, Style, init
init()

import enclib as enc

#todo add encrypted text size output for sending messages


try:
    hashed = enc.hash_a_file("rdisc.py")
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
    hashed = enc.hash_a_file("rdisc.exe")


exiter = {"QUIT": "--"}


class should_exit():
    def check(self):
        return exiter["QUIT"]

    def change(self, change_to):
        return exiter.update({"QUIT": change_to})


if not os.path.isfile("restart.bat"):
    with open("restart.bat", "w", encoding="utf-8") as f:
        f.write("rdisc.exe")


client_sockets = set()
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", 8079))

print(" -> Launching ui.exe")
try:
    os.startfile("ui.exe")
except FileNotFoundError:
    print(Fore.YELLOW, ">> Attempting to download missing/broken file", Fore.RESET)
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


def to_c(text, delay=None):
    if delay:
        time.sleep(delay)
    for client_sock in client_sockets:
        client_sock.send(str(text).encode(encoding="utf-16"))


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
to_c("\n🱫[COLOR THREAD][GREEN] <- Internal socket connected\n", 0.1)


# jump

# implemented code:
# rchat 0.7.119.14 (process build 119, rchat GUI build 14)
# enc 6.4.0

# 0.1 code rewrite and code foundations/framework
# 0.2 enc 6.4.0 implemented and seed key switching added
# 0.3 the auth server framework, sha versioning and updating
# 0.4 the client setup, server version checks, some UI elements updated
# 0.5 time_key server syncing
# 0.6 dynamic key shifting and major auth.txt storage and load rewrites
# 0.7 df_key.txt added, auth_key system, first time login, removed exiter.txt, removed git pushes of password files
# 0.8 most encryption stuff moved into enclib.py library, some login checks, some minor UI changes
# 0.9 UI overhaul part 1, some work done towards resizable forms and message processing stuff
# 0.10 server connections and basic message sending system

# 0.11 message formatting, authorisation, naming
# 0.12 authorised message posting, downloading
# 0.13 logout system and storing data


# ports localhost:8079
# Made by rapidslayer101
# Testers: James Judge

encryption_keys = {}


class keys():
    def get_key(self, key_name):
        return encryption_keys[key_name]

    def update_key(self, key_name, key):
        encryption_keys.update({key_name: key})
        print("Keys updates", encryption_keys)


if not os.path.isfile("df_key.txt"):
    to_c("\n🱫[COLOR THREAD][RED] CRITICAL FILE df_key.txt MISSING", 0.1)
    to_c("\n🱫[COLOR THREAD][YELLOW] Tell the developer that you require df_key and he will help you", 0.1)
    while True:
        input()
keys.update_key(0, "default_key", enc.hash_a_file("df_key.txt"))


def df_encrypt(text):
    return enc.encrypt(text, keys.get_key(0, "default_key"))


def df_decrypt(enc_text):
    return enc.decrypt(enc_text, keys.get_key(0, "default_key"))


def pa_encrypt(text):
    return enc.encrypt(text, keys.get_key(0, "pass_key"))


def pa_decrypt(enc_text):
    return enc.decrypt(enc_text, keys.get_key(0, "pass_key"))


def tk_encrypt(text):
    print(keys.get_key(0, "time_key").split("=")[1])
    return enc.encrypt(text, keys.get_key(0, "time_key").split("=")[1])


def tk_decrypt(enc_text):
    return enc.decrypt(enc_text, keys.get_key(0, "time_key").split("=")[1])


def auth_txt_write(token=None, version_data=None, time_key=None, auth_token=None):
    auth_to_write = ""
    if token:
        auth_to_write += pa_encrypt(df_encrypt(token))
    if version_data:
        auth_to_write += "\n"+df_encrypt(version_data)
    if time_key:
        auth_to_write += "\n"+df_encrypt(pa_encrypt(time_key))
    if auth_token:
        auth_to_write += "\n"+pa_encrypt(df_encrypt(auth_token))
    with open("auth.txt", "w", encoding="utf-8") as f:
        f.write(auth_to_write)


if not os.path.isfile("auth.txt"):
    load = 0
else:
    with open("auth.txt", encoding="utf-8") as f:
        auth_data = f.read().split("\n")
        if len(auth_data) > 0:
            if auth_data[0] == "":
                load = 0
            else:
                enc_bot_token = auth_data[0]
                load = 1
        if len(auth_data) > 1:
            unverified_version = df_decrypt(auth_data[1])
            to_c(f"Loaded version is {unverified_version} (UNVERIFIED)")
            load = 2
        if len(auth_data) > 2:
            enc_time_key = auth_data[2]
            enc_auth_token = auth_data[3]
            load = 4


print(f"loaded {load} auth values")


launch_client = {"LAUNCH": "FALSE"}


class launch_client_state():
    def get(self):
        return launch_client["LAUNCH"]

    def change(self, to):
        launch_client.update({"LAUNCH": to})


def listen_for_cleint(cs, loop):
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
            should_exit.change(0, "FQ")

        return output

    print("now in client loop")
    client = discord.Client()
    to_c("\n >> Logging in", 0.1)

    @client.event
    async def on_ready():
        to_c("🱫[INPUT SHOW]\n🱫[COLOR THREAD][GREEN] << You are now logged in and can post messages", 0.1)
        while True:
            recieved = receive()
            recieved = tk_encrypt(recieved)  # TODO MAKE THIS DF_KEY AS WELL
            channel = client.get_channel(883425805756170283)
            await channel.send(recieved)

    client.run("ODgzODI4MjAyNjE3ODMxNDI2.YTPnKA.Y8YA8NrohVie7hFJaaeZ42e3CT8")


def listen_for_server(cs, loop):
    asyncio.set_event_loop(loop)

    def receive():
        output = cs.recv(1024).decode(encoding="utf-16")
        if output.lower() == '-restart':
            os.startfile("restart.bat")

        if output.lower() == '-quit':
            should_exit.change(0, "FQ")

        return output

    if load == 0:
        to_c("\n You have not yet setup this device")
        to_c("🱫[INPUT SHOW]🱫[MNINPLEN][256] ", 0.1)
        while True:
            to_c("\n🱫[COLOR THREAD][YELLOW] Please enter a password", 0.1)
            password_entry_1 = receive()
            to_c(f"\n Entered ({len(password_entry_1)}chrs): "+"*"*len(password_entry_1))
            to_c("\n🱫[COLOR THREAD][YELLOW] Please re-enter password", 0.1)
            password_entry_2 = receive()
            if password_entry_1 == password_entry_2:
                break
            else:
                to_c("\n🱫[COLOR THREAD][RED] PASSWORDS DO NOT MATCH!")
        to_c("\n🱫[COLOR THREAD][GREEN] Passwords match")
        keys.update_key(0, "pass_key", password_entry_2)

        to_c("\n FOLLOW THE STEPS BELOW\n 1 - Click this link --> https://discord.com/developers/applications"
             "\n 2 - Click new application in the top right"
             "\n 3 - Enter 'Rdisc' as the name and click create"
             "\n 4 - Inside the settings for the rdisc app, on the left panel click bot"
             "\n 5 - Click add bot on the right and then yes"
             "\n 6 - In the bots settings turn on presence intent and server members intent"
             "\n 7 - Click the copy button under reveal token")
        while True:
            to_c("🱫[MNINPLEN][59] ", 0.1)
            to_c("\n🱫[COLOR THREAD][YELLOW] Paste the copied token below", 0.1)
            bot_token = receive()
            if len(bot_token) < 59:
                to_c("\n🱫[COLOR THREAD][RED] Token is to short (should be 59 chars)")
            if len(bot_token) == 59:
                to_c("🱫[INPUT HIDE]\n >> Testing token")
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
            should_exit.change(0, "FQ")
            while True:
                input()

        auth_txt_write(bot_token)
        to_c("\n 8 - Go to general information on the left panel"
             "\n 9 - Click the copy button under the application id"
             "\n 10 - Send the copied application id to Scott"
             "\n\n There is nothing more for you to do here until Scott activates your token"
             "\n As your token can be found by logging into your discord account it is suggested "
             "\n that you enable 2 factor auth on your account"
             "\n\n Close rdisc once you're finished and re-open it once your token has been activated")
        while True:
            receive()
    else:
        to_c("🱫[INPUT SHOW]🱫[MNINPLEN][256] ", 0.1)
        while True:
            try:
                to_c("\n🱫[COLOR THREAD][YELLOW] Please enter your password", 0.1)
                password = receive()
                keys.update_key(0, "pass_key", password)
                bot_token = df_decrypt(pa_decrypt(enc_bot_token))
                break
            except ValueError:
                to_c("\n Incorrect password")
        to_c("\n🱫[COLOR THREAD][GREEN] Correct password", 0.1)

        if load == 4:
            keys.update_key(0, "AUTH_TOKEN", df_decrypt(pa_decrypt(enc_auth_token)))

        client = discord.Client()
        to_c("🱫[INPUT HIDE]\n >> Logging in")

        def client_login():
            if not load == 4:
                to_c("🱫[INPUT SHOW]🱫[MNINPLEN][64] ")
                while True:
                    to_c("\n🱫[COLOR THREAD][YELLOW] Enter what you would like to be called?", 0.1)
                    name_be_called = receive()
                    to_c(f"\n You entered: {name_be_called}")
                    to_c(f"\n🱫[COLOR THREAD][YELLOW] Is this correct (y/n)?", 0.1)
                    choice = receive()
                    if choice.lower() in ["yes", "y"]:
                        break
                    else:
                        to_c(f"🱫[MNINPTXT] {name_be_called}")
                return df_encrypt(f"[LOGIN] {hashed}{name_be_called}")
            else:
                return df_encrypt(f"[LOGIN] {hashed}")

        to_c("🱫[MNINPLEN][4000] ")

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
            if ctx.author.id in [509330868301594624, 425373518566260766]:
                content = df_decrypt(ctx.content)  # todo time_key decrypt
                try:
                    content = tk_decrypt(content)
                    to_c(f"\n{content}", 0.1)
                    print(content)
                except:
                    print(content)
                    if content.startswith("NOTREAL"):
                        to_c("\n🱫[COLOR THREAD][RED] <> INVALID VERSION DETECTED, downloading replacements"
                             " in 5 seconds")
                        await client.close()
                        time.sleep(5)
                        should_exit.change(0, "FQU")
                    if content.startswith("INVALID-"):
                        to_c(f"\n <> Updating rdisc {content[8:]} in 5 seconds")
                        await client.close()
                        time.sleep(5)
                        should_exit.change(0, "FQU")
                        auth_txt_write(bot_token, content[8:].split('->')[0])

                    if content.startswith("ACC_ALR_EXT"):
                        to_c("\n🱫[COLOR THREAD][RED] THIS ACCOUNT ALREADY EXISTS. Ask developer for support")

                    if content.startswith("ACC_CRT_NTA"):
                        to_c("\n🱫[COLOR THREAD][RED] ACCOUNT CREATION NOT ALLOWED. Ask developer for support")

                    if content.startswith("NO_ACC_FND"):
                        to_c("\n🱫[COLOR THREAD][RED] YOU DO NOT HAVE AN ACCOUNT. Ask developer for support")

                    if content.startswith("VALID-"):
                        verified_version = content[6:].split('-')[0]
                        to_c(f"\n << RESPONSE FROM AUTH RECEIVED\n << {verified_version}")
                        to_c(f"Verified version is {verified_version} (VERIFIED)")
                        if (content[6:].split('Ō')[1])[10:11] == " ":
                            time_key, auth_token = content[6:].split('Ō')[1].split("Ǘ")
                            if "NO TIME KEY" in time_key:
                                to_c("\n🱫[COLOR THREAD][RED] NO TIME KEY RECEIVED. Please restart rdisc and retry", 0.1)
                                while True:
                                    receive()
                            auth_txt_write(bot_token, content[6:].split('-')[0], time_key, auth_token)
                            keys.update_key(0, "time_key", time_key)
                        else:
                            current_server_tme_key_hash = content[6:].split('Ō')[1]
                            current_server_tme_key_tme = enc.round_tme()
                            try:
                                current_kt, current_key = pa_decrypt(df_decrypt(enc_time_key)).split("=")
                            except zlib.error:
                                to_c("\n🱫[COLOR THREAD][RED] Invalid time_key loaded.")  # todo time_key change fail_code
                                while True:
                                    receive()

                            date_format_str = '%Y-%m-%d %H:%M:%S'
                            current_kt = datetime.datetime.strptime(str(current_kt), date_format_str)
                            curr_tme_fmt = datetime.datetime.strptime(str(current_kt), date_format_str)
                            diff = datetime.datetime.strptime(str(current_server_tme_key_tme), date_format_str)-curr_tme_fmt
                            iterations = int(diff.total_seconds()) / 30

                            if iterations > 0:
                                to_c(f"\n Updating time_key from {curr_tme_fmt}-->{current_server_tme_key_tme}"
                                     f" via an estimated {int(iterations)} iterations")

                            last_update = time.time()
                            tk_loop = 0
                            while sha256(str(current_key).encode()).hexdigest() != current_server_tme_key_hash:
                                tk_loop += 1
                                current_key = enc.pass_to_seed(str(current_key))
                                curr_tme_fmt += datetime.timedelta(seconds=30)
                                try:
                                    if time.time() - last_update > 0.1:
                                        to_c(f"🱫[TMKYT]{str(curr_tme_fmt).split(' ')[1]}"
                                             f"\n{round((iterations-tk_loop)/122.33,2)}s")
                                        last_update = time.time()
                                except ZeroDivisionError:
                                    print("Division error in key_update on load")
                            auth_txt_write(bot_token, verified_version,
                                           f"{current_server_tme_key_tme}={current_key}", keys.get_key(0, "AUTH_TOKEN"))

                            keys.update_key(0, "time_key", f"{current_server_tme_key_tme}={current_key}")
                            to_c(f"🱫[TMKYT]{str(current_server_tme_key_tme).split(' ')[1]}", 0.1)
                            to_c("\n🱫[COLOR THREAD][GREEN] Key upto-date!")

                        def time_key_update():
                            while True:
                                try:
                                    current_kt, old_key = keys.get_key(0, "time_key").split("=")
                                    current_kt = datetime.datetime.strptime(str(current_kt), '%Y-%m-%d %H:%M:%S')

                                    current_key = old_key
                                    while current_kt != enc.round_tme():
                                        current_key = enc.pass_to_seed(str(old_key))
                                        current_kt += datetime.timedelta(seconds=30)

                                    if str(current_key) != str(old_key):
                                        to_c(f"🱫[TMKYT]{str(current_kt).split(' ')[1]}")
                                        auth_txt_write(bot_token, verified_version,
                                                       f"{current_kt}={current_key}", keys.get_key(0, "AUTH_TOKEN"))
                                        keys.update_key(0, "time_key", f"{current_kt}={current_key}")
                                except Exception as e:
                                    print(e)
                                time.sleep(2)

                        t = Thread(target=time_key_update)
                        t.daemon = True
                        t.start()
                        launch_client_state.change(0, "TRUE")
        try:
            client.run(bot_token)
        except discord.errors.LoginFailure:
            to_c("\nToken change detected. No fail_code added")  # todo token change fail_code
        except aiohttp.client_exceptions.ClientConnectorError:
            to_c("\n🱫[COLOR THREAD][RED] Internet connection not found, please reconnect and try again")


loop = asyncio.new_event_loop()
t = Thread(target=listen_for_server, args=(client_socket, loop,))
t.daemon = True
t.start()


while True:
    if launch_client_state.get(0) == "TRUE":
        launch_client_state.change(0, "FALSE")
        loop = asyncio.new_event_loop()
        t = Thread(target=listen_for_cleint, args=(client_socket, loop,))
        t.daemon = True
        t.start()

    if should_exit.check(0).startswith("FQ"):
        if should_exit.check(0) == "FQU":
            if not os.path.isfile("installer.exe"):
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
