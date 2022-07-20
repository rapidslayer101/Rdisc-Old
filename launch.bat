echo Checking for updates
git reset --hard
git pull origin master
echo Launching client
venv/Scripts/python.exe rdisc.py