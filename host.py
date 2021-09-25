import socket, re, base64, zlib, os, time
from threading import Thread
from datetime import datetime
from random import randint

# SERVER_HOST = "26.101.12.103"
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8080
separator_token = "<SEP>"

client_sockets = set()
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")


def listen_for_client(cs):
    print(cs)
    while True:
        send_all = 1
        send_new_key = 0
        try:
            msg = cs.recv(1024).decode()
            print(msg)
            if str(msg).startswith("[REQUEST CONNECTION]"):
                send_all = 0
                allow_client = 0

                m = re.search("SHA512: '(.+?)'", msg)
                if m:
                    client_sha512 = m.group(1)
                else:
                    client_sha512 = None

                m = re.search("raddr=\('(.+?)', ", str(new_socket))
                if m:
                    client_ip = m.group(1)

                with open("sha512_list.txt", encoding="utf-8") as f:
                    for line in f.readlines():
                        if client_sha512 in line:
                            m = re.search("VERSION: '(.+?)'", line)
                            if m:
                                client_version = m.group(1)
                            allow_client = 1

                if allow_client == 1:
                    print("Client accepted")
                    with open("mkey.txt", encoding="utf-8") as f:
                        for line in f.readlines():
                            mkey = line
                    with open("sha512_list.txt", encoding="utf-8") as f:
                        lines = f.readlines()
                        sha_scroll_up = -1
                        while True:
                            line = lines[sha_scroll_up]
                            if not "TESTBUILD" in line:
                                m = re.search("VERSION: '(.+?)'", line)
                                if m:
                                    sv_version_line = m.group(1)
                                break
                            sha_scroll_up = sha_scroll_up - 1

                    print(client_version)
                    if "TESTBUILD" in client_version:
                        to_send = f"[NE] [{date_now()}] [SERVER THREAD] <-- Connection for {client_address} accepted\n" \
                                  f"[NE] [{date_now()}] <-- You are on client v{client_version}\n" \
                                  f"[NE] [{date_now()}] <-- [KEY] --> '{mkey}'"
                        time.sleep(1)
                        new_socket.send(to_send.encode())
                        client_sockets.add(new_socket)

                    if client_version != sv_version_line:
                        if not "TESTBUILD" in client_version:
                            print("Version requires update")
                            to_send = f"[NE] [{date_now()}] [SERVER THREAD] <-- Connection for {client_address}" \
                                      f" declined - an update was detected\n" \
                                      f"[NE] [{date_now()}] <-- Type -update to update from " \
                                      f"{client_version} to {sv_version_line}"
                            new_socket.send(to_send.encode())
                    else:
                        to_send = f"[NE] [{date_now()}] [SERVER THREAD] <-- Connection for {client_address} accepted\n" \
                                  f"[NE] [{date_now()}] <-- You are on client v{client_version}\n" \
                                  f"[NE] [{date_now()}] <-- [KEY] --> '{mkey}'"
                        time.sleep(1)
                        new_socket.send(to_send.encode())
                        client_sockets.add(new_socket)
                else:
                    print("Client declined")
                    to_send = f"[NE] [{date_now()}] [SERVER THREAD] <-- Connection for {client_address}" \
                              f" declined - your client is not compatible with the network"
                    new_socket.send(to_send.encode())

                msg = None

                to_send = encrypt2(f"[{date_now()}] [SERVER THREAD] [CLIENT JOINED] - IP: {client_ip} v{client_version}\n"
                                   f" >> [E] [{date_now()}] [SERVER THREAD] [CONNECTED] - {len(client_sockets)}")
                for client_socket in client_sockets:
                    client_socket.send(to_send.encode())

            else:
                # gen new key?
                make_new = randint(1, 20)
                if make_new == 1:
                    master_key = generator()
                    print("NEW KEY ISSUED", master_key)
                    new_key1 = f"[{date_now()}] SERVER [KEY] --> '{master_key}'"
                    new_key1 = encrypt2(new_key1)
                    new_key(master_key)
                    send_new_key = 1

        except Exception as e:
            client_sockets.remove(cs)
            to_send = f"[{date_now()}] [SERVER THREAD] [Error] - {e}"
            to_send = encrypt2(to_send)
            client_socket.send(to_send.encode())
        if send_all == 1:
            for client_socket in client_sockets:
                client_socket.send(msg.encode())

        if send_new_key == 1:
            for client_socket in client_sockets:
                client_socket.send(new_key1.encode())


while True:
    client_socket, client_address = s.accept()
    print("NEW CLIENT:", client_socket, client_address)

for cs in client_sockets:
    cs.close()
s.close()
