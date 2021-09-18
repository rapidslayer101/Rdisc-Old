import discum, datetime, os, time
from hashlib import sha512, sha256
from threading import Thread
import enclib as enc

bot = discum.Client(token="mfa.ZiR5m0U02bkR3mo_WkRdRbcVX-1zYxo1eGOdQI78"
                          "jiZFW1pHpY4M3nZUjpOgSF_aFYG43f9xtnR56wnrPdDo", log=False)

# V0.3.7.0 the first version with auto update
# V0.3.8.0 broke the first auto updater as the server system changed

# V0.3.10.0 is first version with working auto update
# V0.5.0.0 the first version with time_key and the standard_key
min_version = "V0.7.0.0"  # CHANGE MIN CLIENT REQ VERSION HERE


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


def version_info(hashed, bot_id=None, sign_up_name=None):
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
                        # user checks
                        valid_user = False
                        with open("users.txt", encoding="utf-8") as f:
                            for line in f.readlines():
                                print(str(bot_id), line.split(", ")[1])
                                if str(bot_id) == line.split(", ")[1]:
                                    valid_user = True

                        print(f"{version} is valid for the {min_version} requirement")
        if not valid_version:
            return f"INVALID-{version}->{min_version}"
        else:
            if sign_up_name:
                print("AUTH SYSTEM WIP")
                print(sign_up_name, bot_id)
                # if sign up key valid here
                valid_sign_up = False

                lines = []
                with open("users.txt", encoding="utf-8") as f:
                    for line in f.readlines():
                        split_line = line.split(", ")
                        if split_line[0] == "ACCOUNT":
                            if str(bot_id) == split_line[1].replace("\n", ""):
                                print("ACCOUNT ALREADY EXISTS")
                                return "ACC_ALR_EXT"
                        if split_line[0] == "NEW_ACCOUNT":
                            if str(bot_id) == split_line[1].replace("\n", ""):
                                auth_token = enc.hex_gens(32)
                                print("VALID BOT ACCOUNT", bot_id, sign_up_name, auth_token)
                                line = f"ACCOUNT, {bot_id}, {sign_up_name}, {auth_token}"
                                valid_sign_up = True
                        lines.append(line)
                if valid_sign_up:
                    with open("users.txt", "w", encoding="utf-8") as f:
                        to_write = ""
                        for item in lines:
                            to_write += item.replace("\n", "")+"\n"
                        f.write(to_write)

                    current_kt, current_key, old_key = get_server_key_from_file()
                    current_kt = datetime.datetime.strptime(str(current_kt), date_format_str)
                    return f"VALID-{version}-{tme}-{bld_num}-{run_num}Ō" \
                           f"{current_kt-datetime.timedelta(seconds=30)}={valid_time_keys['CURRENT']}" \
                           f"Ǘ{auth_token}"
                    # todo the new time system
                else:
                    return "ACC_CRT_NTA"
            else:
                if valid_user:
                    time_key_hashed = sha256(valid_time_keys['CURRENT'].encode()).hexdigest()
                    return f"VALID-{version}-{tme}-{bld_num}-{run_num}Ō{time_key_hashed}"
                else:
                    return f"NO_ACC_FND"


t = Thread(target=update_server_time_key)
t.daemon = True
t.start()


@bot.gateway.command
def processing(resp):
    m = resp.event.response
    if not str(m) == "{'t': None, 's': None, 'op': 11, 'd': None}":
        print(m)

    if resp.event.ready_supplemental:  # ready_supplemental is sent after ready
        user = bot.gateway.session.user
        print(f"logged in as {user['username']}#{user['discriminator']}")
        print("---")

    if resp.event.message:
        m = resp.parsed.auto()
        guildID = m['guild_id'] if 'guild_id' in m else "DM"  # because DMs are technically channels too
        channelID = m['channel_id']
        username = m['author']['username']
        discriminator = m['author']['discriminator']
        content = m['content']

        type = m['type']
        tts = m['tts']
        time_created = m['timestamp']
        try:
            reply = m['referenced_message']
        except:
            reply = "Null"
        mentions = m['mentions']
        mention_roles = m['mention_roles']
        mention_everyone = m['mention_everyone']

        id = m['id']
        bot_id = m['author']['id']
        embeds = m['embeds']
        attachments = m['attachments']

        print(time_created, content, )

        if channelID == "883425805756170283":
            if username+"#"+discriminator != "HELLOTHERE#9406":
                print(m)
                actual_message = False
                try:
                    content = enc.decrypt(content, valid_time_keys['CURRENT'])  # TODO MAKE THIS DF_KEY AS WELL
                    actual_message = True
                except:
                    try:
                        content = enc.decrypt(content, default_key)
                        print(content)
                        if content[136:] == "":
                            version_response = version_info(content[8:136], bot_id)
                        else:
                            version_response = version_info(content[8:136], bot_id, content[136:])
                        bot.sendMessage(channelID="883425805756170283",
                                        message=enc.encrypt(version_response, default_key))
                    except:
                        try:
                            content = enc.decrypt(content, valid_time_keys['OLD'])  # TODO MAKE THIS DF_KEY AS WELL
                            actual_message = True
                        except:
                            try:
                                content = enc.decrypt(content, valid_time_keys['NEW'])  # TODO MAKE THIS DF_KEY AS WELL
                                actual_message = True
                            except Exception as e:
                                print("Could not decrypt", e)

                if actual_message:
                    print(content)
                    bot.sendMessage(channelID="883425805756170283",
                                    message=enc.encrypt(enc.encrypt(content, valid_time_keys['CURRENT']), default_key))

        #if channelID == "883425805756170283":
        #    bot.deleteMessage(channelID=f"{channelID}", messageID=f"{id}")


bot.gateway.run(auto_reconnect=True)
