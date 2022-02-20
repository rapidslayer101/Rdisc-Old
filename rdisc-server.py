import socket, rsa
from threading import Thread
from random import choice, randint
import enclib as enc


min_version = "V0.20.0.0"  # CHANGE MIN CLIENT REQ VERSION HERE

default_salt = """TO$X-YkP#XGl>>Nw@tt ~$c[{N-uF&#~+h#<84@W3 57dkX.V'1el~1JcyMTuRwjG
                  DxnI,ufxSNzdgJyQn<-Qj--.PN+y=Gk.F/(B'Fq+D@,$*9&[`Bt.W3i;0{UN7K="""


def version_info(hashed):
    version_data = None
    with open("sha.txt", encoding="utf-8") as f:
        for line in f.readlines():
            if hashed in line:
                version_data = line
    if not version_data:
        return "UNKNOWN"
    latest_sha, type, version, tme, bld_num, run_num = version_data.split("§")
    print(latest_sha, type, version, tme, bld_num, run_num)
    release_major, major, build, run = version.replace("V", "").split(".")
    req_release_major, req_major, req_build, req_run = min_version.replace("V", "").split(".")
    valid_version = False
    if int(release_major) > int(req_release_major)-1:
        if int(major) > int(req_major)-1:
            if int(build) > int(req_build)-1:
                if int(run) > int(req_run)-1:
                    valid_version = True
                    print(f"{version} is valid for the {min_version} requirement")
    if not valid_version:
        return f"INVALID:{version}->{min_version}"
    else:
        return f"VALID:{version}🱫{tme}🱫{bld_num}🱫{run_num}"


server_port = 8080
client_sockets = set()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', server_port))
s.listen(5)
print(f"[*] Listening as 0.0.0.0:{server_port}")


def client_connection(cs):
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
        try:
            return enc.encrypt("d", cs.recv(1024), alpha, shift_seed, enc_salt)
        except ConnectionResetError:
            print(f"{cs} Disconnected")
            client_sockets.remove(cs)

    while True:
        login_request = recv_d()

        def make_new_dk():
            # email code and username still required
            # submit username after device_key and code

            # email code sending code will be below
            # add error return code for if email code sending fails
            email_code = "".join([choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for x in range(int(16))])
            email_code_send = f"{email_code[:4]}-{email_code[4:8]}-{email_code[8:12]}-{email_code[12:]}"
            print(email_code_send)
            #
            # code_valid_until = datetime.datetime.now()+datetime.timedelta(minutes=15)
            send_e("VALID")
            while True:
                email_code_cli, device_key_ = recv_d().split("🱫")
                if email_code == email_code_cli:
                    send_e("VALID")
                    break
                else:
                    send_e("INVALID_CODE")
            return device_key_

        # check for login, signup or session
        if login_request.startswith("NEWAC:"):
            email, password = login_request[6:].split("🱫")
            with open("users.txt", encoding="utf-8") as f:
                email_valid = True
                for user in f.readlines():
                    if email == user.split("🱫")[2]:
                        email_valid = False

            if not email_valid:
                send_e("INVALID_EMAIL")
            else:
                device_key = make_new_dk()
                print("create user account")
                while True:
                    account_id_valid = True
                    account_id = enc.hex_gens(8)
                    with open("users.txt", encoding="utf-8") as f:
                        for user in f.readlines():
                            account_id_ = user.split("🱫")[0]
                            if account_id_ == account_id:
                                account_id_valid = False
                    if account_id_valid:
                        break
                while True:
                    username_valid = True
                    username = enc.hex_gens(8)
                    with open("users.txt", encoding="utf-8") as f:
                        for user in f.readlines():
                            username_ = user.split("🱫")[1]
                            if username_ == username:
                                username_valid = False
                    if username_valid:
                        break
                password = enc.pass_to_seed(password, default_salt)
                tag = randint(1111, 9999)
                with open("users.txt", "a+", encoding="utf-8") as f:
                    f.write(f"{account_id}🱫{username}#{tag}🱫{email}🱫{password}🱫{device_key}🱫\n")

        if login_request.startswith("NEWDK:"):
            email, password = login_request[6:].split("🱫")
            password = enc.pass_to_seed(password, default_salt)
            email_valid = False
            line_counter = -1
            with open("users.txt", encoding="utf-8") as f:
                users = f.readlines()
                for user in users:
                    line_counter += 1
                    email_, password_ = user.split("🱫")[2:4]
                    if email_ == email:
                        if password_ == password:
                            udata = user.split("🱫")[:4]
                            old_data = f"{udata[0]}🱫{udata[1]}🱫{udata[2]}🱫{udata[3]}"
                            email_valid = True
            if not email_valid:
                send_e("INVALID")
            else:
                send_e("VALID")
                device_key = make_new_dk()
                users[line_counter] = f"{old_data}🱫{device_key}"
                with open("users.txt", "w", encoding="utf-8") as f:
                    for user in users:
                        f.write(user)

        if login_request.startswith("NEWSK:"):
            dk = login_request[6:]
            dk_valid = False
            line_counter = -1
            with open("users.txt", encoding="utf-8") as f:
                users = f.readlines()
                for user in users:
                    line_counter += 1
                    dk_ = user.split("🱫")[4]
                    if dk_ == dk:
                        session_key = enc.pass_to_seed(enc.hex_gens(128), default_salt)
                        udata = user.split("🱫")[:5]
                        old_data = f"{udata[0]}🱫{udata[1]}🱫{udata[2]}🱫{udata[3]}🱫{udata[4]}"
                        users[line_counter] = f"{old_data}🱫{ip}🱫{session_key}"
                        dk_valid = True

            if dk_valid:
                send_e(session_key)
                with open("users.txt", "w", encoding="utf-8") as f:
                    for user in users:
                        f.write(user)
            else:
                send_e("INVALID_DK")

        if login_request.startswith("LOGIN:"):
            sk = login_request[6:]
            login_valid = False
            with open("users.txt", encoding="utf-8") as f:
                for user in f.readlines():
                    user_id_, username_, email_, pass_, dk_, ip_, sk_ = user.split("🱫")
                    if ip_ == ip:
                        if sk_.replace("\n", "") == sk:
                            login_valid = True
                if login_valid:
                    send_e(f"VALID:{user_id_}🱫{username_}")  # todo validate user as logged in
                    break
                else:
                    send_e("INVALID_SK")

    print(f"{user_id_} logged in with IP:{ip}")
    request = recv_d()
    if request.startswith("VCHCK:"):
        version_response = version_info(request[6:])
        send_e(version_response)
        if not version_response.startswith("VALID:"):
            pass  # todo client connection close

    while True:  # main loop
        request = recv_d()
        if request.startswith("CUSRN:"):
            # todo username validation checks
            username_valid = True
            line_counter = -1
            with open("users.txt", encoding="utf-8") as f:
                users = f.readlines()
                for user in users:
                    line_counter += 1
                    username_ = user.split("🱫")[1]
                    ip_ = user.split("🱫")[5]
                    if ip_ == ip:
                        udata = user.split("🱫")
                        username = f"{request[6:]}#{randint(1111, 9999)}"
                        old_data = f"{udata[0]}🱫{username}🱫{udata[2]}🱫{udata[3]}🱫{udata[4]}🱫{udata[5]}🱫{udata[6]}"
                        users[line_counter] = old_data
                    if username_ == request[6:]:
                        username_valid = False
            if username_valid:
                send_e("VALID")
                with open("users.txt", "w", encoding="utf-8") as f:
                    for user in users:
                        f.write(user)
            else:
                send_e("INVALID_NAME")


while True:
    client_socket, client_address = s.accept()
    print("NEW CLIENT:", client_socket, client_address)
    t = Thread(target=client_connection, args=(client_socket,))
    t.daemon = True
    t.start()
