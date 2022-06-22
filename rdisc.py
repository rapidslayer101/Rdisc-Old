import socket
from zlib import error as zl_error
from datetime import datetime
from os import path, remove, system
try:
    import rsa
except ModuleNotFoundError:
    system("pip install rsa")
    system("python launcher.py")
    exit()
try:
    from os import startfile
    ui = True
except ImportError:
    print("[!] os.startfile() failed to import")
    ui = False
from time import sleep
from hashlib import sha512
#from threading import Thread
import enclib as enc

# local sockets localhost:30677, localhost:30678
# Made by rapidslayer101 (Scott Bree), General usage testing and spelling: James Judge
# >>> license and agreement data here <<<

hashed = enc.hash_a_file("rdisc.py")
if path.exists("sha.txt"):
    with open("sha.txt", "r", encoding="utf-8") as f:
        latest_sha_, run_type_, version_, tme_, bld_num_, run_num_ = f.readlines()[-1].split("§")
    print("prev", run_type_, version_, tme_, bld_num_, run_num_)
    release_major, major, build, run = version_.replace("V", "").split(".")
    if latest_sha_ != hashed:
        run = int(run) + 1
        with open("sha.txt", "a+", encoding="utf-8") as f:
            write = f"\n{hashed}§RUN§V{release_major}.{major}.{build}.{run}" \
                    f"§TME-{str(datetime.now())[:-4].replace(' ', '_')}" \
                    f"§BLD_NM-{bld_num_[7:]}§RUN_NM-{int(run_num_[7:])+1}"
            print(f"crnt RUN V{release_major}.{major}.{build}.{run} "
                  f"TME-{str(datetime.now())[:-4].replace(' ', '_')} "
                  f"BLD_NM-{bld_num_[7:]} RUN_NM-{int(run_num_[7:])+1}")
            f.write(write)
    print(f"Running rdisc V{release_major}.{major}.{build}.{run}")

ui_s = False

while True:
    if ui:
        if not ui_s:
            ui_s = socket.socket()
            ui_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            ui_s.bind(("127.0.0.1", 30677))
            print(" -> Launching ui.exe")
            if not path.isfile("ui.exe"):
                print("[!] CRITICAL FILE ui.exe MISSING, falling back to CLI\n")
                ui = False
            else:
                try:
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
                            call_exit.update("EXIT")
                    print(f"Connected to ui.exe via socket {client_address}")
                    to_c("\n🱫[COL-GRN] <- Internal socket connected\n", 0.1)
                except NameError:
                    print("[!] ui.exe failed to launch")
                    ui = False
    if not ui:
        def to_c(text, delay=None):
            if delay:
                sleep(delay)
            if text.startswith("🱫[INP SHOW]🱫"):
                text = text[14:]
            if text.startswith("\n🱫[COL-GRN] "):  # todo CLI colors
                text = text[12:]
            if text.startswith("\n🱫[COL-YEL] "):
                text = text[12:]
            if text.startswith("\n🱫[COL-RED] "):
                text = text[12:]
            if text.startswith("[MNINPLEN][256] "):
                text = text[16:]
            if not text == "":
                print(text)

    if path.exists("version.txt"):
        with open("version.txt", encoding="utf-8") as f:
            version, tme, bld_num, run_num = f.read().split('🱫')
        version = f"{version} ❌"
        to_c(f"🱫[LODVS] {version}")

    default_salt = "52gy\"J$&)6%0}fgYfm/%ino}PbJk$w<5~j'|+R .bJcSZ.H&3z'A:gip/jtW$6A=" \
                   "G-;|&&rR81!BTElChN|+\"TCM'CNJ+ws@ZQ~7[:¬`-OC8)JCTtI¬k<i#.\"H4tq)p4"


    class CoolDown:
        def __init__(self):
            self.cool_down_data = {"x": (str(datetime.utcnow())), "msg_counter": 0}

        def check(self):
            last_msg_time = datetime.strptime(self.cool_down_data["x"], '%Y-%m-%d %H:%M:%S.%f')
            time_since_last = datetime.utcnow() - last_msg_time
            if time_since_last.seconds < 1:  # time between messages before counter adds 1
                self.cool_down_data.update({"msg_counter": self.cool_down_data["msg_counter"]+1})
            if time_since_last.seconds > 5:  # cooldown(s) when triggered
                self.cool_down_data.update({"msg_counter": 0})
            if self.cool_down_data["msg_counter"] > 10:  # total before counter triggers' cooldown(s)
                return round(5-time_since_last.seconds, 2)
            else:
                self.cool_down_data.update({"x": (str(datetime.utcnow()))})
                return "True"


    class Exit:
        def __init__(self):
            self.exit_reason = []

        def update(self, reason):
            self.exit_reason.append(reason)
            raise AssertionError


    cooldown = CoolDown()
    call_exit = Exit()

    try:
        def process_from_c(output_):
            return_value = True
            if output_ in ['🱫[RELOAD]', "-reload"]:
                call_exit.update("RELOAD")
            if output_ in ['🱫[QUIT]', "-quit"]:
                call_exit.update("EXIT")
            if output_ in ['🱫[UI]', '🱫[UIR]', '-ui', '-ui reload', '-restart']:
                if output_ in ['🱫[UI]', '-ui']:
                    call_exit.update("UI")
                if output_ in ['🱫[UIR]', '-ui reload', '-restart']:
                    call_exit.update("UIR")
            if output_.startswith('-change pass'):  # todo change UI trigger for this
                if "✔" in version:
                    print("Change password")
                    n_pass_1 = None
                    while n_pass_1 is None:
                        n_pass_1 = receive("\n🱫[COL-YEL] Please enter new password", 0.1)
                        if len(n_pass_1) < 8:
                            to_c("\n🱫[COL-RED] PASSWORD TO SHORT! (must be at least 8 chars)")
                            n_pass_1 = None
                        else:
                            to_c(f"\n Entered ({len(n_pass_1)}chrs): "+"*" * len(n_pass_1))
                            if n_pass_1 == receive("\n🱫[COL-YEL] Please re-enter password", 0.1):
                                n_pass_1 = enc.pass_to_key(n_pass_1, default_salt, 100000)
                                break
                            else:
                                to_c("\n🱫[COL-RED] PASSWORDS DO NOT MATCH!")
                                n_pass_1 = None
                    old_pass = enc.pass_to_key(receive("\n🱫[COL-YEL] Enter old password"), default_salt, 100000)
                    send_e(f"CPASS:{old_pass}🱫{n_pass_1}")
                    print(f" >> CPASS:{old_pass}🱫{n_pass_1}")
                    cng_pass_resp = recv_d(512)
                    print(f" << {cng_pass_resp}")
                    if cng_pass_resp == "V":
                        to_c("\n🱫[COL-GRN] Success! Password has been changed")
                    else:
                        if cng_pass_resp == "SP":
                            to_c("\n🱫[COL-RED] Old pass and new pass are the same, exiting password change")
                        else:
                            to_c("\n🱫[COL-RED] Old password incorrect, exiting password change")
                else:
                    to_c("\n🱫[COL-RED] You must be logged in to perform this action")

            if output_.startswith('-delete account'):  # todo change UI trigger for this
                if "✔" in version:
                    print("Delete account")
                    pass__ = enc.pass_to_key(receive("\n🱫[COL-YEL] Enter password to delete account"), default_salt, 100000)
                    send_e(f"DLAC:{pass__}")
                    print(" >> Password sent")
                    if recv_d(512) == "V":
                        while True:
                            to_c("\n🱫[COL-GRN] Password correct")
                            depth_ = int(recv_d(512))
                            print(f" << challenge_int received: {depth}")
                            user_challenge_ = sha512(enc.pass_to_key(pass_, key_salt, depth_).encode()).hexdigest()
                            send_e(user_challenge_)
                            print(" >> challenge_hash sent")
                            del_resp = recv_d(512)
                            if del_resp == "V":
                                to_c("\n🱫[COL-YEL] Request valid, type 'CONFIRM' to confirm deletion of account")
                                if receive() == "CONFIRM":
                                    send_e("Y")
                                    print(" >> CONFIRM_DELETION")
                                    if recv_d(512) == "V":
                                        print(" << ACCOUNT_DELETED")
                                        to_c(f"\n🱫[COL-GRN] ACCOUNT {uid} DELETED")
                                        # todo, here suggest app clean
                                        break
                                else:
                                    send_e("N")
                    else:
                        to_c("\n🱫[COL-RED] Password incorrect, exiting account deletion")
                else:
                    to_c("\n🱫[COL-RED] You must be logged in to perform this action")
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
                        call_exit.update("EXIT")
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

        print("Loading auth keys...")
        sign_up = False
        not_found_usb_error = False
        while True:
            if not not_found_usb_error:
                to_c("🱫[INP SHOW]🱫[MNINPLEN][256] ", 0.1)
            if not path.exists('key_location'):
                to_c("\n🱫[COL-YEL] Set 'Access USB Key' drive - Eg 'D:/'")
                while True:
                    key_location = receive()
                    if not path.exists(f'{key_location}key'):
                        to_c("\n🱫[COL-RED] This location does not contain a key file, please try again")
                    else:
                        with open(f'key_location', 'w', encoding="utf-8") as f:
                            f.write(key_location)
                        break
            else:
                with open('key_location', encoding="utf-8") as f:
                    key_location = f.read()
                try:
                    with open(f'{key_location}key', 'rb') as f:
                        key_data = f.read()
                    print(" - Key data loaded")
                    if path.exists(f'{key_location}key_salt'):
                        with open(f'{key_location}key_salt', encoding="utf-8") as f:
                            key_salt, uid = f.read().split("🱫")
                        print(" - Key salt loaded\n - User id loaded")
                    else:
                        to_c("\n Enter the activation key")
                        while True:
                            act_key = receive()
                            try:
                                sign_up_key = sha512(enc.dec_from_key(key_data, act_key).encode()).hexdigest()
                                break
                            except zl_error:
                                to_c("\n🱫[COL-RED] Invalid activation key")
                        to_c("\n🱫[COL-GRN] Key unlocked, validating hash with server")
                        sign_up = True
                    break
                except FileNotFoundError:
                    if not not_found_usb_error:
                        to_c("\n🱫[COL-RED] Key file not found, insert USB")
                    not_found_usb_error = True
                    sleep(0.2)

        # Establish connection to server

        print("Establishing connection to server")
        pub_key, pri_key = rsa.newkeys(1024)
        s = socket.socket()
        if path.exists('server_ip'):
            with open('server_ip', encoding="utf-8") as f:
                server_ip, server_port = f.read().split(":")
                server_port = int(server_port)
            to_c("\n\n >> Connecting to server")
            server_connect_error = False
            while True:
                try:
                    s.connect((server_ip, server_port))
                    to_c("\n🱫[COL-GRN] << Connected to server")
                    break
                except ConnectionRefusedError:
                    to_c("\n🱫[COL-RED] Could not connect to server")
                    if not server_connect_error:
                        to_c("\n🱫[COL-YEL] Enter something to retry connection", 0.1)
                    server_connect_error = True
                    receive("🱫[INP SHOW]", 0.1)
                    to_c("🱫[INP HIDE]", 0.1)
        else:
            to_c("\n🱫[COL-YEL] Enter server IP address and port (eg: 127.0.0.1:30678)")
            while True:
                try:
                    server_ip, server_port = receive().split(":")
                    server_port = int(server_port)
                except ValueError or NameError:
                    to_c("\n🱫[COL-RED] Invalid input")
                else:
                    if server_port < 1 or server_port > 65535:
                        to_c("\n🱫[COL-RED] Port number must be between 1 and 65535")
                    else:
                        try:
                            ip_1, ip_2, ip_3, ip_4 = server_ip.split(".")
                        except ValueError:
                            to_c("\n🱫[COL-RED] IP address must be in the format 'xxx.xxx.xxx.xxx'")
                        try:
                            if all(i.isdigit() and 0 <= int(i) <= 255 for i in [ip_1, ip_2, ip_3, ip_4]):
                                try:
                                    s = socket.socket()
                                    to_c("\n\n >> Connecting to server")
                                    print(server_ip, server_port)
                                    s.connect((str(server_ip), server_port))
                                    to_c("\n🱫[COL-GRN] << Connected to server")
                                    with open('server_ip', 'w', encoding="utf-8") as f:
                                        f.write(f'{server_ip}:{server_port}')
                                    break
                                except ConnectionRefusedError:
                                    to_c("\n🱫[COL-RED] Connection failed, enter another another IP address and port")
                            else:
                                to_c("\n🱫[COL-RED] IP address must have integers between 0 and 255")
                        except NameError:
                            to_c("\n🱫[COL-RED] IP address must be in the form of 'xxx.xxx.xxx.xxx'")

        l_ip, l_port = str(s).split("laddr=")[1].split("raddr=")[0][2:-3].split("', ")
        s_ip, s_port = str(s).split("raddr=")[1][2:-2].split("', ")
        print(f" << Server connected via {l_ip}:{l_port} -> {s_ip}:{s_port}")
        try:
            s.send(rsa.PublicKey.save_pkcs1(pub_key))
        except ConnectionResetError:
            call_exit.update("CONNECTION_LOST")
        print(" >> Public RSA key sent")
        enc_seed = rsa.decrypt(s.recv(128), pri_key).decode()
        enc_salt = rsa.decrypt(s.recv(128), pri_key).decode()
        enc_key = enc.pass_to_key(enc_seed, enc_salt, 100000)
        print(" << Client enc_seed and enc_salt received and loaded")
        to_c("\n🱫[COL-GRN] RSA Enc bootstrap complete\n")

        def send_e(text):
            try:
                s.send(enc.enc_from_key(text, enc_key))
            except ConnectionResetError:
                call_exit.update("CONNECTION_LOST")

        def recv_d(buf_lim):
            try:
                return enc.dec_from_key(s.recv(buf_lim), enc_key)
            except ConnectionResetError:
                call_exit.update("CONNECTION_LOST")

        # Login system

        if sign_up:
            print("Create a new account")
            send_e(f"NAC:{sign_up_key}")
            print(" >> Sign up key sent")
            nac_resp = recv_d(512)
            if nac_resp == "N":
                print(" << Invalid signup hash")
                to_c("\n🱫[COL-RED] Invalid activation key")
                remove("key_location")
                call_exit.update("INVALID_SIGNUP_HASH")
            else:
                key_salt = nac_resp[2:]
                print(" << Valid signup hash: Key salt received")
                to_c("\n🱫[COL-GRN] Activation key validated")
                pass_ = None
                while pass_ is None:
                    pass_1 = receive("\n🱫[COL-YEL] Please enter a password", 0.1)
                    if len(pass_1) < 8:
                        to_c("\n🱫[COL-RED] PASSWORD TO SHORT! (must be at least 8 chars)")
                    else:
                        to_c(f"\n Entered ({len(pass_1)}chrs): " + "*" * len(pass_1))
                        if pass_1 == receive("\n🱫[COL-YEL] Please re-enter password", 0.1):
                            pass_ = enc.pass_to_key(pass_1, default_salt, 100000)
                            break
                        else:
                            to_c("\n🱫[COL-RED] PASSWORDS DO NOT MATCH!")
                            pass_ = None
                send_e(pass_)
                print(" >> Password sent")
                depth = int(recv_d(512))
                print(f" << challenge_int received: {depth}")
                user_challenge = sha512(enc.pass_to_key(pass_, key_salt, depth).encode()).hexdigest()
                send_e(user_challenge)
                print(" >> challenge_hash sent")
                uid = recv_d(512)
                if uid != "N":
                    print(f" << received user_id: {uid}")
                    to_c(f"\n🱫[COL-GRN] User authenticated, account '{uid}' created successfully")
                else:
                    print(" << AUTH_FAILED")
                    to_c("\n🱫[COL-RED] User authentication failed")
                    call_exit.update("AUTH_FAILED")
                with open(f'{key_location}key_salt', 'w', encoding="utf-8") as f:
                    f.write(key_salt+"🱫"+uid)
                print("Wrote key_salt and uid")
        else:
            print("Login with existing account")
            send_e(f"LOG:{uid}")
            print(" >> uid sent")
            while True:
                depth = recv_d(512)
                if depth == "N":
                    print(" << INVALID_UID")
                    to_c("\n🱫[COL-RED] User does not exist")
                else:
                    if depth == "SESH_T":
                        print(" << SESSION_TAKEN")
                        to_c("\n🱫[COL-RED] This account or IP is already logged in")
                        call_exit.update("SESH_TAKEN")
                    else:
                        print(f" << challenge_int received: {depth}")
                        pass_ = receive("\n🱫[COL-YEL] Please enter your password", 0.1)
                        pass_ = enc.pass_to_key(pass_, default_salt, 100000)
                        user_challenge = sha512(enc.pass_to_key(pass_, key_salt, int(depth)).encode()).hexdigest()
                        send_e(user_challenge)
                        print(" >> challenge_hash sent")
                        challenge_resp = recv_d(512)
                        if challenge_resp != "N":
                            print(" << logged in")
                            break
                        else:
                            print(" << AUTH_FAILED")
                            to_c("\n🱫[COL-RED] User authentication failed")

        print("Version updater")
        send_e(hashed)
        print(f" >> sent version hash")
        v_check_resp = recv_d(512)
        print(f" << {v_check_resp}")
        if v_check_resp.startswith("V"):
            with open("version.txt", "w", encoding="utf-8") as f:
                f.write(v_check_resp[1:])
            version, tme, bld_num, run_num = v_check_resp[1:].split('🱫')
            version = f"{version} ✔"
            to_c(f"🱫[LODVS] {version}", 0.1)

        if v_check_resp.startswith("N"):
            version, update_size, update_hash = v_check_resp[1:].split("🱫")
            to_c(f"\n <> Updating rdisc {version} - ({round(int(update_size)/1024/1024, 2)}MB)")
            call_exit.update("UPDATE")

        if v_check_resp.startswith("UNKNOWN"):
            to_c("\n🱫[COL-RED] <> MODIFIED VERSION DETECTED")

        to_c(f"\n🱫[COL-GRN] You are now logged in as {uid}")
        to_c("🱫[INP SHOW]🱫", 0.1)
        print("Logged in loop")

        #def server_loop():
        #    while True:
        #        server_msg = s.recv(512).decode()
        #        if server_msg.startswith("UON:"):
        #            print(server_msg[4:])
        #            print(server_msg)
        #            to_c(server_msg)

        #t = Thread(target=server_loop())
        #t.daemon = True
        #t.start()

        while True:
            # user data loading
            request = receive()
            #if request.startswith("-change name"):
            #    username = request[13:].replace("#", "").replace(" ", "")
            #    if username == user.key('u_name')[:-5]:
            #        to_c("\n🱫[COL-RED] Username cannot be the same as previous username")
            #    else:
            #        if 4 < len(username) < 33:
            #            send_e(f"CUSRN:{username}")
            #            print(f" >> CUSRN:{username}")
            #            new_u_name_resp = recv_d(128)
            #            if new_u_name_resp == "N_NAME":
            #                print(" << INVALID_NAME")
            #                to_c("\n🱫[COL-RED] Username already taken")
            #            else:
            #                print(" << VALID")
            #                to_c("\n🱫[COL-GRN] Username changed to "
            #                     f"{new_u_name_resp[1:]} from {user.key('u_name')}")
            #                user.update_key('u_name', new_u_name_resp[1:])
            #        else:
            #            to_c(f"\n🱫[COL-RED] Username must be 5-32 chars, you entered: {username[:64]}")

    except AssertionError:
        exit_reason = str(call_exit.exit_reason)[2:-2]
        if exit_reason == "SESH_TAKEN":
            to_c("🱫[INP SHOW]", 0.1)
            receive("\n🱫[COL-YEL] Enter something to retry connection", 0.)
            to_c("🱫[INP HIDE]", 0.1)
            exit_reason = "RELOAD"
        if exit_reason == "CONNECTION_LOST":
            print("SERVER CONNECTION LOST, RELOADING")
            to_c("🱫[CLRO]")
            to_c("\n🱫[COL-RED] Connection lost - Reloading")
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
            to_c("\n🱫[COL-GRN] -- Reloading --", 0.1)
        if exit_reason in ["RESTART", "EXIT"]:
            to_c("🱫[EXIT]")
            s.close()
        if exit_reason == "EXIT":
            break

# if cooldown.check(0) == "True":  # todo maybe stop input until allowed, bring back what was entered
#    s.send(enc.encrypt_key(client_send, user.key('df_key'), "salt"))
# else:
#    to_c(f"\nYOU'RE SENDING MESSAGES TOO FAST! please wait {checked}s~")
