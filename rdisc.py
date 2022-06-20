import socket, datetime, zlib, rsa
from os import path, startfile, remove
from time import sleep
from uuid import getnode as get_mac
from hashlib import sha512
import enclib as enc

# local sockets localhost:8079, localhost:8080
# Made by rapidslayer101 (Scott Bree), General usage testing and spelling: James Judge
# >>> license and agreement data here <<<

if path.exists("rdisc.py"):
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
else:
    hashed = enc.hash_a_file("rdisc.exe")


ui = True
ui_s = False

while True:
    if ui:
        if not ui_s:
            ui_s = socket.socket()
            ui_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if path.exists("rdisc.py"):
                ui_s.bind(("127.0.0.1", 8078))
            else:
                ui_s.bind(("127.0.0.1", 8079))
            print(" -> Launching ui.exe")
            if not path.isfile("ui.exe"):
                print("[!] CRITICAL FILE ui.exe MISSING, falling back to CLI\n")
                ui = False
            else:
                startfile("ui.exe")
                print(" <- ui.exe launched")
                ui_s.listen(1)
                cs, client_address = ui_s.accept()

                def to_c(text, delay=None):
                    if delay:
                        sleep(delay)
                    try:
                        cs.send(str(text).encode(encoding="utf-16"))
                    except ConnectionResetError:
                        exit.update("EXIT")
                print(f"Connected to ui.exe via socket {client_address}")
                to_c("\n🱫[COLOR][GRN] <- Internal socket connected\n", 0.1)
    if not ui:
        def to_c(text, delay=None):
            if delay:
                sleep(delay)
            if text.startswith("🱫[INP SHOW]🱫"):
                text = text[14:]
            if text.startswith("\n🱫[COLOR][GRN] "):  # todo CLI colors
                text = text[15:]
            if text.startswith("\n🱫[COLOR][YEL] "):
                text = text[15:]
            if text.startswith("\n🱫[COLOR][RED] "):
                text = text[15:]
            if text.startswith("[MNINPLEN][256] "):
                text = text[16:]
            if not text == "":
                print(text)

    user_data = {}

    class user:
        def key(self):
            try:
                return user_data[self]
            except KeyError:
                return False

        def update_key(self, key):
            user_data.update({self: key})

    if path.exists("version.txt"):
        with open("version.txt", encoding="utf-8") as f:
            version, tme, bld_num, run_num = f.read().split('🱫')
        version = f"{version} ❌"
        to_c(f"🱫[LODVS] {version}")

    default_salt = "52gy\"J$&)6%0}fgYfm/%ino}PbJk$w<5~j'|+R .bJcSZ.H&3z'A:gip/jtW$6A=" \
                   "G-;|&&rR81!BTElChN|+\"TCM'CNJ+ws@ZQ~7[:¬`-OC8)JCTtI¬k<i#.\"H4tq)p4"
    mac = enc.pass_to_key(hex(get_mac()), default_salt, 100000)

    def mac_enc(text):
        return enc.encrypt_key(text, mac, default_salt)

    def mac_dec(enc_text):
        return enc.decrypt_key(enc_text, mac, default_salt)

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

    exit_reason = []

    class exit:
        def update(self):
            exit_reason.append(self)
            raise AssertionError

        def get(self):
            return exit_reason

    try:
        def process_from_c(output_):
            return_value = True
            if output_ in ['🱫[RELOAD]', "-reload"]:
                exit.update("RELOAD")
            if output_ in ['🱫[QUIT]', "-quit"]:
                exit.update("EXIT")
            if output_ in ['🱫[UI]', '🱫[UIR]', '-ui', '-ui reload', '-restart']:
                if output_ in ['🱫[UI]', '-ui']:
                    exit.update("UI")
                if output_ in ['🱫[UIR]', '-ui reload', '-restart']:
                    exit.update("UIR")
            if output_.startswith('🱫[CNGPASS'):
                print("Change password")
                n_pass_1 = None
                while n_pass_1 is None:
                    n_pass_1 = receive("\n🱫[COLOR][YEL] Please enter new password", 0.1)
                    if len(n_pass_1) < 8:
                        to_c("\n🱫[COLOR][RED] PASSWORD TO SHORT! (must be at least 8 chars)")
                    else:
                        to_c(f"\n Entered ({len(n_pass_1)}chrs): "+"*" * len(n_pass_1))
                        if n_pass_1 == receive("\n🱫[COLOR][YEL] Please re-enter password", 0.1):
                            n_pass_1 = enc.pass_to_key(n_pass_1, default_salt, 100000)
                            break
                        else:
                            to_c("\n🱫[COLOR][RED] PASSWORDS DO NOT MATCH!")
                            n_pass_1 = None
                old_pass = enc.pass_to_key(receive("\n🱫[COLOR][YEL] Enter old password"), default_salt, 100000)
                send_e(f"CPASS:{old_pass}🱫{n_pass_1}")
                print(f" >> CPASS:{old_pass}🱫{n_pass_1}")
                cng_pass_resp = recv_d(512)
                print(f" << {cng_pass_resp}")
                if cng_pass_resp == "V":
                    to_c("\n🱫[COLOR][GRN] Success! Password has been changed")
                else:
                    if cng_pass_resp == "SP":
                        to_c("\n🱫[COLOR][RED] Old pass and new pass are the same, exiting password change")
                    else:
                        to_c("\n🱫[COLOR][RED] Old password incorrect, exiting password change")

            if output_.startswith('🱫[LOG]'):
                if user.key('u_name'):
                    if output_ == '🱫[LOG]':
                        try:
                            remove("auth.txt")
                        except FileNotFoundError:
                            pass
                        exit.update("LOGOUT")
                    if output_ == '🱫[LOG_A]':
                        send_e("LOG_A")
                        try:
                            remove("auth.txt")
                        except FileNotFoundError:
                            pass
                        exit.update("LOGOUT")
                    else:
                        to_c("\n🱫[COLOR][RED] You must be logged in to perform this action")

            if output_.startswith('🱫[DELAC]'):
                if user.key('u_name'):
                    print("Delete account")
                    pass__ = enc.pass_to_key(receive("\n🱫[COLOR][YEL] Enter password to delete account"), default_salt, 100000)
                    send_e(f"DELAC:{pass__}")
                    print(f" >> DELAC:{pass__}")
                    if recv_d(512) == "V":
                        to_c("\n🱫[COLOR][GRN] A verification code has "
                             "been sent to your email (code valid for 15 minutes)")
                        while True:
                            to_c("\n🱫[COLOR][YEL] Enter 16 char code", 0.1)
                            email_code = ""
                            while len(email_code) != 16:
                                email_code = receive().replace("-", "").upper()
                            send_e(f"{email_code}")
                            print(f" >> {email_code}")
                            if recv_d(512) == "V":
                                print(" << VALID:ACCOUNT_DELETED")
                                to_c("\n🱫[COLOR][GRN] Request valid, account deleted")
                                try:
                                    remove("auth.txt")
                                except FileNotFoundError:
                                    pass
                                exit.update("LOGOUT")
                            else:
                                print(" << INVALID_CODE")
                                to_c("\n🱫[COLOR][RED] Invalid email code")
                    else:
                        to_c("\n🱫[COLOR][RED] Password incorrect, exiting account deletion")
                else:
                    to_c("\n🱫[COLOR][RED] You must be logged in to perform this action")
            if output_ == '🱫[GET_VDATA_E]':
                try:
                    to_c(f"🱫[LODVS_E] {version}-{tme}-{bld_num}-{run_num}")
                except:
                    pass
                return_value = False
            if output_ == '🱫[GET_VDATA]':
                try:
                    to_c(f"🱫[LODVS] {version}")
                except:
                    pass
                return_value = False
            if return_value:
                return True
            else:
                return False
        if ui:
            def receive(c_text=None, delay=None):
                if c_text:
                    if delay:
                        to_c(c_text, delay)
                    else:
                        to_c(c_text)
                while True:
                    try:
                        output = cs.recv(1024).decode(encoding="utf-16")
                    except ConnectionResetError:
                        exit.update("EXIT")
                    if process_from_c(output):
                        break
                return output
        else:
            def receive(c_text=None, delay=None):
                if c_text:
                    if delay:
                        to_c(c_text, delay)
                    else:
                        to_c(c_text)
                output = input()
                process_from_c(output)
                return output

        # Load auth key

        sign_up = False
        not_found_usb_error = False
        while True:
            to_c("🱫[INP SHOW]🱫[MNINPLEN][256] ", 0.1)
            if not path.exists('key_location'):
                to_c("\n🱫[COLOR][YEL] Set 'Access USB Key' drive - Eg 'D:/'")
                while True:
                    key_location = receive()
                    if not path.exists(f'{key_location}key'):
                        to_c("\n🱫[COLOR][RED] This location does not contain a key file, please try again")
                    else:
                        with open(f'key_location', 'w') as f:
                            f.write(key_location)
                        break
            else:
                with open('key_location', 'r') as f:
                    key_location = f.read()
                try:
                    with open(f'{key_location}key', 'rb') as f:
                        key_data = f.read()
                    if path.exists(f'{key_location}key_salt'):
                        with open(f'{key_location}key_salt') as f:
                            key_salt = f.read()
                        with open(f'{key_location}u_id') as f:
                            u_id = f.read()
                    else:
                        to_c("\n Enter the activation key")
                        while True:
                            #act_pass = receive()
                            act_pass = """8qYu[xkh"T]|>4I{G<£gY6)6F pLv2zD¬Vqk0M9P6V`82m+Pv//P/gX>5]1e?lb$8,GBt#7h%|IU{r"""
                            try:
                                sign_up_key = sha512(enc.dec_from_key(key_data, act_pass).encode()).hexdigest()
                                break
                            except zlib.error:
                                to_c("\n🱫[COLOR][RED] Invalid activation key")
                        to_c("\n🱫[COLOR][GRN] Key unlocked, validating hash with server")
                        sign_up = True
                    break
                except FileNotFoundError:
                    if not not_found_usb_error:
                        to_c("\n🱫[COLOR][RED] Key file not found, insert USB")
                    not_found_usb_error = True
                    sleep(0.2)

        # Establish connection to server

        pub_key, pri_key = rsa.newkeys(512)
        server_host = "192.168.1.153"
        server_port = 8080
        s = socket.socket()
        to_c("\n\n >> Connecting to server")
        server_connect_error = False
        while True:
            try:
                s.connect((server_host, server_port))
                to_c("\n🱫[COLOR][GRN] << Connected to server")
                break
            except ConnectionRefusedError:
                to_c("\n🱫[COLOR][RED] Could not connect to server")
                if not server_connect_error:
                    to_c("\n🱫[COLOR][YEL] Enter something to retry connection", 0.1)
                server_connect_error = True
                receive("🱫[INP SHOW]", 0.1)
                to_c("🱫[INP HIDE]", 0.1)

        l_ip, l_port = str(s).split("laddr=")[1].split("raddr=")[0][2:-3].split("', ")
        s_ip, s_port = str(s).split("raddr=")[1][2:-2].split("', ")
        print(f"Server connected via {l_ip}:{l_port} -> {s_ip}:{s_port}")
        try:
            s.send(rsa.PublicKey.save_pkcs1(pub_key))
        except ConnectionResetError:
            exit.update("CONNECTION_LOST")
        print(" >> Public RSA key sent")
        enc_seed = rsa.decrypt(s.recv(128), pri_key).decode()
        enc_salt = rsa.decrypt(s.recv(128), pri_key).decode()
        enc_key = enc.pass_to_key(enc_seed, enc_salt, 100000)
        print(" << Client enc_seed and enc_salt received and loaded")
        to_c("\n🱫[COLOR][GRN] RSA Enc bootstrap complete\n")

        def send_e(text):
            try:
                s.send(enc.enc_from_key(text, enc_key))
            except ConnectionResetError:
                exit.update("CONNECTION_LOST")

        def recv_d(buf_lim):
            try:
                return enc.dec_from_key(s.recv(buf_lim), enc_key)
            except ConnectionResetError:
                exit.update("CONNECTION_LOST")

        # Login system

        if sign_up:
            print("Create a new account")
            send_e(f"NAC:{sign_up_key}")
            print(" >> Sign up key sent")
            nac_resp = recv_d(512)
            if nac_resp == "N":
                print(" << Invalid signup hash")
                to_c("\n🱫[COLOR][RED] Invalid activation key")
                remove("key_location")
                exit.update("INVALID_SIGNUP_HASH")
            else:
                key_salt = nac_resp[2:]
                print(" << Valid signup hash: Key salt received")
                to_c("\n🱫[COLOR][GRN] Activation key validated")
                pass_ = None
                while pass_ is None:
                    pass_1 = receive("\n🱫[COLOR][YEL] Please enter a password", 0.1)
                    if len(pass_1) < 8:
                        to_c("\n🱫[COLOR][RED] PASSWORD TO SHORT! (must be at least 8 chars)")
                    else:
                        to_c(f"\n Entered ({len(pass_1)}chrs): " + "*" * len(pass_1))
                        if pass_1 == receive("\n🱫[COLOR][YEL] Please re-enter password", 0.1):
                            pass_ = enc.pass_to_key(pass_1, default_salt, 100000)
                            break
                        else:
                            to_c("\n🱫[COLOR][RED] PASSWORDS DO NOT MATCH!")
                            pass_ = None
                send_e(pass_)
                print(" >> Password sent")
                depth = int(recv_d(512))
                print(f" << challenge_int received: {depth}")
                user_challenge = sha512(enc.pass_to_key(pass_, key_salt, depth).encode()).hexdigest()
                send_e(user_challenge)
                print(" >> challenge_hash sent")
                u_id = recv_d(512)
                if u_id != "N":
                    print(f" << received user_id: {u_id}")
                    to_c(f"\n🱫[COLOR][GRN] User authenticated, account '{u_id}' created successfully")
                else:
                    print(" << AUTH_FAILED")
                    to_c("\n🱫[COLOR][RED] User authentication failed")
                    exit.update("AUTH_FAILED")
                with open(f'{key_location}key_salt', 'w') as f:
                    f.write(key_salt)
                with open(f'{key_location}u_id', 'w') as f:
                    f.write(u_id)
                print("Wrote key_salt and u_id")
                break
        else:
            print("Login with existing account")
            send_e(f"LOG:{u_id}")
            print(" >> u_id sent")
            while True:
                depth = recv_d(512)
                if depth == "N_UID":
                    print(" << INVALID_U_ID")
                    to_c("\n🱫[COLOR][RED] User does not exist")
                if depth == "SESH_T":
                    print(" << SESSION_TAKEN")
                    to_c("\n🱫[COLOR][RED] This account or IP is already logged in")
                    exit.update("SESH_TAKEN")
                else:
                    print(f" << challenge_int received: {depth}")
                    pass_ = receive("\n🱫[COLOR][YEL] Please enter your password", 0.1)
                    pass_ = enc.pass_to_key(pass_, default_salt, 100000)
                    user_challenge = sha512(enc.pass_to_key(pass_, key_salt, int(depth)).encode()).hexdigest()
                    send_e(user_challenge)
                    print(" >> challenge_hash sent")
                    challenge_resp = recv_d(512)
                    if challenge_resp != "N":
                        print(" << logged in")
                        to_c("\n🱫[COLOR][GRN] Logged in successfully")
                        break
                    else:
                        print(" << AUTH_FAILED")
                        to_c("\n🱫[COLOR][RED] User authentication failed")
        print("Version updater")
        send_e(hashed)
        print(f" >> {hashed}")
        v_check_resp = recv_d(512)
        print(f" << {v_check_resp}")
        if v_check_resp.startswith("V"):
            with open("version.txt", "w", encoding="utf-8") as f:
                f.write(v_check_resp[1:])
            version, tme, bld_num, run_num = v_check_resp[1:].split('🱫')
            version = f"{version} ✔"
            to_c(f"🱫[LODVS] {version}", 0.1)

        if v_check_resp.startswith("N"):
            version_up_info, update_size, update_hash = v_check_resp[1:].split("🱫")
            to_c(f"\n <> Updating rdisc {version_up_info} ({round(int(update_size)/1024/1024, 2)}MB)")
            exit.update("UPDATE")

        if v_check_resp.startswith("UNKNOWN"):
            update_size, update_hash = v_check_resp[7:].split("🱫")
            to_c("\n🱫[COLOR][RED] <> INVALID OR CORRUPTED VERSION, downloading new copy")
            exit.update("UPDATE")

        to_c(f"\n🱫[COLOR][GRN] You are now logged in as {user.key('u_id')}")
        to_c("🱫[INP SHOW]🱫", 0.1)
        print("Logged in loop")
        while True:
            # user data loading
            request = receive()
            if request.startswith("-change name"):
                username = request[13:].replace("#", "").replace(" ", "")
                if username == user.key('u_name')[:-5]:
                    to_c("\n🱫[COLOR][RED] Username cannot be the same as previous username")
                else:
                    if 4 < len(username) < 33:
                        send_e(f"CUSRN:{username}")
                        print(f" >> CUSRN:{username}")
                        new_u_name_resp = recv_d(128)
                        if new_u_name_resp == "N_NAME":
                            print(" << INVALID_NAME")
                            to_c("\n🱫[COLOR][RED] Username already taken")
                        else:
                            print(" << VALID")
                            to_c("\n🱫[COLOR][GRN] Username changed to "
                                 f"{new_u_name_resp[1:]} from {user.key('u_name')}")
                            user.update_key('u_name', new_u_name_resp[1:])
                    else:
                        to_c(f"\n🱫[COLOR][RED] Username must be 5-32 chars, you entered: {username[:64]}")

            #if request.startswith("-add friend"):
            #    add_friend_n = request[12:]
            #    if 9 < len(add_friend_n) < 38:
            #        try:
            #            int(add_friend_n[-4:])
            #            if add_friend_n[-5] != "#":
            #                to_c(f"\n🱫[COLOR][RED] Tag missing or invalid (eg #0001)")
            #            else:
            #                send_e(f"ADDFR:{add_friend_n}")
            #                print(f" >> ADDFR:{add_friend_n}")
            #                new_fr_req = recv_d(128)
            #                print(new_fr_req)
            #        except ValueError:
            #            to_c(f"\n🱫[COLOR][RED] Invalid tag (tag example: #0001)")
            #    else:
            #        to_c(f"\n🱫[COLOR][RED] Username+Tag must be 10-37 chars, you entered: {add_friend_n[:64]}")

    except AssertionError:
        exit_reason = str(exit.get(0))[2:-2]
        if exit_reason == "SESH_TAKEN":
            to_c("🱫[INP SHOW]", 0.1)
            receive("\n🱫[COLOR][YEL] Enter something to retry connection", 0.)
            to_c("🱫[INP HIDE]", 0.1)
            exit_reason = "RELOAD"
        if exit_reason == "CONNECTION_LOST":
            print("SERVER CONNECTION LOST, RELOADING")
            to_c("🱫[CLRO]")
            to_c("\n🱫[COLOR][RED] Connection lost - Reloading")
        if exit_reason in ["RELOAD", "UI", "UIR"]:
            if exit_reason in ["UI", "UIR"]:
                if ui:
                    to_c("🱫[EXIT]")
                    s.close()
                    ui_s = False
                    if exit_reason == "UI":
                        ui = False
                else:
                    ui = True
            print("RELOADING")
            to_c("🱫[CLRO]")
            to_c("\n🱫[COLOR][GRN] -- Reloading --", 0.1)
        if exit_reason == "UPDATE":
            with open("Update.zip", "wb") as f:
                for i in range((int(update_size)//4096)+1):
                    bytes_read = s.recv(4096)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
            if enc.hash_a_file("Update.zip") == update_hash:
                to_c("🱫[EXIT]")
                sleep(0.5)
                startfile("updater.exe")
                break
            else:
                to_c("\n🱫[COLOR][RED] Update files corrupt")
        if exit_reason in ["RESTART", "EXIT"]:
            to_c("🱫[EXIT]")
            s.close()
        if exit_reason == "EXIT":
            break

# if cooldown.check(0) == "True":  # todo maybe stop input until allowed, bring back what was entered
#    s.send(enc.encrypt_key(client_send, user.key('df_key'), "salt"))
# else:
#    to_c(f"\nYOU'RE SENDING MESSAGES TOO FAST! please wait {checked}s~")
