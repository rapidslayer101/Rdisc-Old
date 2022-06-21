from os import system
system("git reset --hard")
system("git pull origin master")
print("Launching client")
system("python rdisc.py")

