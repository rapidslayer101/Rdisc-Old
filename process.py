import socket, os, time, re
from base64 import b64decode
from zlib import decompress
from random import randint
from hashlib import sha512
from threading import Thread
from datetime import datetime


# 0.1 created encryption algorithm
# 0.2 created rchat end to end application
# 0.3 created file sending system
# 0.4 created auto update, mkey sending
# 0.5 created rewrote and improved e
# 0.6 created GUI and c# <--> python system
# 0.7 created auto update 2.0

# ports 8080, 5001, 8079
# Made by rapidslayer101
# Testers: James judge, Kit jackson

h_name = socket.gethostname()
SERVER_HOST = "26.111.108.30"
SERVER_PORT = 8080
s = socket.socket()

while True:
    try:
        s.connect((SERVER_HOST, SERVER_PORT))
        break
    except:
        warn("Could not connect to host, hit enter to try again")
    inp("")
to_c(f"[NE] [{date_now()}] --> Connected to host, awaiting key")

if not os.path.exists(f'name.txt'):
    to_c("\nYou have not set a name yet! Type one and hit enter")
    while True:
        name = inp("")[2:]
        if len(name) > 24:
            warn("This name is to long, max length 24 chars")
        else:
            with open("name.txt", "w", encoding="utf-8") as f:
                f.write(name)
                break
else:
    with open("name.txt", encoding="utf-8") as f:
        for line in f.readlines():
            name = line
            if len(name) > 24:
                warn("\nThis loaded name is to long, max length 24 chars, type a new one")
                while True:
                    name = inp("")[2:]
                    if len(name) > 24:
                        warn("This name is to long, max length 24 chars")
                    else:
                        with open("name.txt", "w", encoding="utf-8") as f:
                            f.write(name)
                            break


if not os.path.exists(f'ip.txt'):
    h_name = socket.gethostname()
    IP_address = socket.gethostbyname(h_name)
    if "26." not in str(IP_address):
        to_c("\nYou have not set a ip yet, tried to set automatically but radmin was not your default")
        to_c("\nPlease find and copy your radmin IP and enter it")
        while True:
            IP_address = inp("")
            if "26." not in str(IP_address):
                warn("This IP is not a radmin 26. IP, you will not be able to receive files unless you change this IP")
            with open("ip.txt", "w", encoding="utf-8") as f:
                f.write(IP_address)
                break
    else:
        with open("ip.txt", "w", encoding="utf-8") as f:
            f.write(IP_address)
else:
    with open("ip.txt", encoding="utf-8") as f:
        for line in f.readlines():
            IP_address = line

s.send(f"[REQUEST CONNECTION] --> SHA512: '{sha512.hexdigest()}'".encode())


def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        if "[NE]" not in message[:20]:
            message = decrypt(message)
        m = re.search('<SEP1>(.+?)<SEP2>', message)
        if m:
            command = m.group(1)
        else:
            command = ""

        if command.startswith(" [CONNECTIONS]"):
            to_send = " [CONNECTIONS RESPONSE]"
            text = f"[{date_now()}] {h_name} {name}" \
                   f"{separator_token}{to_send}{separator_token2}"
            text = encrypt2(text)
            s.send(text.encode())

        if command.startswith(" [PING]"):
            if command[12:] == name:
                ToastNotifier().show_toast(title="PING!", msg="A user has pinged you in Rchat!",
                                           icon_path="rchat.ico", duration=5, threaded=True)

        #if command.startswith(" [CONNECTIONS RESPONSE]"):
            #message = search(data=line, filter_fr="", filter_to="<SEP2>")

        if command.startswith(" [FILE TRANSFER]"):
            with open("sending.txt", encoding="utf-8") as f:
                for line in f.readlines():
                    if line == "0":
                        to_c("FILE TRANSFER DETECTED")

                        to_send = f" [ACCEPT TRANSFER] --> {IP_address} | 21"
                        text = f"[{date_now()}] {h_name} {IP_address} {name}" \
                               f"{separator_token}{to_send}{separator_token2}"
                        text = encrypt2(text)
                        s.send(text.encode())

                        try:
                            file_receive.receive(IP_address=IP_address)
                        except:
                            to_c(f"[{date_now()}] ERROR [!] - File receive failure")

        if "[KEY] -->" in str(message):
            master_key = search(data=message, filter_fr="KEY] --> '", filter_to="'")
            new_key(master_key)
            message = message.replace(f" --> '{master_key}'", "")

        if command.startswith(" [ACCEPT TRANSFER]"):
            with open("sending.txt", encoding="utf-8") as f:
                for line in f.readlines():
                    if line == "1":
                        to_c(f"ACCEPT TRANSFER FROM {command}")
                        ip = search(data=line, filter_fr="ACCEPT TRANSFER] --> ", filter_to=" | 21")
                        try:
                            file_send.send(filename=filename, ip=ip)
                        except:
                            to_c(f"[{date_now()}] ERROR [!] - File send failure")

        message = message.replace("/shrug", "¯\_(ツ)_/¯")
        message = message.replace(separator_token, "")
        message = message.replace(separator_token2, "")

        to_c(message)


t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

while True:
    allow_send = 1
    exiter = 0
    to_send = inp("")

    if to_send == ": ":
        warn("You cannot send an empty message!")
        allow_send = 0

    try:
        with open("last_sent.txt") as f:
            for line in f.readlines():
                last_msg_time = line
        last_msg_time = datetime.strptime(last_msg_time, '%Y-%m-%d %H:%M:%S.%f')
        time_since_insertion = datetime.utcnow() - last_msg_time
        if time_since_insertion.seconds < 0.5:
            msg_to_fast = msg_to_fast + 1
            if msg_to_fast > 10:
                warn(f"YOU'RE SENDING MESSAGES TOO FAST! last message was {time_since_insertion}")
                allow_send = 0
        if time_since_insertion.seconds > 5:
            msg_to_fast = 0
    except:
        xxx = 0

    with open("last_sent.txt", "w") as f:
        f.write(str(datetime.utcnow()))

    if len(to_send) > 2000:
        warn("Your message is over the 2000 char limit, send a shorter message!")
    else:
        if to_send.lower() == ': -client commands':
            to_send = f" [CLIENT COMMANDS] --> -client commands, -update, -restart," \
                      f" -change ip, -change name, -change mkey, -connected, -send, -ping"

        if to_send.lower() == ': -update':
            to_c("This client will now exit, update initialising file transfer")
            os.startfile("updater.exe")
            exiter = 1
            allow_send = 0

        if to_send.lower() == ': -quit':
            exiter = 1
            to_send = " [QUIT]"

        if to_send.lower() == ': -restart':
            os.startfile("restart.bat")
            exiter = 1
            to_send = " [RESTART]"

        if to_send.lower().startswith(': -change ip'):
            allow_send = 0
            new_ip = to_send[13:]
            if new_ip == "":
                warn("You did enter an ip! Do '-change ip <NEW IP>'")
            else:
                if "26." not in str(new_ip):
                    warn("This IP is not a radmin 26. IP, you will not be able"
                         " to receive files unless you change this IP")
                IP_address = new_ip
                with open("ip.txt", "w", encoding="utf-8") as f:
                    f.write(IP_address)

        if to_send.lower().startswith(': -change name'):
            new_name = to_send[15:]
            if new_name == "":
                warn("You did enter a name! Do '-change ip <NEW NAME>'")
                allow_send = 0
            else:
                to_send = f" [CHANGE NAME] {name} --> {new_name}"
                name = new_name
                with open("name.txt", "w", encoding="utf-8") as f:
                    f.write(name)

        if to_send.lower().startswith(': -change mkey'):
            new_mkey = to_send[15:]
            allow_send = 0
            if new_mkey == "":
                warn("You did enter a new key! Do '-change mkey <NEW MKEY>'")
            else:
                to_send = f" [CHANGE MKEY]"
                try:
                    new_key(new_mkey)
                except:
                    warn("The key you entered is not valid")

        if to_send.lower() == ': -connected':
            to_send = " [CONNECTIONS]"

        if to_send.lower() == ': -send':
            filename = inp("Drag file onto window and hit enter\n")
            try:
                filename = filename.replace("\"", "")
                filesize = os.path.getsize(filename)
                filebasename = os.path.basename(filename)
                f_name, f_ext = os.path.splitext(filename)

                if f_ext in [".txt"]:
                    inp("This file type will soon support file encryption, but it doesnt yet, hit enter to cont.")
                else:
                    inp("THIS FILE TYPE DOES NOT SUPPORT ENCRYPTION (yet), YOUR FILE WILL NOT BE SENT ENCRYPTED.\n"
                        "HIT ENTER TO CONFIRM SEND")

                def format_bytes(size):
                    power = 2 ** 10
                    n = 0
                    power_labels = {0: '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
                    while size > power:
                        size /= power
                        n += 1
                    return f"{round(size,2)} {power_labels[n]}bytes"
                filesize_converted = format_bytes(filesize)
                to_send = f" [FILE TRANSFER] --> {filebasename} | {filesize_converted} == {filesize} bytes"
                with open("sending.txt", "w", encoding="utf-8") as f:
                    f.write("1")
            except:
                warn("Invalid file, exiting")
                to_send = f" [FAILED FILE TRANSFER]"

        if to_send.lower().startswith(': -ping'):
            ping = to_send[8:]
            if ping == "":
                warn("You did enter who to ping! Do '-ping <NAME>'")
                allow_send = 0
            else:
                to_send = f" [PING] --> {ping}"

        # LIEF

        if to_send.lower() == ': -lief':
            to_c("ENTERED LIEF PRIVATE CHANNEL")
            to_send = " [L I E F]"

        # LIEF

        if allow_send == 1:
            text = f"[{date_now()}] {h_name} {name}" \
                   f"{separator_token}{to_send}{separator_token2}"
            text = encrypt2(text)
            s.send(text.encode())

    if exiter == 1:
        time.sleep(5)
        break

s.close()