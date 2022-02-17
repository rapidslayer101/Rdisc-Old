import datetime, os, socket, rsa, uuid
from threading import Thread
import enclib as enc


min_version = "V0.17.0.0"  # CHANGE MIN CLIENT REQ VERSION HERE


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
            print(email, password)
            with open("users.txt", encoding="utf-8") as f:
                email_valid = True
                for user in f.readlines():
                    if email == user.split("🱫")[2]:
                        email_valid = False
            if email_valid:
                print("make account")
            else:
                print("flag email usage")


        input()
    # old code
    content = enc.decrypt_key(cs.recv(1024), default_key, "salt")
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
