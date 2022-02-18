import datetime, os, socket, rsa, uuid
from threading import Thread
from random import choice, randint
import enclib as enc


min_version = "V0.17.0.0"  # CHANGE MIN CLIENT REQ VERSION HERE

default_salt = """TO$X-YkP#XGl>>Nw@tt ~$c[{N-uF&#~+h#<84@W3 57dkX.V'1el~1JcyMTuRwjG
                  DxnI,ufxSNzdgJyQn<-Qj--.PN+y=Gk.F/(B'Fq+D@,$*9&[`Bt.W3i;0{UN7K="""


def version_info(hashed, user_id, cs):
    print(hashed, user_id)
    with open("sha.txt", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if hashed in line:
                version_data = line
            else:
                return "NOTREAL"
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
        return f"INVALID-{version}->{min_version}"
    else:
        if users.get(0, user_id[:64]):  # todo redo
            client_sockets.add(cs)
            print("Updated cs", client_sockets)
            return f"VALID-{version}-{tme}-{bld_num}-{run_num}"
        else:
            return f"NO_ACC_FND"


server_port = 8080
client_sockets = set()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', server_port))
s.listen(5)
print(f"[*] Listening as 0.0.0.0:{server_port}")


def client_connection(cs):
    ip, port = str(cs).split("raddr=")[1][2:-2].split("', ")
    print("Waiting for pub key from", ip, port)
    pub_key_cli = rsa.PublicKey.load_pkcs1(cs.recv(1024))
    enc_seed = enc.hex_gens(78)
    enc_salt = enc.hex_gens(32)
    cs.send(rsa.encrypt(enc_seed.encode(), pub_key_cli))
    cs.send(rsa.encrypt(enc_salt.encode(), pub_key_cli))
    alpha, shift_seed = enc.seed_to_data(enc_seed)
    while True:
        login_request = enc.encrypt("d", cs.recv(1024), alpha, shift_seed, enc_salt, "join_dec")

        # check for login, signup or session
        if login_request.startswith("NEWAC:"):
            email, password = login_request[6:].split("<|>")
            with open("users.txt", encoding="utf-8") as f:
                email_valid = True
                for user in f.readlines():
                    if email == user.split("🱫")[2]:
                        email_valid = False

            if not email_valid:
                cs.send(enc.encrypt("e", "INVALID_EMAIL", alpha, shift_seed, enc_salt))
            else:
                # email code and username still required
                # submit username after device_key and code

                # email code sending code will be below
                # add error return code for if email code sending fails
                email_code = "".join([choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for x in range(int(16))])
                email_code_send = f"{email_code[:4]}-{email_code[4:8]}-{email_code[8:12]}-{email_code[12:]}"
                print(email_code_send)
                #
                #code_valid_until = datetime.datetime.now()+datetime.timedelta(minutes=15)
                cs.send(enc.encrypt("e", f"VALID", alpha, shift_seed, enc_salt))
                while True:
                    create_verify = enc.encrypt("d", cs.recv(1024), alpha, shift_seed, enc_salt, "join_dec")
                    email_code_cli, device_key = create_verify.split("<|>")
                    print(create_verify)
                    if email_code == email_code_cli:
                        cs.send(enc.encrypt("e", f"VALID", alpha, shift_seed, enc_salt))
                        break
                    else:
                        cs.send(enc.encrypt("e", f"INVALID_CODE", alpha, shift_seed, enc_salt))

                while True:
                    username = enc.encrypt("d", cs.recv(1024), alpha, shift_seed, enc_salt, "join_dec")
                    user_valid = True
                    if len(username) > 32 or "#" in username:
                        print("reject")  # todo this will not be possible without client modification, flag
                        user_valid = False
                    # todo other char checks
                    else:
                        # todo proper all tag check, currently only allowing one user the ability to be called something
                        with open("users.txt", encoding="utf-8") as f:
                            for user in f.readlines():
                                username_, tag = user.split("🱫")[1].split("#")
                                if username_ == username:
                                    user_valid = False
                    if not user_valid:
                        cs.send(enc.encrypt("e", "INVALID_NAME", alpha, shift_seed, enc_salt))
                    else:
                        session_key = enc.pass_to_seed(enc.hex_gens(128), default_salt)
                        cs.send(enc.encrypt("e", session_key, alpha, shift_seed, enc_salt))
                        break
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
                password = enc.pass_to_seed(password, default_salt)
                tag = randint(1111, 9999)
                with open("users.txt", "a+", encoding="utf-8") as f:
                    f.write(f"{account_id}🱫{username}#{tag}🱫{email}🱫{password}🱫{device_key}🱫{ip}🱫{session_key}\n")



    input()
    # old code
    print(content)
    cs.send(enc.encrypt_key(version_info(content.split("🱫")[0][8:], content.split("🱫")[1], cs), default_key, "salt"))

    while True:
        try:
            content = cs.recv(1024)
        except ConnectionResetError:
            print(f"{cs} Disconnected")
            client_sockets.remove(cs)
            break
        actual_message = False
        try:
            print(content)
            content = enc.decrypt_key(content, default_key, "salt")
            actual_message = True
        except Exception as e:
            print("Could not decrypt_key", e)
            client_socket.close()

        if actual_message:
            process_code = content[:3]
            payload = content[3:]
            print(ip, port, process_code, payload)

            if process_code == "MSG":  # message post
                send = f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} " \
                          f"{ip}:{port}: {payload}"

            #if process_code == "CAN":  # change account name  # todo dup checks and reject to long
            #    users.change_name(0, content[:64], account_data[:32], payload)
            #    send = enc.encrypt_key(f"'{account_name}' changed name to '{payload}'", default_key)

            #if send:
            for client_socket in client_sockets:
                client_socket.send(enc.encrypt_key(send, default_key, "salt"))


while True:
    client_socket, client_address = s.accept()
    print("NEW CLIENT:", client_socket, client_address)
    t = Thread(target=client_connection, args=(client_socket,))
    t.daemon = True
    t.start()
