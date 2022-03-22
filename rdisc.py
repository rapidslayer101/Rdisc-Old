import socket, os, time, datetime, zlib, uuid, rsa
import enclib as enc

# local sockets localhost:8079, localhost:8080
# Made by rapidslayer101 (Scott Bree), General usage testing and spelling: James Judge
# >>> license and agreement data here <<<

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


ui = True
ui_s = False

while True:
    if ui:
        if not ui_s:
            ui_s = socket.socket()
            ui_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if os.path.exists("rdisc.py"):
                ui_s.bind(("127.0.0.1", 8078))
            else:
                ui_s.bind(("127.0.0.1", 8079))
            print(" -> Launching ui.exe")
            if not os.path.isfile("ui.exe"):
                input("[!] CRITICAL FILE ui.exe MISSING, hit enter to fall back to CLI\n")
                ui = False
            else:
                os.startfile("ui.exe")
                print(" <- ui.exe launched")
                ui_s.listen()
                cs, client_address = ui_s.accept()

                def to_c(text, delay=None):
                    if delay:
                        time.sleep(delay)
                    try:
                        cs.send(str(text).encode(encoding="utf-16"))
                    except ConnectionResetError:
                        exit.update("EXIT")
                print(f" Connected to ui.exe via socket {client_address}")
                to_c("\n🱫[COLOR][GRN] <- Internal socket connected\n", 0.1)
    if not ui:
        def to_c(text, delay=None):
            if delay:
                time.sleep(delay)
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

    if os.path.exists("version.txt"):
        with open("version.txt", encoding="utf-8") as f:
            version, tme, bld_num, run_num = f.read().split('🱫')
        version = f"{version} ❌"
        to_c(f"🱫[LODVS] {version}")

    default_salt = """52gy"J$&)6%0}fgYfm/%ino}PbJk$w<5~j'|+R .bJcSZ.H&3z'A:gip/jtW$6A=
                      G-;|&&rR81!BTElChN|+"TCM'CNJ+ws@ZQ~7[:¬`-OC8)JCTtI¬k<i#."H4tq)p4"""
    mac = enc.pass_to_seed(hex(uuid.getnode()), default_salt)

    def mac_enc(text):
        return enc.encrypt_key(text, mac, default_salt)

    def mac_dec(enc_text):
        return enc.decrypt_key(enc_text, mac, default_salt)

    def auth_txt_write(uid, dk, sk=None):
        auth_write = mac_enc(uid)+b"  "+mac_enc(dk)
        if sk:
            auth_write += b"  "+mac_enc(sk)
        with open("auth.txt", "wb") as auth_txt_:
            auth_txt_.write(auth_write)

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
                            n_pass_1 = enc.pass_to_seed(n_pass_1, default_salt)
                            break
                        else:
                            to_c("\n🱫[COLOR][RED] PASSWORDS DO NOT MATCH!")
                            n_pass_1 = None
                old_pass = enc.pass_to_seed(receive("\n🱫[COLOR][YEL] Enter old password"), default_salt)
                send_e(f"CPASS:{old_pass}🱫{n_pass_1}")
                print(f" >> CPASS:{old_pass}🱫{n_pass_1}")
                cng_pass_resp = recv_d(512)
                print(f" << {cng_pass_resp}")
                if cng_pass_resp == "VALID":
                    to_c("\n🱫[COLOR][GRN] Success! Password has been changed")
                else:
                    if cng_pass_resp == "SAME_PASS":
                        to_c("\n🱫[COLOR][RED] Old pass and new pass are the same, exiting password change")
                    else:
                        to_c("\n🱫[COLOR][RED] Old password incorrect, exiting password change")

            if output_.startswith('🱫[LOG]'):
                if user.key('u_name'):
                    if output_ == '🱫[LOG]':
                        try:
                            os.remove("auth.txt")
                        except FileNotFoundError:
                            pass
                        exit.update("LOGOUT")
                    if output_ == '🱫[LOG_A]':
                        send_e("LOG_A")
                        try:
                            os.remove("auth.txt")
                        except FileNotFoundError:
                            pass
                        exit.update("LOGOUT")
                    else:
                        to_c("\n🱫[COLOR][RED] You must be logged in to perform this action")

            if output_.startswith('🱫[DELAC]'):
                if user.key('u_name'):
                    print("Delete account")
                    pass__ = enc.pass_to_seed(receive("\n🱫[COLOR][YEL] Enter password to delete account"), default_salt)
                    send_e(f"DELAC:{pass__}")
                    print(f" >> DELAC:{pass__}")
                    if recv_d(512) == "VALID":
                        to_c("\n🱫[COLOR][GRN] A verification code has "
                             "been sent to your email (code valid for 15 minutes)")
                        while True:
                            to_c("\n🱫[COLOR][YEL] Enter 16 char code", 0.1)
                            email_code = ""
                            while len(email_code) != 16:
                                email_code = receive().replace("-", "").upper()
                            send_e(f"{email_code}")
                            print(f" >> {email_code}")
                            verify_dk_resp = recv_d(512)
                            if verify_dk_resp == "VALID":
                                print(" << VALID:ACCOUNT_DELETED")
                                to_c("\n🱫[COLOR][GRN] Request valid, account deleted")
                                try:
                                    os.remove("auth.txt")
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
                to_c(f"🱫[LODVS_E] {version}-{tme}-{bld_num}-{run_num}")
                return_value = False
            if output_ == '🱫[GET_VDATA]':
                to_c(f"🱫[LODVS] {version}")
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

        pub_key, pri_key = rsa.newkeys(1024)
        server_host = "26.29.111.99"
        server_port = 8080
        s = socket.socket()
        to_c("\n >> Connecting to server")
        while True:
            try:
                s.connect((server_host, server_port))
                to_c("\n🱫[COLOR][GRN] << Connected to server")
                break
            except ConnectionRefusedError:
                to_c("\n🱫[COLOR][RED] Could not connect to server")
                receive("🱫[INP SHOW]\n🱫[COLOR][YEL] Enter something to retry connection", 0.1)
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
        alpha, shift_seed = enc.seed_to_data(enc_seed)
        print(" << Client enc_seed and enc_salt received and loaded")
        to_c("\n🱫[COLOR][GRN] RSA -> enc bootstrap complete")

        def send_e(text):
            try:
                s.send(enc.encrypt("e", text, alpha, shift_seed, enc_salt))
            except ConnectionResetError:
                exit.update("CONNECTION_LOST")

        def recv_d(buf_lim):
            return enc.encrypt("d", s.recv(buf_lim), alpha, shift_seed, enc_salt)

        device_key = False
        if os.path.isfile("auth.txt"):
            with open("auth.txt", "rb") as auth_txt:
                auth_data = auth_txt.read().split(b"  ")
                if len(auth_data) > 1:
                    if not auth_data[0] == b"":
                        try:
                            user.update_key('uid', mac_dec(auth_data[0]))
                            print("LOADED UID")
                        except zlib.error:
                            pass
                        try:
                            device_key = mac_dec(auth_data[1])
                            print("LOADED DK")
                        except zlib.error:
                            pass
                if len(auth_data) > 2:
                    try:
                        user.update_key('sk', mac_dec(auth_data[2]))
                        print("LOADED SK")
                    except zlib.error:
                        pass

        def login():
            print("Login with session key")
            send_e(f"LOGIN:{user.key('uid')}🱫{user.key('sk')}")
            print(f" >> LOGIN:{user.key('uid')}🱫{user.key('sk')}")
            login_req_resp = recv_d(512)
            if login_req_resp.startswith("VALID:"):
                print(f" << {login_req_resp}")
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
                print(f" >> NEWSK:{user.key('uid')}🱫{enc.pass_to_seed(device_key, mac)}")
                dk_req_resp = recv_d(512)
                if dk_req_resp.startswith("VALID:"):
                    session_key = dk_req_resp[6:]
                    print(f" << VALID:{session_key}")
                    auth_txt_write(user.key('uid'), device_key, session_key)
                    user.update_key('sk', session_key)
                    if login():
                        break
                else:
                    if dk_req_resp == "SESSION_TAKEN":
                        to_c("\n🱫[COLOR][RED] User logged in on another device or multiple app instances open")
                        print(" << SESSION_TAKEN")
                        exit.update("SESSION_TAKEN")
                    else:
                        print(" << INVALID_DK")

            print("Create a new account or log in to an existing one")
            to_c("🱫[INP SHOW]🱫[MNINPLEN][256] ", 0.1)  # todo set len to 7?
            while True:
                to_c("Create a new account or log in to an existing one")
                login_signup = receive("\n🱫[COLOR][YEL] Type 'login' or 'sign up' or 'forgot' (password)", 0.1)
                if login_signup.lower().replace(" ", "") in ["login", "signup", "forgot"]:
                    break

            def enter_email():
                while True:
                    _email_ = receive("\n🱫[COLOR][YEL] Please enter email", 0.1).lower()
                    if "@" not in _email_:
                        to_c("\n🱫[COLOR][RED] Email does not contain an '@'")
                    else:
                        break
                return _email_

            def make_new_dk():
                print("Get a new device_key and session_key")
                device_key_ = enc.rand_b96_string(128)
                salted_dk = enc.pass_to_seed(device_key_, mac)
                to_c("\n🱫[COLOR][GRN] A verification code has "
                     f"been sent to '{email}' (code valid for 15 minutes)")
                while True:
                    to_c("\n🱫[COLOR][YEL] Enter 16 char code", 0.1)
                    email_code = ""
                    while len(email_code) != 16:
                        email_code = receive().replace("-", "").upper()
                    send_e(f"{email_code}🱫{salted_dk}")
                    print(f" >> {email_code}🱫{salted_dk}")
                    verify_dk_resp = recv_d(512)
                    if verify_dk_resp.startswith("VALID:"):
                        print(f" << {verify_dk_resp}")
                        break
                    else:
                        print(" << INVALID_CODE")
                        to_c("\n🱫[COLOR][RED] Invalid email code")
                uid, session_key_ = verify_dk_resp[6:].split("🱫")
                auth_txt_write(uid, device_key_, session_key_)
                user.update_key('sk', session_key_)
                user.update_key('uid', uid)

            if login_signup == "login":
                print("Login system")
                while True:
                    email = enter_email()
                    to_c("\n🱫[COLOR][YEL] Please enter your password", 0.1)
                    pass_ = enc.pass_to_seed(receive(), default_salt)
                    send_e(f"NEWDK:{email}🱫{pass_}")
                    print(f" >> NEWDK:{email}🱫{pass_}")
                    new_dk_resp = recv_d(64)
                    if new_dk_resp == "INVALID":
                        print(" << INVALID")
                        to_c("\n🱫[COLOR][RED] Email or password invalid")
                    else:
                        if new_dk_resp == "SESSION_TAKEN":
                            to_c("\n🱫[COLOR][RED] User logged in on another device or multiple app instances open")
                            print(" << SESSION_TAKEN")
                            exit.update("SESSION_TAKEN")
                        else:
                            print(" << VALID")
                            break
                make_new_dk()
            else:
                if login_signup == "signup":
                    print("Signup")
                    pass_ = None
                    while True:
                        email = enter_email()
                        while pass_ is None:
                            pass_1 = receive("\n🱫[COLOR][YEL] Please enter a password", 0.1)
                            if len(pass_1) < 8:
                                to_c("\n🱫[COLOR][RED] PASSWORD TO SHORT! (must be at least 8 chars)")
                            else:
                                to_c(f"\n Entered ({len(pass_1)}chrs): "+"*"*len(pass_1))
                                if pass_1 == receive("\n🱫[COLOR][YEL] Please re-enter password", 0.1):
                                    pass_ = enc.pass_to_seed(pass_1, default_salt)
                                    break
                                else:
                                    to_c("\n🱫[COLOR][RED] PASSWORDS DO NOT MATCH!")
                                    pass_ = None
                        send_e(f"NEWAC:{email}🱫{pass_}")
                        print(f" >> NEWAC:{email}🱫{pass_}")
                        new_ac_resp = recv_d(64)
                        if new_ac_resp == "INVALID_EMAIL":
                            print(" << INVALID_EMAIL")
                            to_c("\n🱫[COLOR][RED] Email was invalid, probably already taken")
                        else:
                            if new_ac_resp == "IP_CREATE_LIMIT":
                                to_c("\n🱫[COLOR][RED] This IP has already reached the creation limit of 2 accounts)")
                                break
                            else:
                                print(" << VALID")
                                make_new_dk()
                                to_c("\n🱫[COLOR][GRN] Account setup complete, logging in...")
                                print("Account setup complete, dk and sk received and saved")
                                break
                else:
                    print("Forgot password")
                    send_e(f"FGPAS:{enter_email()}")
                    if recv_d(64) == "INVALID_EMAIL":
                        print(" << INVALID_EMAIL")
                        to_c("\n🱫[COLOR][RED] Email invalid! No account was linked to this email")
                    else:
                        n_pass_1 = None
                        while n_pass_1 is None:
                            n_pass_1 = receive("\n🱫[COLOR][YEL] Please enter new password", 0.1)
                            if len(n_pass_1) < 8:
                                to_c("\n🱫[COLOR][RED] PASSWORD TO SHORT! (must be at least 8 chars)")
                            else:
                                to_c(f"\n Entered ({len(n_pass_1)}chrs): " + "*" * len(n_pass_1))
                                if n_pass_1 == receive("\n🱫[COLOR][YEL] Please re-enter password", 0.1):
                                    n_pass_1 = enc.pass_to_seed(n_pass_1, default_salt)
                                    break
                                else:
                                    to_c("\n🱫[COLOR][RED] PASSWORDS DO NOT MATCH!")
                                    n_pass_1 = None
                        to_c("\n🱫[COLOR][GRN] A verification code has "
                             "been sent to your email (code valid for 15 minutes)")
                        while True:
                            to_c("\n🱫[COLOR][YEL] Enter 16 char code", 0.1)
                            email_code = ""
                            while len(email_code) != 16:
                                email_code = receive().replace("-", "").upper()
                            send_e(f"{email_code}🱫{n_pass_1}")
                            print(f" >> {email_code}")
                            verify_dk_resp = recv_d(512)
                            if verify_dk_resp == "VALID":
                                print(" << VALID:PASS_CHANGE")
                                to_c("\n🱫[COLOR][GRN] Request valid, password changed")
                                break
                            else:
                                print(" << INVALID_CODE")
                                to_c("\n🱫[COLOR][RED] Invalid email code")

        print("Version updater")
        send_e(hashed)
        print(f" >> {hashed}")
        v_check_resp = recv_d(512)
        print(f" << {v_check_resp}")
        if v_check_resp.startswith("VALID:"):
            with open("version.txt", "w", encoding="utf-8") as f:
                f.write(v_check_resp[6:])
            version, tme, bld_num, run_num = v_check_resp[6:].split('🱫')
            version = f"{version} ✔"
            to_c(f"🱫[LODVS] {version}", 0.1)

        if v_check_resp.startswith("INVALID:"):
            version_up_info, update_size, update_hash = v_check_resp[8:].split("🱫")
            to_c(f"\n <> Updating rdisc {version_up_info} ({round(int(update_size)/1024/1024, 2)}MB)")
            exit.update("UPDATE")

        if v_check_resp.startswith("UNKNOWN:"):
            update_size, update_hash = v_check_resp[8:].split("🱫")
            to_c("\n🱫[COLOR][RED] <> INVALID OR CORRUPTED VERSION, downloading new copy")
            exit.update("UPDATE")

        to_c(f"\n🱫[COLOR][GRN] You are now logged in as {user.key('u_name')}")
        to_c("🱫[INP SHOW]🱫", 0.1)
        print("Logged in loop")
        while True:
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
                        if new_u_name_resp == "INVALID_NAME":
                            print(" << INVALID_NAME")
                            to_c("\n🱫[COLOR][RED] Username already taken")
                        else:
                            print(" << VALID")
                            to_c("\n🱫[COLOR][GRN] Username changed to "
                                 f"{new_u_name_resp[6:]} from {user.key('u_name')}")
                            user.update_key('u_name', new_u_name_resp[6:])
                    else:
                        to_c(f"\n🱫[COLOR][RED] Username must be 5-32 chars, you entered: {username[:64]}")

    except AssertionError:
        exit_reason = str(exit.get(0))[2:-2]
        if exit_reason == "SESSION_TAKEN":
            pass
        if exit_reason == "CONNECTION_LOST":
            print("SERVER CONNECTION LOST, RELOADING")
            to_c("\n🱫[COLOR][RED] Connection lost - Reloading")
            pass
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
            pass
        if exit_reason == "UPDATE":
            with open("Update.zip", "wb") as f:
                for i in range((int(update_size)//4096)+1):
                    bytes_read = s.recv(4096)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
                    #to_c(f"\n{round(i/((int(update_size)//4096)+1)*100, 2)}%")
            if enc.hash_a_file("Update.zip") == update_hash:
                to_c("🱫[EXIT]")
                time.sleep(0.5)
                os.startfile("updater.exe")
                break
            else:
                to_c("\n🱫[COLOR][RED] Update files corrupt")
                pass
        if exit_reason in ["RESTART", "EXIT"]:
            to_c("🱫[EXIT]")
            s.close()
        if exit_reason == "EXIT":
            break

# if cooldown.check(0) == "True":  # todo maybe stop input until allowed, bring back what was entered
#    s.send(enc.encrypt_key(client_send, user.key('df_key'), "salt"))
# else:
#    to_c(f"\nYOU'RE SENDING MESSAGES TOO FAST! please wait {checked}s~")
