import socket, os, time, datetime, rsa, uuid
from threading import Thread
import enclib as enc


try:
    hashed = enc.hash_a_file("rdisc.py")
    with open("sha.txt", "r", encoding="utf-8") as f:
        latest_sha, run_type, version, tme, bld_num, run_num = f.readlines()[-1].split("§")
    print("prev", run_type, version, tme, bld_num, run_num)
    release_major, major, build, run = version.replace("V", "").split(".")

    if latest_sha != hashed:
        run = int(run) + 1
        with open("sha.txt", "a+", encoding="utf-8") as f:
            write = f"\n{hashed}§RUN§V{release_major}.{major}.{build}.{run}" \
                    f"§TME-{str(datetime.datetime.now())[:-4].replace(' ', '_')}" \
                    f"§BLD_NM-{bld_num[7:]}§RUN_NM-{int(run_num[7:])+1}"
            print(f"crnt RUN V{release_major}.{major}.{build}.{run} "
                  f"TME-{str(datetime.datetime.now())[:-4].replace(' ', '_')} "
                  f"BLD_NM-{bld_num[7:]} RUN_NM-{int(run_num[7:])+1}")
            f.write(write)
        print(f"Running rdisc V{release_major}.{major}.{build}.{run}")
except FileNotFoundError:
    hashed = enc.hash_a_file("rdisc.exe")


exit_state = {"QUIT": "--"}


class should_exit:
    def check(self):
        return exit_state["QUIT"]

    def change(self, change_to):
        return exit_state.update({"QUIT": change_to})


s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if os.path.exists("rdisc.py"):
    s.bind(("127.0.0.1", 8078))
else:
    s.bind(("127.0.0.1", 8079))

print(" -> Launching ui.exe")
if not os.path.isfile("ui.exe"):
    print("[!] CRITICAL FILE ui.exe MISSING")
else:
    os.startfile("ui.exe")
print(" <- ui.exe launched")
s.listen(10)

cs, client_address = s.accept()


def to_c(text, delay=None):
    if delay:
        time.sleep(delay)
    cs.send(str(text).encode(encoding="utf-16"))


print(f" Connected to ui.exe via socket {client_address}")
to_c("\n🱫[COLOR THREAD][GREEN] <- Internal socket connected\n", 0.1)


# 0.1 code rewrite and code foundations/framework from rchat 0.7.119.14 (process build 119, rchat GUI build 14)
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
# 0.12 message post fixes, cooldown + changes. ui.exe now usable as launcher, restart.bat removed
# 0.13 upgrade to enc 7.0.0, massive rewrite to sockets instead of discord slight login changes (half complete)
# 0.14 first functioning socket version
# 0.15 file cleanup and load changes, code cleanup, names, multi-user support (so actually functional)
# 0.16 socket close improvements, name changes, fixed restarts, password changes, len checks
# 0.17 rdisc-rc3 rewrites, enc 9.5.0 implemented, changed mostly from str to bytes, removal of entire time_key system
# 0.18 s<->c connect RSA falls back to enc 10.0.1 (implemented), signup complete (apart from key saving to auth)
# 0.19 saving keys, logging back in via dk and sk

# 0.20 fall back method if sk/ip wrong -> dk, if no dk -> email and pass

# 0.21 basic chat functionality, client to client connections and keys
# 0.22 downloading, saving, load req files from a first time setup file, on setup know what version is installed
# 0.23 logout system and storing data


# ports localhost:8079, localhost:8080
# Made by rapidslayer101 (Scott Bree), Main tester: James Judge

encryption_keys = {}


class keys:
    def get_key(self, key_name):
        return encryption_keys[key_name]

    def update_key(self, key_name, key):
        encryption_keys.update({key_name: key})


default_salt = """52gy"J$&)6%0}fgYfm/%ino}PbJk$w<5~j'|+R .bJcSZ.H&3z'A:gip/jtW$6A=
                  G-;|&&rR81!BTElChN|+"TCM'CNJ+ws@ZQ~7[:¬`-OC8)JCTtI¬k<i#."H4tq)p4"""
keys.update_key(0, "mac", enc.pass_to_seed(hex(uuid.getnode()), default_salt))


def mac_encrypt_key(text):
    return enc.encrypt_key(text, keys.get_key(0, "mac"), "salt")


def mac_decrypt_key(enc_text):
    return enc.decrypt_key(enc_text, keys.get_key(0, "mac"), "salt")


def at_encrypt_key(text):
    return enc.encrypt_key(text, keys.get_key(0, "session_key")[64:], "salt")


def at_decrypt_key(enc_text):
    return enc.decrypt_key(enc_text, keys.get_key(0, "session_key")[64:], "salt")


def auth_txt_write(dk, sk=None):
    auth_to_write = b""
    if dk:
        auth_to_write += mac_encrypt_key(dk)
    if sk:
        auth_to_write += b"  "+mac_encrypt_key(sk)
    with open("auth.txt", "wb") as auth_txt:
        auth_txt.write(auth_to_write)


cool_down_data = {"x": (str(datetime.datetime.utcnow())), "msg_counter": 0}


class cooldown:
    def check(self):
        last_msg_time = datetime.datetime.strptime(cool_down_data["x"], '%Y-%m-%d %H:%M:%S.%f')
        time_since_last = datetime.datetime.utcnow() - last_msg_time
        if time_since_last.seconds < 1:  # time between messages before counter adds 1
            cool_down_data.update({"msg_counter": cool_down_data["msg_counter"]+1})
        if time_since_last.seconds > 5:  # cooldown(s) when triggered
            cool_down_data.update({"msg_counter": 0})

        if cool_down_data["msg_counter"] > 10:  # total before counter triggers cooldown(s)
            return round(5-time_since_last.seconds, 2)
        else:
            cool_down_data.update({"x": (str(datetime.datetime.utcnow()))})
            return "True"


def receive():
    output = cs.recv(1024).decode(encoding="utf-16")
    if output.lower() == '-restart':
        should_exit.change(0, "FQR")

    if output.lower() == '-quit':
        should_exit.change(0, "FQ")
    return output


# initiate server connection
pub_key, pri_key = rsa.newkeys(1024)

server_host = "26.29.111.99"
server_port = 8080
s = socket.socket()
try:
    s.connect((server_host, server_port))
    to_c("\n🱫[COLOR THREAD][GREEN] Connected to server")
except ConnectionRefusedError:
    to_c("\n🱫[COLOR THREAD][RED] Could not connect to server")
    input()
print("Server connected ->", s)

# server bootstrap
s.send(rsa.PublicKey.save_pkcs1(pub_key))
print(" >> Public RSA key sent")
enc_seed = rsa.decrypt(s.recv(1024), pri_key).decode()
enc_salt = rsa.decrypt(s.recv(1024), pri_key).decode()
alpha, shift_seed = enc.seed_to_data(enc_seed)
print(" << Client enc_seed and enc_salt received and loaded")
to_c("\n🱫[COLOR THREAD][GREEN] RSA -> enc bootstrap complete")


def send_e(text):
    s.send(enc.encrypt("e", text, alpha, shift_seed, enc_salt))


def send_d():
    return enc.encrypt("d", s.recv(1024), alpha, shift_seed, enc_salt)


while True:  # login loop
    device_key = False
    session_key = False

    if os.path.isfile("auth.txt"):
        with open("auth.txt", "rb") as f:
            auth_data = f.read().split(b"  ")
            if len(auth_data) > 0:
                if not auth_data[0] == b"":
                    device_key = mac_decrypt_key(auth_data[0])
            if len(auth_data) > 1:
                session_key = mac_decrypt_key(auth_data[1])


    # todo version load
    #to_c(f"Loaded version is {unverified_version} (UNVERIFIED)")

    if session_key:
        print("login with session key")
        send_e(f"LOGIN:{session_key}")
        print(f" >> Request sent: LOGIN:{session_key}")
        login_request_response = send_d()
        if login_request_response != "INVALID_SK":
            session_key = login_request_response
            print(f" << VALID")
            to_c(f"\n🱫[COLOR THREAD][GREEN] You are now logged in as USERNAME_PLACEHOLDER#TAG")
            break
        else:
            print(" << INVALID_SK")
            input("what to do here")  # todo
    else:
        if device_key:
            print("get new session_key")
            send_e(f"NEWSK:{enc.pass_to_seed(device_key, keys.get_key(0, 'mac'))}")
            print(f" >> Request sent: NEWSK:{device_key}")
            dk_request_response = send_d()
            if dk_request_response != "INVALID_DK":
                session_key = dk_request_response
                print(f" << VALID:{session_key}")
                auth_txt_write(device_key, session_key)
            else:
                print(" << INVALID_DK")
        else:
            print("create new account or log in")
            to_c("🱫[INPUT SHOW]🱫[MNINPLEN][256] ", 0.1)  # todo set len to 7?
            while True:
                to_c("\n🱫[COLOR THREAD][YELLOW] Type 'login' or 'sign up'")
                login_signup = receive().lower().replace(" ", "")
                if login_signup in ["login", "signup"]:
                    break
            if login_signup == "login":
                print("login system")
                request = "LOGIN:"
            else:
                password = None
                while True:
                    while True:
                        to_c("\n🱫[COLOR THREAD][YELLOW] Please enter an email", 0.1)
                        email = receive().lower()
                        if "@" not in email:
                            to_c("\n🱫[COLOR THREAD][RED] Email does not contain an '@'")
                        else:
                            break

                    while password is None:
                        to_c("\n🱫[COLOR THREAD][YELLOW] Please enter a password", 0.1)
                        # password_entry_1 = receive()
                        password_entry_1 = "f839056vgnq5"
                        if len(password_entry_1) < 8:
                            to_c("\n🱫[COLOR THREAD][RED] PASSWORD TO SHORT! (must be at least 8 chars)")
                        else:
                            to_c(f"\n Entered ({len(password_entry_1)}chrs): "+"*"*len(password_entry_1))
                            to_c("\n🱫[COLOR THREAD][YELLOW] Please re-enter password", 0.1)
                            # password_entry_2 = receive()
                            password_entry_2 = "f839056vgnq5"
                            if password_entry_1 == password_entry_2:
                                password = enc.pass_to_seed(password_entry_1, default_salt)
                                break
                            else:
                                to_c("\n🱫[COLOR THREAD][RED] PASSWORDS DO NOT MATCH!")
                                password = None
                    send_e(f"NEWAC:{email}<|>{password}")
                    print(f" >> Request sent: NEWAC:{email}<|>{password}")
                    create_ac_response = send_d()
                    if create_ac_response == "INVALID_EMAIL":
                        print(" << INVALID_EMAIL")
                        to_c("\n🱫[COLOR THREAD][RED] Email was invalid, probably already taken")
                    else:
                        print(" << VALID")
                        break
                device_key = enc.hex_gens(128)
                salted_dk = enc.pass_to_seed(device_key, keys.get_key(0, "mac"))
                to_c(f"\n🱫[COLOR THREAD][GREEN] A verification code has "
                     f"been send to '{email}' (code valid for 15 minutes)")
                # to_c("🱫[INPUT SHOW]🱫[MNINPLEN][16] ", 0.1)  # todo set limit?

                while True:
                    to_c(f"\n🱫[COLOR THREAD][YELLOW] Enter 16 char code below", 0.1)
                    email_code = ""
                    while len(email_code) != 16:
                        email_code = receive().replace("-", "")

                    send_e(f"{email_code}<|>{salted_dk}")
                    print(f" >> Request sent: {email_code}<|>{salted_dk}")
                    verify_dk_response = send_d()
                    if verify_dk_response == "VALID":
                        print(" << VALID")
                        break
                    else:
                        print(" << INVALID_CODE")
                        to_c("\n🱫[COLOR THREAD][RED] Invalid email code")

                while True:
                    to_c(f"\n🱫[COLOR THREAD][YELLOW] Enter a username (upto 32 chars)", 0.1)
                    while True:
                        username = receive().replace("#", "")
                        if 2 < len(username) < 33:
                            break
                        else:
                            to_c(f"\n🱫[COLOR THREAD][RED] Username must be 3-32 chars", 0.1)

                    send_e(username)
                    print(f" >> Request sent: {username}")
                    verify_dk_response = send_d()
                    if verify_dk_response == "INVALID_NAME":
                        print(" << INVALID_NAME")
                        to_c("\n🱫[COLOR THREAD][RED] Username already taken")
                    else:
                        print(f" << VALID")
                        break

                auth_txt_write(device_key)
                to_c("\n🱫[COLOR THREAD][GREEN] Account setup complete, logging in...")
                print("Username accepted, account setup complete, dk received and saved")


# todo grab version and updates here after login
input("LOGGED IN")


def listen_for_server(cs):

    def receive():
        output = cs.recv(1024).decode(encoding="utf-16")
        if output.lower() == '-restart':
            should_exit.change(0, "FQR")

        if output.lower() == '-quit':
            should_exit.change(0, "FQ")
        return output

    # code removed

    content = mac_decrypt_key(s.recv(1024))
    print(f"reached login checks - {content}")
    if content.startswith("NOTREAL"):
        to_c("\n🱫[COLOR THREAD][RED] <> INVALID VERSION DETECTED, downloading replacements"
             " in 5 seconds")
        time.sleep(5)
        should_exit.change(0, "FQU")

    if content.startswith("INVALID-"):
        to_c(f"\n <> Updating rdisc {content[8:]} in 5 seconds")
        time.sleep(5)
        should_exit.change(0, "FQU")
        auth_txt_write(session_key, content[8:].split('->')[0])
        while True:
            receive()

    if content.startswith("NO_ACC_FND"):
        to_c("\n🱫[COLOR THREAD][RED] INVALID LOGIN TOKEN. Ask developer for support")

    if content.startswith("VALID-"):
        to_c("\n🱫[COLOR THREAD][GREEN] << Login success")
        verified_version = content[6:].split('-')[0]
        to_c(f"\n << RESPONSE FROM AUTH RECEIVED\n << {verified_version}")
        to_c(f"Verified version is {verified_version} (VERIFIED)", 0.1)

        auth_txt_write(session_key, verified_version)  # 1 more key supported
        to_c("🱫[INPUT SHOW]\n🱫[COLOR THREAD][GREEN] << You are now logged in and can post messages", 0.1)

        def listen_for_messages():
            print("message listener launched")
            while True:
                to_c(f"\n{mac_decrypt_key(s.recv(1024))}")

        t = Thread(target=listen_for_messages)
        t.daemon = True
        t.start()

        print("input handler launched")
        while True:
            received = s.recv(1024).decode(encoding="utf-16")
            received_l = received.lower()
            client_send = None
            send = True
            print(received, received_l)

            # internal
            if received_l == '-restart':
                should_exit.change(0, "FQR")
                send = False

            if received_l == '-quit':
                should_exit.change(0, "FQ")
                send = False

            if received_l.startswith("-change password "):
                send = False
                if len(received[17:]) < 8:
                    to_c("\n🱫[COLOR THREAD][RED] Password to short (must be 8-256 chars)")
                    to_c(f"🱫[MNINPTXT] {received}", 0.1)
                else:
                    if len(received[13:]) > 256:
                        to_c("\n🱫[COLOR THREAD][RED] Password to large (must be 8-256 chars)")
                        to_c(f"🱫[MNINPTXT] {received}", 0.1)
                    else:
                        keys.update_key(0, "pass_key", received[17:])
                        auth_txt_write(session_key, verified_version)
                        to_c(f"\n New password set ({len(received[17:])}chrs): " + "*" * len(received[17:]))

            # external
            if received_l.startswith("-change name "):
                send = False
                if len(received[13:]) < 4:
                    to_c("\n🱫[COLOR THREAD][RED] Name to short (must be 4-32 chars)")
                    to_c(f"🱫[MNINPTXT] {received}", 0.1)
                else:
                    if len(received[13:]) > 32:
                        to_c("\n🱫[COLOR THREAD][RED] Name to large (must be 4-32 chars)")
                        to_c(f"🱫[MNINPTXT] {received}", 0.1)
                    else:
                        client_send = f"CAN{received[13:]}"
                        send = True

            if send:
                if not client_send:
                    client_send = f"MSG{received}"

                while received.endswith("\n"):
                    received = received[:-2]

                checked = cooldown.check(0)  # todo maybe stop input until allowed, bring back what was entered
                if checked == "True":
                    s.send(enc.encrypt_key(client_send, keys.get_key(0, "df_key"), "salt"))
                else:
                    to_c(f"\nYOU'RE SENDING MESSAGES TOO FAST! please wait {checked}s~")


t = Thread(target=listen_for_server, args=(cs,))
t.daemon = True
t.start()


while True:
    if should_exit.check(0).startswith("FQ"):
        #if should_exit.check(0) == "FQU":
        #    os.startfile("installer.exe")
        if should_exit.check(0) == "FQR":
            os.startfile("rdisc.exe")
        break
    time.sleep(1)
