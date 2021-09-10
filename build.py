import os, datetime
from hashlib import sha512

with open("sha.txt", encoding="utf-8") as f:
    latest_sha, type, version, tme, bld_num, run_num = f.readlines()[-1].split(" ")
    print(latest_sha, type, version, tme, bld_num, run_num)
    release_major, major, build, run = version.replace("V", "").split(".")

os.startfile("build.bat")
input("Hit enter when build finished")
is_major = input("Major y/n: ")
if is_major.lower() == "y":
    major = int(major)+1
    build = 0
    run = 0
else:
    build = int(build)+1
    run = 0

block_size = 65536
hash_ = sha512()
with open("C:/Users/rapidslayer101/PycharmProjects/rdisc/venv/Scripts/dist/rdisc.exe", 'rb') as hash_file:
    buf = hash_file.read(block_size)
    while len(buf) > 0:
        hash_.update(buf)
        buf = hash_file.read(block_size)
hashed = hash_.hexdigest()

if latest_sha == hashed:
    print("This build is identical to the previous, no changes to sha.txt have been made")
else:
    with open("sha.txt", "a+", encoding="utf-8") as f:
        tme = str(datetime.datetime.now()).replace(" ", "_")
        print(f"{hashed} BLD V{release_major}.{major}.{build}.{run} TME-{tme}"
              f"BLD_NM-{int(bld_num[7:])+1} RUN_NM-{run_num[7:]}")
        f.write(f"\n{hashed} BLD V{release_major}.{major}.{build}.{run} TME-{tme}"
                f" BLD_NM-{int(bld_num[7:])+1} RUN_NM-{run_num[7:]}")
