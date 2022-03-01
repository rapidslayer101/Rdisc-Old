from os import startfile
from zipfile import ZipFile
import time
time.sleep(2)
try:
    with ZipFile("Update.zip", 'r') as zip_:
        zip_.printdir()
        print('Extracting update files...')
        zip_.extractall()
        print('Update patches applied, launching rdisc')
except FileNotFoundError:
    print("No update files found, launching rdisc")
time.sleep(2)
startfile("rdisc.exe")
time.sleep(2)
