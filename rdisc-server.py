import datetime, os, time, socket
from hashlib import sha512, sha256
from threading import Thread
import enclib as enc

min_version = "V0.14.0.0"  # CHANGE MIN CLIENT REQ VERSION HERE

block_size = 65536
hash_ = sha512()

if not os.path.exists("df.key"):
    with open("df.key", "w", encoding="utf-8") as f:
        for i in range(10):
            f.write(f"{enc.hex_gens(50)}\n")
#with open("df.key", 'rb') as hash_file:
#    buf = hash_file.read(block_size)
#    while len(buf) > 0:
#        hash_.update(buf)
#        buf = hash_file.read(block_size)
default_key = enc.hash_a_file("df.key")


def get_server_key_from_file():
    with open("server_time_key.txt", "rb") as f:
        cur_ky_tm, old_ky = enc.decrypt_key(f.read(), default_key, "salt").split("§")
    return cur_ky_tm, old_ky, old_ky


def write_server_key_to_file(sver_key_tme, sver_tme_key):
    with open("server_time_key.txt", "wb") as f:
        f.write(enc.encrypt_key(f"{sver_key_tme}§{sver_tme_key}", default_key, "salt"))


if os.path.exists("server_time_key.txt"):
    date_format_str = '%Y-%m-%d %H:%M:%S'
    current_key_time, current_key, old_key = get_server_key_from_file()
    current_key_time = datetime.datetime.strptime(str(current_key_time), date_format_str)

    desired_time = enc.round_tme()+datetime.timedelta(seconds=30)
    curr_tme_fmt = datetime.datetime.strptime(str(current_key_time), date_format_str)
    diff = datetime.datetime.strptime(str(desired_time), date_format_str) - curr_tme_fmt
    iterations = int(diff.total_seconds()) / 30

    if iterations > 0:
        print(f"Updating time_key from {curr_tme_fmt}-->{desired_time} via {iterations} iterations")

    loop = 0
    while current_key_time != desired_time:
        loop += 1
        current_key = enc.pass_to_seed(str(current_key), str(current_key))
        current_key_time += datetime.timedelta(seconds=30)
        if loop % 20 == 0:
            print(loop, current_key_time, current_key)

    write_server_key_to_file(current_key_time, current_key)
    print("Key upto-date!")
else:
    current_key_time = enc.round_tme()
    current_key = enc.pass_to_seed(enc.hex_gens(64), enc.hex_gens(64))
    current_key_time += datetime.timedelta(seconds=30)
    print(f"Entry point 2: {current_key_time}={current_key}")
    write_server_key_to_file(current_key_time, current_key)


valid_time_keys = {"OLD": f"{current_key_time}={current_key}",
                   "CURRENT": f"{current_key_time}={current_key}",
                   "NEW": f"{current_key_time}={current_key}"}
print(valid_time_keys)
date_format_str = '%Y-%m-%d %H:%M:%S'
print()


class time_keys:
    def get(self):
        return valid_time_keys

    def add(self, time_key):
        valid_time_keys.update({"OLD": f"{valid_time_keys['CURRENT']}"})
        valid_time_keys.update({"CURRENT": f"{valid_time_keys['NEW']}"})
        valid_time_keys.update({"NEW": f"{time_key}"})


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


def update_server_time_key():
    while True:
        current_key_time, current_key, old_key = get_server_key_from_file()
        try:
            current_key_time = datetime.datetime.strptime(str(current_key_time), date_format_str)
            desired_time = enc.round_tme()+datetime.timedelta(seconds=30)
            curr_tme_fmt = datetime.datetime.strptime(str(current_key_time), date_format_str)
            diff = datetime.datetime.strptime(str(desired_time), date_format_str) - curr_tme_fmt
            iterations = int(diff.total_seconds()) / 30

            if iterations > 1:
                print("CRITICAL ERROR THIS SHOULD NOT HAVE OCCURED")

            while current_key_time != desired_time:
                current_key = enc.pass_to_seed(str(old_key), str(old_key))
                current_key_time += datetime.timedelta(seconds=30)

            if str(current_key) != str(old_key):
                print(f"{current_key_time}={current_key}")
                write_server_key_to_file(current_key_time, current_key)
                time_keys.add(0, current_key)
        except Exception as e:
            print("error", e)
        time.sleep(1)


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
                print(user_id[64:])
                #if enc.decrypt_key(user_id[64:], users.get(0, user_id[:64])[:32], "salt") == "at_ck":
                #if user_id[64:] == "at_ck":
                time_key_hashed = sha256(valid_time_keys['CURRENT'].encode()).hexdigest()
                client_sockets.add(cs)
                print("Updated cs", client_sockets)
                return f"VALID-{version}-{tme}-{bld_num}-{run_num}Ō{time_key_hashed}"
            else:
                return f"NO_ACC_FND"


t = Thread(target=update_server_time_key)
t.daemon = True
t.start()

SERVER_PORT = 8080
client_sockets = set()
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', SERVER_PORT))
s.listen(5)
print(f"[*] Listening as 0.0.0.0:{SERVER_PORT}")


def client_connection(cs):
    ip = str(cs).split("raddr=")[1]
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
            content = enc.decrypt_key(content, valid_time_keys['CURRENT'], "salt")
            actual_message = True
        except:
            try:
                content = enc.decrypt_key(content, valid_time_keys['OLD'], "salt")
                actual_message = True
            except:
                try:
                    content = enc.decrypt_key(content, valid_time_keys['NEW'], "salt")
                    actual_message = True
                except Exception as e:
                    print("Could not decrypt_key", e)

        if actual_message:
            if users.get(0, content[:64]):
                account_data = users.get(0, content[:64])
                content_without_id = enc.decrypt_key(content[64:], account_data[:32], "salt")
                account_name = account_data[33:]
            else:
                print("invalid message post attempted")

            send = True
            process_code = content_without_id[:3]
            payload = content_without_id[3:]
            print(ip, process_code, content)

            if process_code == "MSG":  # message post
                payload = f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} " \
                          f"{account_name}: {payload}"
                send = enc.encrypt_key(payload, valid_time_keys['CURRENT'])

            if process_code == "CAN":  # change account name  # todo dup checks and reject to long
                users.change_name(0, content[:64], account_data[:32], payload)
                send = enc.encrypt_key(f"'{account_name}' changed name to '{payload}'", valid_time_keys['CURRENT'])

            if send:
                for client_socket in client_sockets:
                    client_socket.send(enc.encrypt_key(send, default_key).encode())


while True:
    client_socket, client_address = s.accept()
    print("NEW CLIENT:", client_socket, client_address)
    t = Thread(target=client_connection, args=(client_socket,))
    t.daemon = True
    t.start()
