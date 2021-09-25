import discum, datetime, os, time, socket
from hashlib import sha512, sha256
from threading import Thread
import enclib as enc

bot = discum.Client(token="mfa.ZiR5m0U02bkR3mo_WkRdRbcVX-1zYxo1eGOdQI78"
                          "jiZFW1pHpY4M3nZUjpOgSF_aFYG43f9xtnR56wnrPdDo", log=False)

# V0.3.7.0 the first version with auto update
# V0.3.8.0 broke the first auto updater as the server system changed
# V0.3.10.0 is first version with working auto update
# V0.5.0.0 the first version with time_key and the standard_key
min_version = "V0.11.0.0"  # CHANGE MIN CLIENT REQ VERSION HERE


block_size = 65536
hash_ = sha512()
with open("df_key.txt", 'rb') as hash_file:
    buf = hash_file.read(block_size)
    while len(buf) > 0:
        hash_.update(buf)
        buf = hash_file.read(block_size)
default_key = hash_.hexdigest()


def get_server_key_from_file():
    with open("server_time_key.txt", encoding="utf-8") as f:
        cur_ky_tm, old_ky = enc.decrypt(f.read(), default_key).split("=")
    return cur_ky_tm, old_ky, old_ky


def write_server_key_to_file(sver_key_tme, sver_tme_key):
    with open("server_time_key.txt", "w", encoding="utf-8") as f:
        f.write(enc.encrypt(f"{sver_key_tme}={sver_tme_key}", default_key))


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
        current_key = enc.pass_to_seed(str(current_key))
        current_key_time += datetime.timedelta(seconds=30)
        if loop % 20 == 0:
            print(loop, current_key_time, current_key)

    write_server_key_to_file(current_key_time, current_key)
    print("Key upto-date!")
else:
    time_key_entry = input("Time_key entry point: ")
    current_key_time = enc.round_tme()()
    print(f"Entry point: {time_key_entry}={current_key_time}")
    current_key = enc.pass_to_seed(time_key_entry)
    current_key_time += datetime.timedelta(seconds=30)
    print(f"Entry point 2: {current_key_time}={current_key}")
    write_server_key_to_file(current_key_time, current_key)


valid_time_keys = {"OLD": "NO TIME KEY", "CURRENT": "NO TIME KEY", "NEW": "NO TIME KEY"}
print(valid_time_keys)
date_format_str = '%Y-%m-%d %H:%M:%S'


class time_keys():
    def get(self):
        return valid_time_keys

    def add(self, time_key):
        valid_time_keys.update({"OLD": f"{valid_time_keys['CURRENT']}"})
        valid_time_keys.update({"CURRENT": f"{valid_time_keys['NEW']}"})
        valid_time_keys.update({"NEW": f"{time_key}"})


user_data = {}


class users():
    def reload(self):
        with open("users.txt", encoding="utf-8") as f:
            for line in f.readlines():
                line = line.replace("\n", "")
                if len(line.split(", ")) == 3:
                    account_id, account_name, account_auth = line.split(", ")
                    user_data.update({account_id: f"ACCOUNT-{account_name}-{account_auth}"})
                else:
                    user_data.update({line.split(', ')[0]: "NEW_ACCOUNT"})
        print("reload", user_data)

    def get(self, userid):
        try:
            return user_data[str(userid)]
        except:
            return False


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

            loop = 0
            while current_key_time != desired_time:
                loop += 1
                current_key = enc.pass_to_seed(str(old_key))
                current_key_time += datetime.timedelta(seconds=30)

            if str(current_key) != str(old_key):
                print(f"{current_key_time}={current_key}")
                write_server_key_to_file(current_key_time, current_key)
                time_keys.add(0, current_key)
        except Exception as e:
            print("error", e)
        time.sleep(1)


def version_info(hashed, user_id=None, sign_up_name=None):
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
        latest_sha, type, version, tme, bld_num, run_num = version_data.split(" ")
        print(latest_sha, type, version, tme, bld_num, run_num)
        release_major, major, build, run = version.replace("V", "").split(".")
        req_release_major, req_major, req_build, req_run = min_version.replace("V", "").split(".")
        valid_version = False
        if int(release_major) > int(req_release_major) - 1:
            if int(major) > int(req_major) - 1:
                if int(build) > int(req_build) - 1:
                    if int(run) > int(req_run) - 1:
                        valid_version = True
                        print(f"{version} is valid for the {min_version} requirement")
        if not valid_version:
            return f"INVALID-{version}->{min_version}"
        else:
            if sign_up_name:
                print("AUTH SYSTEM WIP")
                print(sign_up_name, user_id)
                if users.get(0, user_id):
                    user_checks = users.get(0, user_id)
                    if user_checks.startswith("NEW_ACCOUNT"):
                        print("allowed")
                        auth_token = enc.hex_gens(32)
                        print("VALID BOT ACCOUNT", user_id, sign_up_name, auth_token)
                        lines = []
                        with open("users.txt", encoding="utf-8") as f:
                            for line in f.readlines():
                                if line.startswith(str(user_id)):
                                    lines.append(f"{user_id}, {sign_up_name}, {auth_token}")
                                else:
                                    lines.append(line)
                        with open("users.txt", "w", encoding="utf-8") as f:
                            to_write = ""
                            for item in lines:
                                to_write += item.replace("\n", "") + "\n"
                            f.write(to_write)

                        current_kt, current_key, old_key = get_server_key_from_file()
                        current_kt = datetime.datetime.strptime(str(current_kt), date_format_str)
                        users.reload(0)
                        return f"VALID-{version}-{tme}-{bld_num}-{run_num}Ō" \
                               f"{current_kt - datetime.timedelta(seconds=30)}={valid_time_keys['CURRENT']}" \
                               f"Ǘ{auth_token}"
                    else:
                        return "ACC_ALR_EXT"
                else:
                    return "ACC_CRT_NTA"
            else:
                if users.get(0, user_id):
                    time_key_hashed = sha256(valid_time_keys['CURRENT'].encode()).hexdigest()
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
    content = cs.recv(1024).decode()

    actual_message = False
    try:
        content = enc.decrypt(content, valid_time_keys['CURRENT'])
        actual_message = True
    except:
        try:
            content = enc.decrypt(content, default_key)
            print("login", content)
            if content[136:] == "":
                version_response = version_info(content[8:136], ip)
            else:
                version_response = version_info(content[8:136], ip, content[136:])
            cs.send(enc.encrypt(version_response, default_key).encode())
        except:
            try:
                content = enc.decrypt(content, valid_time_keys['OLD'])
                actual_message = True
            except:
                try:
                    content = enc.decrypt(content, valid_time_keys['NEW'])
                    actual_message = True
                except Exception as e:
                    print("Could not decrypt", e)

    if actual_message:
        print("actual message", ip, content)
        account_state, account_name, account_auth = users.get(0, ip).split("-")
        print(user_data)
        try:
            content = enc.decrypt(content, account_auth)
            content = f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')} " \
                      f"{account_name}: {content[3:]}"
            cs.send(enc.encrypt(enc.encrypt(content, valid_time_keys['CURRENT']), default_key))
        except:
            print("auth decrypt error")


while True:
    client_socket, client_address = s.accept()
    print("NEW CLIENT:", client_socket, client_address)
    global new_socket
    new_socket = client_socket
    t = Thread(target=client_connection, args=(client_socket,))
    t.daemon = True
    t.start()
