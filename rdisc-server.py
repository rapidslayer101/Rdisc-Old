import datetime, os, socket
from hashlib import sha512
from threading import Thread
import enclib as enc

min_version = "V0.14.0.0"  # CHANGE MIN CLIENT REQ VERSION HERE

block_size = 65536
hash_ = sha512()

if not os.path.exists("df.key"):
    with open("df.key", "w", encoding="utf-8") as f:
        for i in range(10):
            f.write(f"{enc.hex_gens(50)}\n")
default_key = enc.hash_a_file("df.key")


user_data = {}


class users:
    def reload(self):
        with open("users.txt", encoding="utf-8") as f:
            for line in f.readlines():
                line = line.replace("\n", "")
                ac_dt, account_name = line.split(', ')
                user_data.update({ac_dt[:64]: f"{ac_dt[64:]}-{account_name}"})
        print("reload", user_data)

    def get(self, userid):  # todo this could be reworked to return split up account data
        try:
            return user_data[str(userid)]
        except:
            return False

    def change_name(self, userid, filler, new_name):
        user_data.update({userid: f"{filler}-{new_name}"})
        with open("users.txt", "w", encoding="utf-8") as f:
            for item in user_data:
                item_p2, name = user_data[item].split("-")
                f.write(f"{item}{item_p2}, {name}\n")


users.reload(0)


def version_info(hashed, user_id, cs):
    print(hashed, user_id)
    real_version = False
    with open("sha.txt", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if hashed in line:
                real_version = True
                version_data = line
    if not real_version:
        return "NOTREAL"
    else:
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
            if users.get(0, user_id[:64]):
                #if enc.decrypt_key(user_id[64:], users.get(0, user_id[:64])[:32], "salt") == "at_ck":
                #if user_id[64:] == "at_ck":
                client_sockets.add(cs)
                print("Updated cs", client_sockets)
                return f"VALID-{version}-{tme}-{bld_num}-{run_num}"
            else:
                return f"NO_ACC_FND"


SERVER_PORT = 8080
client_sockets = set()
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', SERVER_PORT))
s.listen(5)
print(f"[*] Listening as 0.0.0.0:{SERVER_PORT}")


def client_connection(cs):
    ip, port = str(cs).split("raddr=")[1][2:-2].split("', ")
    print("Waiting for login data", ip)
    content = cs.recv(1024)
    print("CONT", content, default_key, "salt")
    content = enc.decrypt_key(content, default_key, "salt")
    print("login", content)
    version_response = version_info(content.split("🱫")[0][8:], content.split("🱫")[1], cs)
    cs.send(enc.encrypt_key(version_response, default_key, "salt"))

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
            #if users.get(0, content[:64]):
            #    account_data = users.get(0, content[:64])
            #    print(account_data[:32])
            #    override = b'R`*3\xd3\xff\xef\xbe\x1f\x17\xa4\xc8\x8dV\xb3\xcf<\xf3\xcf<'
                #content_without_id = enc.decrypt_key(content[64:].encode(), account_data[:32].encode(), "salt")
            #    content_without_id = enc.decrypt_key(content[64:].encode(), override, "salt")
            #    account_name = account_data[33:]
            #else:
            #    print("invalid message post attempted")

            #send = True
            process_code = content[:3]
            payload = content[3:]
            print(ip, port, process_code, payload)

            if process_code == "MSG":  # message post
                send = f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} " \
                          f"{ip}:{port}: {payload}"
                          #f"{account_name}: {payload}"
                #send = enc.encrypt_key(payload, default_key, "salt")

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
