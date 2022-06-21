from os import system
system("git clean")
system("git pull origin master")
print("Launching client")
system("python rdisc.py")

