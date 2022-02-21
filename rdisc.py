import socket, os, time, datetime, zlib, rsa, uuid
from threading import Thread
import enclib as enc


try:
    hashed = enc.hash_a_file("rdisc.py")
    with open("sha.txt", "r", encoding="utf-8") as f:
        latest_sha_, run_type_, version_, tme_, bld_num_, run_num_ = f.readlines()[-1].split("§")
    print("prev", run_type_, version_, tme_, bld_num_, run_num_)
    release_major, major, build, run = version_.replace("V", "").split(".")

    if latest_sha_ != hashed:
        run = int(run) + 1
        with open("sha.txt", "a+", encoding="utf-8") as f:
            write = f"\n{hashed}§RUN§V{release_major}.{major}.{build}.{run}" \
                    f"§TME-{str(datetime.datetime.now())[:-4].replace(' ', '_')}" \
                    f"§BLD_NM-{bld_num_[7:]}§RUN_NM-{int(run_num_[7:])+1}"
            print(f"crnt RUN V{release_major}.{major}.{build}.{run} "
                  f"TME-{str(datetime.datetime.now())[:-4].replace(' ', '_')} "
                  f"BLD_NM-{bld_num_[7:]} RUN_NM-{int(run_num_[7:])+1}")
            f.write(write)
        print(f"Running rdisc V{release_major}.{major}.{build}.{run}")
except FileNotFoundError:
    hashed = enc.hash_a_file("rdisc.exe")


exit_state = {"QUIT": "--"}


class should_exit:
    def check(self):
        return exit_state["QUIT"]

    def change(self):
        return exit_state.update({"QUIT": self})


ui_s = socket.socket()
ui_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if os.path.exists("rdisc.py"):
    ui_s.bind(("127.0.0.1", 8078))
else:
    ui_s.bind(("127.0.0.1", 8079))

print(" -> Launching ui.exe")
if not os.path.isfile("ui.exe"):
    print("[!] CRITICAL FILE ui.exe MISSING")
else:
    os.startfile("ui.exe")
print(" <- ui.exe launched")
ui_s.listen(10)
cs, client_address = ui_s.accept()


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
# 0.21 version checking (on setup know version), username changing
# 0.22 login and signup rework -> a new dk call will now also give back a sk, general validation framework
# 0.23 users folder with new user saving to support more future data and data access efficiency, uid now in auth.txt
# 0.24 dynamic loading rewrites, solution cleanup

# 0.25 finding other clients, connecting to them / friending (on/offline), user tag support

# 0.26 basic DM chat functionality with client to server to client connections and keys
# 0.27 downloading, saving, load req files from a first time setup file
# 0.28 logout system and storing data


# local sockets localhost:8079, localhost:8080
# Made by rapidslayer101 (Scott Bree), Main tester: James Judge
# >>> license and agreement data here <<<

user_data = {}


class user:
    def key(self):
        try:
            return user_data[self]
        except KeyError:
            return False

    def update_key(self, key):
        user_data.update({self: key})


default_salt = """52gy"J$&)6%0}fgYfm/%ino}PbJk$w<5~j'|+R .bJcSZ.H&3z'A:gip/jtW$6A=
                  G-;|&&rR81!BTElChN|+"TCM'CNJ+ws@ZQ~7[:¬`-OC8)JCTtI¬k<i#."H4tq)p4"""  # todo improve, pass+salt?
mac = enc.pass_to_seed(hex(uuid.getnode()), default_salt)


def mac_enc(text):
    return enc.encrypt_key(text, mac, default_salt)


def mac_dec(enc_text):
    return enc.decrypt_key(enc_text, mac, default_salt)


def auth_txt_write(uid, dk, sk=None):
    auth_to_write = b""
    if dk:
        auth_to_write += mac_enc(uid)
        auth_to_write += b"  "+mac_enc(dk)
    if sk:
        auth_to_write += b"  "+mac_enc(sk)
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

        if cool_down_data["msg_counter"] > 10:  # total before counter triggers' cooldown(s)
            return round(5-time_since_last.seconds, 2)
        else:
            cool_down_data.update({"x": (str(datetime.datetime.utcnow()))})
            return "True"


def listen_for_server(cs):
    def receive(c_text=None, delay=None):
        if c_text:
            if delay:
                to_c(c_text, delay)
            else:
                to_c(c_text)
        output = cs.recv(1024).decode(encoding="utf-16")
        if output.lower() == '-restart':
            should_exit.change("FQR")

        if output.lower() == '-quit':
            should_exit.change("FQ")
        return output

    pub_key, pri_key = rsa.newkeys(1024)
    server_host = "26.29.111.99"
    server_port = 8080
    s = socket.socket()
    while True:
        try:
            s.connect((server_host, server_port))
            to_c("\n🱫[COLOR THREAD][GREEN] Connected to server")
            break
        except ConnectionRefusedError:
            to_c("\n🱫[COLOR THREAD][RED] Could not connect to server")
            receive("🱫[INPUT SHOW]\n🱫[COLOR THREAD][YELLOW] Enter something to retry connection")
            to_c("🱫[INPUT HIDE]")

    print("Server connected ->", s)
    s.send(rsa.PublicKey.save_pkcs1(pub_key))
    print(" >> Public RSA key sent")
    enc_seed = rsa.decrypt(s.recv(1024), pri_key).decode()
    enc_salt = rsa.decrypt(s.recv(1024), pri_key).decode()
    alpha, shift_seed = enc.seed_to_data(enc_seed)
    print(" << Client enc_seed and enc_salt received and loaded")
    to_c("\n🱫[COLOR THREAD][GREEN] RSA -> enc bootstrap complete")

    def send_e(text):
        s.send(enc.encrypt("e", text, alpha, shift_seed, enc_salt))

    def recv_d():
        return enc.encrypt("d", s.recv(1024), alpha, shift_seed, enc_salt)

    device_key = False
    if os.path.isfile("auth.txt"):
        with open("auth.txt", "rb") as auth_txt:
            auth_data = auth_txt.read().split(b"  ")
            if len(auth_data) > 1:
                if not auth_data[0] == b"":
                    try:
                        user.update_key('uid', mac_dec(auth_data[0]))
                        print(f"LOADED UID")

                    except zlib.error:
                        pass
                    try:
                        device_key = mac_dec(auth_data[1])
                        print(f"LOADED DK")
                    except zlib.error:
                        pass
            if len(auth_data) > 2:
                try:
                    user.update_key('sk', mac_dec(auth_data[2]))
                    print(f"LOADED SK")
                except zlib.error:
                    pass

    def login():
        print("Login with session key")
        send_e(f"LOGIN:{user.key('uid')}🱫{user.key('sk')}")
        print(f" >> Request sent: LOGIN:{user.key('uid')}🱫{user.key('sk')}")
        login_req_resp = recv_d()
        if login_req_resp.startswith("VALID:"):
            print(f" << {login_req_resp}")
            to_c(f"\n🱫[COLOR THREAD][GREEN] You are now logged in as {login_req_resp[6:]}")
            user.update_key('u_name', login_req_resp[6:])
            return True
        else:
            print(" << INVALID_SK")
            return False

    while True:  # login loop
        if user.key('sk'):
            if login():
                break
        if device_key:
            print("Get a new session_key")
            send_e(f"NEWSK:{user.key('uid')}🱫{enc.pass_to_seed(device_key, mac)}")
            print(f" >> Request sent: NEWSK:{user.key('uid')}🱫{enc.pass_to_seed(device_key, mac)}")
            dk_req_resp = recv_d()
            if dk_req_resp.startswith("VALID:"):
                session_key = dk_req_resp[6:]
                print(f" << VALID:{session_key}")
                auth_txt_write(user.key('uid'), device_key, session_key)
                user.update_key('sk', session_key)
                if login():
                    break
            else:
                print(" << INVALID_DK")

        print("Create a new account or log in to an existing one")
        to_c("🱫[INPUT SHOW]🱫[MNINPLEN][256] ", 0.1)  # todo set len to 7?
        while True:
            to_c("Create a new account or log in to an existing one")
            login_signup = receive("\n🱫[COLOR THREAD][YELLOW] Type 'login' or 'sign up'", 0.1).lower().replace(" ", "")
            if login_signup in ["login", "signup"]:
                break

        def enter_email():
            while True:
                email_ = receive("\n🱫[COLOR THREAD][YELLOW] Please enter email", 0.1).lower()
                if "@" not in email_:
                    to_c("\n🱫[COLOR THREAD][RED] Email does not contain an '@'")
                else:
                    break
            return email_

        def make_new_dk():
            print("Get a new device_key and session_key")
            device_key_ = enc.hex_gens(128)
            salted_dk = enc.pass_to_seed(device_key_, mac)
            to_c(f"\n🱫[COLOR THREAD][GREEN] A verification code has "
                 f"been sent to '{email}' (code valid for 15 minutes)")
            # to_c("🱫[INPUT SHOW]🱫[MNINPLEN][16] ", 0.1)  # todo set limit?

            while True:
                to_c(f"\n🱫[COLOR THREAD][YELLOW] Enter 16 char code below", 0.1)
                email_code = ""
                while len(email_code) != 16:  # todo improve
                    email_code = receive().replace("-", "").upper()

                send_e(f"{email_code}🱫{salted_dk}")
                print(f" >> Request sent: {email_code}🱫{salted_dk}")
                verify_dk_resp = recv_d()
                if verify_dk_resp.startswith("VALID:"):
                    print(f" << {verify_dk_resp}")
                    break
                else:
                    print(" << INVALID_CODE")
                    to_c("\n🱫[COLOR THREAD][RED] Invalid email code")
            uid, session_key_ = verify_dk_resp[6:].split("🱫")
            auth_txt_write(uid, device_key_, session_key_)
            user.update_key('sk', session_key_)
            user.update_key('uid', uid)

        if login_signup == "login":
            print("Login system")
            while True:
                email = enter_email()
                to_c("\n🱫[COLOR THREAD][YELLOW] Please enter your password", 0.1)
                password = enc.pass_to_seed(receive(), default_salt)
                send_e(f"NEWDK:{email}🱫{password}")
                print(f" >> Request sent: NEWDK:{email}🱫{password}")
                get_dk_response = recv_d()
                if get_dk_response == "INVALID":
                    print(" << INVALID")
                    to_c("\n🱫[COLOR THREAD][RED] Email or password invalid")
                else:
                    print(" << VALID")
                    break

            make_new_dk()
        else:
            password = None
            while True:
                email = enter_email()
                while password is None:
                    password_entry_1 = receive("\n🱫[COLOR THREAD][YELLOW] Please enter a password", 0.1)
                    if len(password_entry_1) < 8:
                        to_c("\n🱫[COLOR THREAD][RED] PASSWORD TO SHORT! (must be at least 8 chars)")
                    else:
                        to_c(f"\n Entered ({len(password_entry_1)}chrs): "+"*"*len(password_entry_1))
                        password_entry_2 = receive("\n🱫[COLOR THREAD][YELLOW] Please re-enter password", 0.1)
                        if password_entry_1 == password_entry_2:
                            password = enc.pass_to_seed(password_entry_1, default_salt)
                            break
                        else:
                            to_c("\n🱫[COLOR THREAD][RED] PASSWORDS DO NOT MATCH!")
                            password = None
                send_e(f"NEWAC:{email}🱫{password}")
                print(f" >> Request sent: NEWAC:{email}🱫{password}")
                create_ac_response = recv_d()
                if create_ac_response == "INVALID_EMAIL":
                    print(" << INVALID_EMAIL")
                    to_c("\n🱫[COLOR THREAD][RED] Email was invalid, probably already taken")
                else:
                    print(" << VALID")
                    break

            make_new_dk()
            to_c("\n🱫[COLOR THREAD][GREEN] Account setup complete, logging in...")
            print("Account setup complete, dk and sk received and saved")

    print("Version updater")  # todo version load
    send_e(f"VCHCK:{hashed}")
    print(f" >> VCHCK:{hashed}")
    version_check_response = recv_d()
    print(f" << {version_check_response}")
    if version_check_response.startswith("VALID:"):
        verified_version, tme, bld_num, run_num = version_check_response[6:].split('🱫')
        to_c(f"Verified version is {verified_version} (VERIFIED)", 0.1)

    if version_check_response.startswith("INVALID:"):
        to_c(f"\n <> Updating rdisc {version_check_response[8:]} in 5 seconds")
        time.sleep(5)
        should_exit.change("FQU")
        while True:
            receive()

    if version_check_response.startswith("UNKNOWN"):
        to_c("\n🱫[COLOR THREAD][RED] <> INVALID OR CORRUPTED VERSION, downloading new copy in 5 seconds")
        time.sleep(5)
        should_exit.change("FQU")

    to_c("🱫[INPUT SHOW]🱫", 0.1)
    print("Main thread")
    while True:
        request = receive()

        if request.startswith("-change name"):
            username = request[13:].replace("#", "").replace(" ", "")
            if username == user.key('u_name')[:-5]:
                to_c(f"\n🱫[COLOR THREAD][RED] Username cannot be the same as previous username")
            else:
                if 4 < len(username) < 33:
                    send_e(f"CUSRN:{username}")
                    print(f" >> Request sent: CUSRN:{username}")
                    new_u_name_resp = recv_d()
                    if new_u_name_resp == "INVALID_NAME":
                        print(" << INVALID_NAME")
                        to_c("\n🱫[COLOR THREAD][RED] Username already taken")
                    else:
                        print(f" << VALID")
                        to_c(f"\n🱫[COLOR THREAD][GREEN] Username changed to "
                             f"{new_u_name_resp[6:]} from {user.key('u_name')}")
                        user.update_key('u_name', new_u_name_resp[6:])
                else:
                    to_c(f"\n🱫[COLOR THREAD][RED] Username must be 5-32 chars, you entered: {username[:64]}")

    print("Exit")

    #checked = cooldown.check(0)  # todo maybe stop input until allowed, bring back what was entered
    #if checked == "True":
    #    s.send(enc.encrypt_key(client_send, user.key('df_key'), "salt"))
    #else:
    #    to_c(f"\nYOU'RE SENDING MESSAGES TOO FAST! please wait {checked}s~")


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
