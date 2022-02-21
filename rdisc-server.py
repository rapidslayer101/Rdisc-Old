import socket, os, rsa
from threading import Thread
from random import choice, randint
import enclib as enc


min_version = "V0.22.0.0"  # CHANGE MIN CLIENT REQ VERSION HERE

default_salt = """TO$X-YkP#XGl>>Nw@tt ~$c[{N-uF&#~+h#<84@W3 57dkX.V'1el~1JcyMTuRwjG
                  DxnI,ufxSNzdgJyQn<-Qj--.PN+y=Gk.F/(B'Fq+D@,$*9&[`Bt.W3i;0{UN7K="""
b62set = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"


def version_info(hashed):
    version_data = None
    with open("sha.txt", encoding="utf-8") as f:
        for line in f.readlines():
            if hashed in line:
                version_data = line
    if not version_data:
        return "UNKNOWN"
    version_, tme_, bld_num, run_num = version_data.split("§")[2:]
    print(version_, tme_, bld_num, run_num)
    release_major, major, build, run = version_.replace("V", "").split(".")
    req_release_major, req_major, req_build, req_run = min_version.replace("V", "").split(".")
    valid_version = False
    if int(release_major) > int(req_release_major)-1:
        if int(major) > int(req_major)-1:
            if int(build) > int(req_build)-1:
                if int(run) > int(req_run)-1:
                    valid_version = True
                    print(f"{version_} is valid for the {min_version} requirement")
    if not valid_version:
        return f"INVALID:{version_}->{min_version}"
    else:
        return f"VALID:{version_}🱫{tme_}🱫{bld_num}🱫{run_num}"


if not os.path.exists("Users"):
    os.mkdir("Users")

user_dirs = {}
u_ids = []
u_emails = []
u_names = []

for user_dir in os.listdir("Users"):
    user_id_, email_, username_, = user_dir.split(" ")
    user_dirs.update({user_id_: [email_, username_]})
    u_ids.append(user_id_)
    u_emails.append(email_)
    u_names.append(username_)


class users:
    def dirs(self):
        return user_dirs

    def dirs_update(self, _email_, _username_):
        user_dirs.update({self: [_email_, _username_]})

    def ids(self):
        return u_ids

    def ids_update(self):
        u_ids.append(self)
        u_ids.sort()

    def names(self):
        return u_names

    def names_update(self):
        u_names.append(self)
        u_names.sort()

    def names_remove(self):
        u_names.pop(self)

    def emails(self):
        return u_emails

    def emails_update(self):
        u_emails.append(self)
        u_emails.sort()


server_port = 8080
client_sockets = set()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', server_port))
s.listen(5)
print(f"[*] Listening as 0.0.0.0:{server_port}")


def client_connection(cs):
    try:
        ip, port = str(cs).split("raddr=")[1][2:-2].split("', ")
        pub_key_cli = rsa.PublicKey.load_pkcs1(cs.recv(1024))
        enc_seed = enc.hex_gens(78)
        enc_salt = enc.hex_gens(32)
        cs.send(rsa.encrypt(enc_seed.encode(), pub_key_cli))
        cs.send(rsa.encrypt(enc_salt.encode(), pub_key_cli))
        alpha, shift_seed = enc.seed_to_data(enc_seed)

        def send_e(text):
            cs.send(enc.encrypt("e", text, alpha, shift_seed, enc_salt))

        def recv_d():
            return enc.encrypt("d", cs.recv(1024), alpha, shift_seed, enc_salt)

        def make_new_dk():
            # email code and username still required
            # submit username after device_key and code

            # email code sending code will be below
            # add error return code for if email code sending fails
            email_code = "".join([choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for x in range(16)])
            email_code_send = f"{email_code[:4]}-{email_code[4:8]}-{email_code[8:12]}-{email_code[12:]}"
            print(email_code_send)
            #
            # code_valid_until = datetime.datetime.now()+datetime.timedelta(minutes=15)
            while True:
                email_code_cli, device_key_ = recv_d().split("🱫")
                if email_code == email_code_cli:
                    session_key_ = enc.pass_to_seed(enc.hex_gens(128), default_salt)
                    break
                else:
                    send_e("INVALID_CODE")
            return device_key_, session_key_

        while True:
            login_request = recv_d()

            # check for login, signup or session
            if login_request.startswith("NEWAC:"):  # todo if email contains invalid chars reject
                email, password = login_request[6:].split("🱫")
                if email in users.emails(0):
                    send_e("INVALID_EMAIL")
                else:
                    send_e("VALID")
                    device_key, session_key = make_new_dk()
                    while True:
                        u_id = "".join([choice(b62set) for x in range(8)])
                        if u_id not in users.ids(0):
                            break
                    while True:  # todo tag support
                        username = "".join([choice(b62set) for x in range(8)])
                        username = f"{username}#{randint(1111, 9999)}"
                        if username not in users.names(0):
                            break
                    password = enc.pass_to_seed(password, default_salt)
                    os.mkdir(f"Users/{u_id} {email} {username}")
                    with open(f"Users/{u_id} {email} {username}/keys.txt", "w", encoding="utf-8") as f:
                        f.write(f"{password}🱫{device_key}🱫{ip}🱫{session_key}")
                    users.dirs_update(u_id, email, username)
                    users.ids_update(u_id)
                    users.emails_update(email)
                    users.names_update(username)
                    send_e(f"VALID:{u_id}🱫{session_key}")

            if login_request.startswith("NEWDK:"):
                email, password = login_request[6:].split("🱫")
                password = enc.pass_to_seed(password, default_salt)
                valid_email = False
                dirs = users.dirs(0)
                for dir_ in dirs:
                    if dirs[dir_][0] == email:
                        dir__ = dir_
                        username = dirs[dir_][1]
                        valid_email = True
                if not valid_email:
                    send_e("INVALID")  # email not found
                else:
                    pass_correct = False
                    u_dir = f"{dir__} {email} {username}"
                    with open(f"Users/{u_dir}/keys.txt", encoding="utf-8") as f:
                        pass_ = f.read().split("🱫")[0]
                        if password == pass_:
                            pass_correct = True
                    if not pass_correct:
                        send_e("INVALID")  # password wrong
                    else:
                        send_e("VALID")
                        device_key, session_key = make_new_dk()
                        with open(f"Users/{u_dir}/keys.txt", "w", encoding="utf-8") as f:
                            f.write(f"{pass_}🱫{device_key}🱫{ip}🱫{session_key}")
                        send_e(f"VALID:{dir__}🱫{session_key}")

            if login_request.startswith("NEWSK:"):
                uid, dk = login_request[6:].split("🱫")
                try:
                    u_dir = users.dirs(0)[uid]
                except KeyError:
                    send_e("INVALID_DK")  # User ID not found
                else:
                    u_dir = f"{uid} {u_dir[0]} {u_dir[1]}"
                    dk_valid = False
                    with open(f"Users/{u_dir}/keys.txt", encoding="utf-8") as f:
                        pass_, dk_ = f.read().split("🱫")[:2]
                        if dk == dk_:
                            dk_valid = True
                    if not dk_valid:
                        send_e("INVALID_DK")  # DK invalid
                    else:
                        session_key = enc.pass_to_seed(enc.hex_gens(128), default_salt)
                        with open(f"Users/{u_dir}/keys.txt", "w", encoding="utf-8") as f:
                            f.write(f"{pass_}🱫{dk_}🱫{ip}🱫{session_key}")
                        send_e(f"VALID:{session_key}")

            if login_request.startswith("LOGIN:"):
                uid, sk = login_request[6:].split("🱫")
                try:
                    u_dir = users.dirs(0)[uid]
                except KeyError:
                    send_e("INVALID_SK")  # User ID not found
                else:
                    u_dir = f"{uid} {u_dir[0]} {u_dir[1]}"
                    login_valid = False
                    with open(f"Users/{u_dir}/keys.txt", encoding="utf-8") as f:
                        ip_, sk_ = f.read().split("🱫")[2:]
                        if ip == ip_:
                            if sk.replace("\n", "") == sk_.replace("\n", ""):
                                login_valid = True
                    if not login_valid:
                        send_e("INVALID_SK")  # DK invalid
                    else:
                        send_e(f"VALID:{u_dir.split(' ')[2]}")  # todo validate user as logged in
                        break

        print(f"{uid} logged in with IP:{ip}")
        request = recv_d()
        if request.startswith("VCHCK:"):
            version_response = version_info(request[6:])
            send_e(version_response)
            if not version_response.startswith("VALID:"):
                raise AssertionError

        while True:  # main loop
            request = recv_d()
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

                u_name = f"{u_name}#{randint(1111, 9999)}"
                if u_name not in users.names(0):
                    user_dir_new = f"{uid} {u_dir.split(' ')[1]} {u_name}"
                    os.rename(f"Users/{u_dir}", f"Users/{user_dir_new}")
                    users.dirs_update(uid, u_dir.split(' ')[1], u_name)
                    users.names_remove(users.names(0).index(u_dir.split(" ")[2]))
                    users.names_update(u_name)
                    send_e(f"VALID:{u_name}")
                else:
                    send_e("INVALID_NAME")

    except ConnectionResetError:
        print(f"{uid}:{ip} DC")
    except AssertionError:
        print(f"{uid}:{ip} DC - modified client request")


while True:
    client_socket, client_address = s.accept()
    print("NEW CLIENT:", client_socket, client_address)
    t = Thread(target=client_connection, args=(client_socket,))
    t.daemon = True
    t.start()
