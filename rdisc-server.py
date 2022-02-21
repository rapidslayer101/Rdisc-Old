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
user_dirs = os.listdir("Users")
user_id_list = []
user_emails = []
username_list = []
for user_dir__ in user_dirs:
    user_id_, user_email_, username_, = user_dir__.split(" ")
    user_id_list.append(user_id_)
    user_emails.append(user_email_)
    username_list.append(username_)


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

        while True:
            login_request = recv_d()

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

            # check for login, signup or session
            if login_request.startswith("NEWAC:"):  # todo if email contains invalid chars reject
                email, password = login_request[6:].split("🱫")
                if email in user_emails:
                    send_e("INVALID_EMAIL")
                else:
                    send_e("VALID")
                    device_key, session_key = make_new_dk()
                    print("create user account")
                    while True:
                        user_id = "".join([choice(b62set) for x in range(8)])
                        if user_id not in user_id_list:
                            break
                    while True:  # todo tag support
                        username = "".join([choice(b62set) for x in range(8)])
                        username = f"{username}#{randint(1111, 9999)}"
                        if username not in username_list:
                            break
                    password = enc.pass_to_seed(password, default_salt)
                    os.mkdir(f"Users/{user_id} {email} {username}")
                    user_dirs.append(f"{user_id} {email} {username}")
                    user_dirs.sort()  # todo test if this actually works
                    with open(f"Users/{user_id} {email} {username}/keys.txt", "w", encoding="utf-8") as f:
                        f.write(f"{password}🱫{device_key}🱫{ip}🱫{session_key}\n")
                    send_e(f"VALID:{user_id}🱫{session_key}")

            if login_request.startswith("NEWDK:"):
                email, password = login_request[6:].split("🱫")
                password = enc.pass_to_seed(password, default_salt)
                email_present = False
                for user_dir in user_dirs:
                    user_id_, user_email_, username_, = user_dir.split(" ")
                    if user_email_ == email:
                        user_dir_ = user_dir
                        user_id__ = user_id_
                        email_present = True
                if not email_present:
                    send_e("INVALID")  # email not found
                else:
                    pass_correct = False
                    with open(f"Users/{user_dir_}/keys.txt", encoding="utf-8") as f:
                        pass_ = f.read().split("🱫")[0]
                        if password == pass_:
                            pass_correct = True
                    if not pass_correct:
                        send_e("INVALID")  # password wrong
                    else:
                        send_e("VALID")
                        device_key, session_key = make_new_dk()
                        with open(f"Users/{user_dir_}/keys.txt", "w", encoding="utf-8") as f:
                            f.write(f"{pass_}🱫{device_key}🱫{ip}🱫{session_key}")
                        send_e(f"VALID:{user_id__}🱫{session_key}")

            if login_request.startswith("NEWSK:"):
                uid, dk = login_request[6:].split("🱫")
                uid_found = False
                for user_dir in user_dirs:
                    if uid == user_dir.split(" ")[0]:
                        user_dir_ = user_dir
                        uid_found = True
                if not uid_found:
                    send_e("INVALID_DK")  # User ID not found
                else:
                    dk_valid = False
                    with open(f"Users/{user_dir_}/keys.txt", encoding="utf-8") as f:
                        pass_, dk_ = f.read().split("🱫")[:2]
                        if dk == dk_:
                            dk_valid = True
                    if not dk_valid:
                        send_e("INVALID_DK")  # DK invalid
                    else:
                        session_key = enc.pass_to_seed(enc.hex_gens(128), default_salt)
                        with open(f"Users/{user_dir_}/keys.txt", "w", encoding="utf-8") as f:
                            f.write(f"{pass_}🱫{dk_}🱫{ip}🱫{session_key}")
                        send_e(f"VALID:{session_key}")

            if login_request.startswith("LOGIN:"):
                uid, sk = login_request[6:].split("🱫")
                uid_found = False
                for user_dir in user_dirs:
                    if uid == user_dir.split(" ")[0]:
                        user_dir_ = user_dir
                        uid_found = True
                if not uid_found:
                    send_e("INVALID_SK")  # User ID not found
                else:
                    login_valid = False
                    with open(f"Users/{user_dir_}/keys.txt", encoding="utf-8") as f:
                        ip_, sk_ = f.read().split("🱫")[2:]
                        if ip == ip_:
                            if sk == sk_:
                                login_valid = True
                    if not login_valid:
                        send_e("INVALID_SK")  # DK invalid
                    else:
                        send_e(f"VALID:{user_dir.split(' ')[2]}")  # todo validate user as logged in
                        break

        print(f"{uid} logged in with IP:{ip}")
        request = recv_d()
        if request.startswith("VCHCK:"):
            version_response = version_info(request[6:])
            send_e(version_response)
            if not version_response.startswith("VALID:"):
                raise AssertionError

        logged_username = user_dir.split(" ")[2]
        while True:  # main loop
            request = recv_d()
            if request.startswith("CUSRN:"):
                username = request[6:]
                if not 4 < len(username) < 33:
                    raise AssertionError
                if "#" in username or " " in username:
                    raise AssertionError
                if username == logged_username[:-5]:
                    raise AssertionError

                username = f"{username}#{randint(1111, 9999)}"
                if username not in username_list:
                    for user_dir in os.listdir("Users"):  # todo make a reload class in future
                        if uid == user_dir.split(" ")[0]:
                            user_dir_ = user_dir
                    user_dir_new = f"{uid} {user_dir_.split(' ')[1]} {username}"
                    os.rename(f"Users/{user_dir_}", f"Users/{user_dir_new}")
                    logged_username = username
                    send_e(f"VALID:{logged_username}")
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
