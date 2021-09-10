import os
from mega import Mega
mega = Mega()
m = mega.login("theretards909@gmail.com", "smokester1/")
print("Starting file downloads")
file = m.find('rdisc.exe')
try:
    m.download(file)
except PermissionError:
    print("rdisc.exe downloaded")
file = m.find('ui.exe')
try:
    m.download(file)
except PermissionError:
    print("ui.exe downloaded")
if not os.path.isfile("user_agents.zip"):
    file = m.find('user_agents.zip')
    try:
        m.download(file)
    except PermissionError:
        print("user_agents.zip downloaded")
os.startfile("rdisc.exe")
