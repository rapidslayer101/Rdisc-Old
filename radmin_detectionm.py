import psutil

while True:
    try:
        addresses = psutil.net_if_addrs()["Radmin VPN"]
        print(addresses)
    except KeyError:
        print("Radmin is not installed on this machine")
    input()