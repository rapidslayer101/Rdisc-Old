from datetime import datetime
from hashlib import sha512
import enclib as enc

with open("sha.txt", encoding="utf-8") as f:
    latest_sha, run_type, version, tme, bld_num, run_num = f.readlines()[-1].split("§")
    print(latest_sha, run_type, version, tme, bld_num, run_num)
    release_major, major, run = version.replace("V", "").split(".")

is_major = input("Major y/n: ")
if is_major.lower() == "y":
    major = int(major)+1
    run = 0

block_size = 65536
hash_ = sha512()
hashed = enc.hash_a_file("C:/Users/rapid/PycharmProjects/rdisc/rdisc.py")

if latest_sha == hashed:
    print("This build is identical to the previous, no changes to sha.txt have been made")
else:
    with open("sha.txt", "a+", encoding="utf-8") as f:
        tme = str(datetime.now())[:-4].replace(' ', '_')
        print(f"{hashed}§COM§V{release_major}.{major}.{run}§TME-{tme}"
              f"§RUN_NM-{run_num[7:]}")
        f.write(f"\n{hashed}§BLD§V{release_major}.{major}.{run}§TME-{tme}"
                f"§RUN_NM-{run_num[7:]}")
