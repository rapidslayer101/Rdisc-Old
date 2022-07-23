if EXIST launch.bat (
    echo "launch.bat already exists, skipping installation"
    start launch.bat
) ELSE (
    echo Downloading files
    git clone https://github.com/rapidslayer101/Rdisc
    cd Rdisc
    echo Unzipping python virtual environment
    tar -xf venv.zip
    echo Starting client
    start venv/Scripts/python.exe rdisc.py
)
END