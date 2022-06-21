import zlib, socket, rsa
from os import path, mkdir, listdir, remove, removedirs, rename
from threading import Thread
from random import choice, choices, randint
from hashlib import sha512
import enclib as enc

min_version = "V0.35.6.0"  # CHANGE MIN CLIENT REQ VERSION HERE
stable_release_zip = f"rdisc.zip"
update_size = path.getsize(stable_release_zip)
updater_size = path.getsize("updater.exe")
update_hash = enc.hash_a_file(stable_release_zip)
default_salt = "52gy\"J$&)6%0}fgYfm/%ino}PbJk$w<5~j'|+R .bJcSZ.H&3z'A:gip/jtW$6A=" \
                "G-;|&&rR81!BTElChN|+\"TCM'CNJ+ws@ZQ~7[:¬`-OC8)JCTtI¬k<i#.\"H4tq)p4"
b36set = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
b62set = b36set+"abcdefghijklmnopqrstuvwxyz"


def version_info(hashed):
    if hashed == "UPD":
        return "UPD"
    print(hashed)
    version_data = None
    with open("sha.txt", encoding="utf-8") as f:
        for _hash_ in f.readlines():
            if hashed in _hash_:
                version_data = line
    if not version_data:
        return f"UNKNOWN{update_size}🱫{update_hash}"
    version_, tme_, bld_num, run_num = version_data.split("§")[2:]
    release_major, major, build, run = version_.replace("V", "").split(".")
    req_release_major, req_major, req_build, req_run = min_version.replace("V", "").split(".")
    valid_version = False
    if int(release_major) > int(req_release_major)-1:
        if int(major) > int(req_major):
            valid_version = True
        else:
            if int(major) > int(req_major)-1:
                if int(build) > int(req_build)-1:
                    if int(run) > int(req_run)-1:
                        valid_version = True
    if not valid_version:
        return f"N{version_}🱫{update_size}🱫{update_hash}"
    else:
        return f"V{version_}🱫{tme_}🱫{bld_num}🱫{run_num}"


validation_hashes = []
if not path.exists("validation_keys.txt"):
    with open("validation_keys.txt", "w", encoding="utf-8") as f:
        f.write("")
else:
    with open("validation_keys.txt", encoding="utf-8") as f:
        for line in f.readlines():
            validation_hashes.append(line.split("🱫")[1])

if not path.exists("Users"):
    mkdir("Users")

u_ids, logged_in_users, sockets = [[], [], []]

for user_id_ in listdir("Users"):
    u_ids.append(user_id_)


class users:
    def ids(self):
        return u_ids

    def ids_update(self):
        u_ids.append(self)
        u_ids.sort()

    def logged_in(self):
        return logged_in_users

    def login(self, ip, cs):
        logged_in_users.append(self)
        logged_in_users.append(ip)
        sockets.append(cs)
        #time.sleep(0.5)
        #for i in sockets:
        #    i.send(f"UON:{self}".encode())

    def logout(self, ip, cs):
        try:
            logged_in_users.pop(logged_in_users.index(self))
            logged_in_users.pop(logged_in_users.index(ip))
            sockets.pop(sockets.index(cs))
        except ValueError:
            pass


client_sockets = set()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 8080))
s.listen()
print(f"[*] Listening as {str(s).split('laddr=')[1][:-1]}")


def client_connection(cs):
    try:
        ip, port = str(cs).split("raddr=")[1][2:-2].split("', ")
        print(f"NEW CLIENT-{ip}:{port}")
        uid = None
        try:
            pub_key_cli = rsa.PublicKey.load_pkcs1(cs.recv(256))
        except ValueError:
            raise AssertionError
        enc_seed, enc_salt= enc.rand_b96_str(48), enc.rand_b96_str(48)
        cs.send(rsa.encrypt(enc_seed.encode(), pub_key_cli))
        cs.send(rsa.encrypt(enc_salt.encode(), pub_key_cli))
        enc_key = enc.pass_to_key(enc_seed, enc_salt, 100000)

        def send_e(text):
            try:
                cs.send(enc.enc_from_key(text, enc_key))
            except zlib.error:
                raise ConnectionResetError

        def recv_d(buf_lim):
            try:
                return enc.dec_from_key(cs.recv(buf_lim), enc_key)
            except zlib.error:
                raise ConnectionResetError

        def check_logged_in(uid_):
            l_users = users.logged_in(0)
            if uid_ in l_users:
                return True
            else:
                if ip in l_users:
                    return True
                else:
                    return False

        while True:
            login_request = recv_d(1024)
            print(login_request)  # temp debug for dev

            if login_request.startswith("NAC:"):
                if login_request[4:] in validation_hashes:
                    user_salt = enc.rand_b96_str(64)
                    send_e(f"V:{user_salt}")
                    user_pass = recv_d(2048)
                    challenge_int = randint(1, 999999)
                    challenge_hash = sha512(enc.pass_to_key(user_pass, user_salt, challenge_int).encode()).hexdigest()
                    send_e(f"{challenge_int}")
                    user_challenge = recv_d(2048)
                    if user_challenge == challenge_hash:
                        while True:
                            u_id = "".join(choices(b36set, k=8))
                            if u_id not in users.ids(0):
                                break
                        mkdir(f"Users/{u_id}")
                        with open(f"Users/{u_id}/{u_id}-keys.txt", "w", encoding="utf-8") as f:
                            f.write(f"{user_pass}🱫{user_salt}")
                            #f.write(f"{user_pass}🱫{user_salt}🱫{ip}")
                        users.ids_update(u_id)
                        users.login(uid, ip, cs)
                        send_e(f"{u_id}")
                    else:
                        send_e("N")
                else:
                    send_e("N")

            if login_request.startswith("LOG:"):
                uid = login_request[4:]
                if check_logged_in(uid):
                    send_e("SESH_T")
                    raise ConnectionRefusedError
                else:
                    try:
                        users.ids(0).index(uid)
                    except ValueError:
                        send_e("N")  # User ID not found
                    else:
                        with open(f"Users/{uid}/{uid}-keys.txt", "r", encoding="utf-8") as f:
                            u_pass, u_salt = f.read().split("🱫")
                        while True:
                            challenge_int = randint(1, 999999)
                            challenge_hash = sha512(enc.pass_to_key(u_pass, u_salt, challenge_int).encode()).hexdigest()
                            send_e(f"{challenge_int}")
                            user_challenge = recv_d(2048)
                            if user_challenge != challenge_hash:
                                send_e("N")
                            else:
                                break
                        send_e("V")
                        while True:
                            version_response = version_info(recv_d(512))
                            if version_response == "UPD":
                                send_e(str(updater_size))
                                with open("updater.exe", "rb") as f:
                                    while True:
                                        bytes_read = f.read(4096)
                                        if not bytes_read:
                                            break
                                        cs.sendall(bytes_read)
                                raise ConnectionResetError
                            else:
                                break
                        send_e(version_response)
                        if not version_response.startswith("V"):
                            with open(stable_release_zip, "rb") as f:
                                while True:
                                    bytes_read = f.read(4096)
                                    if not bytes_read:
                                        break
                                    cs.sendall(bytes_read)
                            raise ConnectionResetError
                        users.login(uid, ip, cs)
                        break

        print(f"{uid} logged in with IP-{ip}:{port} and version-{version_response}")
        while True:  # main loop
            request = recv_d(1024)
            print(request)  # temp debug for dev

            # logout causing requests
            if request.startswith("LOG_A"):
                with open(f"Users/{u_dir}/{uid}-keys.txt", encoding="utf-8") as f:
                    log_a_write = f.readlines()[0]
                with open(f"Users/{u_dir}/{uid}-keys.txt", "w", encoding="utf-8") as f:
                    f.write(log_a_write)
                raise ConnectionResetError

            if request.startswith("DELAC:"):
                password = enc.pass_to_seed(request[6:], default_salt)
                u_dir = users.dirs(0)[uid]
                u_dir = f"{uid} {u_dir[0]} {u_dir[1]}"
                pass_present = False
                with open(f"Users/{u_dir}/{uid}-keys.txt", encoding="utf-8") as f:
                    if password == f.readlines()[0].replace("\n", ""):
                        pass_present = True
                if pass_present:
                    send_e("V")
                    # email code sending code will be below
                    # add error return code for if email code sending fails
                    email_code = "".join([choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for x in range(16)])
                    email_code_send = f"{email_code[:4]}-{email_code[4:8]}-{email_code[8:12]}-{email_code[12:]}"
                    print(email_code_send)
                    #
                    # code_valid_until = datetime.datetime.now()+datetime.timedelta(minutes=15)
                    while True:
                        if email_code == recv_d(1024):
                            for file in listdir(f"Users/{u_dir}"):
                                remove(f"Users/{u_dir}/{file}")
                            removedirs(f"Users/{u_dir}")
                            print(f"{u_dir} deleted")
                            send_e("V")
                            raise ConnectionResetError
                        else:
                            send_e("N_CODE")
                else:
                    send_e("N_PASS")

            if request.startswith("CPASS:"):
                try:
                    old_pass, new_pass = request[6:].split("🱫")
                except ValueError:
                    raise AssertionError
                if old_pass == new_pass:
                    send_e("SP")  # old pass and new pass the same
                else:
                    pass_correct = False
                    u_dir = users.dirs(0)[uid]
                    u_dir = f"{uid} {u_dir[0]} {u_dir[1]}"
                    with open(f"Users/{u_dir}/{uid}-keys.txt", encoding="utf-8") as f:
                        lines = f.readlines()
                        if enc.pass_to_seed(old_pass, default_salt) == lines[0].replace("\n", ""):
                            lines[0] = enc.pass_to_seed(new_pass, default_salt)
                            pass_correct = True
                    if not pass_correct:
                        send_e("N")  # password wrong
                    else:
                        with open(f"Users/{u_dir}/{uid}-keys.txt", "w", encoding="utf-8") as f:
                            for line in lines:
                                f.write(line.replace("\n", "")+"\n")
                        send_e("V")

            if request.startswith("CUSRN:"):
                u_name = request[6:]
                u_dir = users.dirs(0)[uid]
                u_dir = f"{uid} {u_dir[0]} {u_dir[1]}"
                if not 4 < len(u_name) < 33:
                    raise AssertionError
                if "#" in u_name or " " in u_name:
                    raise AssertionError
                if u_name == u_dir.split(" ")[2][:-5]:
                    raise AssertionError

                # todo check amount of username changes here

                u_name = f"{u_name}#{randint(1111, 9999)}"
                if u_name not in users.names(0):
                    user_dir_new = f"{uid} {u_dir.split(' ')[1]} {u_name}"
                    rename(f"Users/{u_dir}", f"Users/{user_dir_new}")
                    users.dirs_update(uid, u_dir.split(' ')[1], u_name)
                    users.names_remove(users.names(0).index(u_dir.split(" ")[2]))
                    users.names_update(u_name)
                    # todo update amount of username changes here
                    send_e(f"V{u_name}")
                else:
                    send_e("N_NAME")

            if request.startswith("ADDFR:"):
                add_friend_n = request[6:]
                if 9 < len(add_friend_n) < 38:
                    try:
                        int(add_friend_n[-4:])
                        if add_friend_n[-5] != "#":
                            raise AssertionError
                        else:
                            print("process new friend")
                            print(add_friend_n)
                    except ValueError:
                        raise AssertionError
                else:
                    raise AssertionError

    except ConnectionResetError:
        print(f"{uid}-{ip}:{port} DC")
        users.logout(uid, ip, cs)
    except ConnectionRefusedError:
        print(f"{uid}-{ip}:{port} DC - 1 session limit")
    except AssertionError:
        print(f"{uid}-{ip}:{port} DC - modified/invalid client request")
        users.logout(uid, ip, cs)


while True:
    client_socket, client_address = s.accept()
    t = Thread(target=client_connection, args=(client_socket,))
    t.daemon = True
    t.start()
