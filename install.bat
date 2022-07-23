if EXIST launch.bat (
    echo "launch.bat already exists, skipping installation"
    start launch.bat
) ELSE (
    echo Downloading files
    git clone --filter=blob:none --no-checkout https://github.com/rapidslayer101/Rdisc
    cd Rdisc
    git sparse-checkout init --cone
    git read-tree -mu HEAD
    echo Unzipping python virtual environment
    tar -xf venv.zip
    echo Starting client
    start venv/Scripts/python.exe rdisc.py
)
END