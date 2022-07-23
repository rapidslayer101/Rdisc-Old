if EXIST launch.bat (
    echo "launch.bat already exists, skipping installation"
    start launch.bat
) ELSE (
    echo Setting up repository
    git clone --filter=blob:none --no-checkout --depth 1 --sparse https://github.com/rapidslayer101/Rdisc
    cd Rdisc
    git config core.sparsecheckout true
    echo venv.zip > .git/info/sparse-checkout
    echo rdisc.py >> .git/info/sparse-checkout
    echo enclib.py >> .git/info/sparse-checkout
    echo ui.exe >> .git/info/sparse-checkout
    echo launch.bat >> .git/info/sparse-checkout
    echo Downloading and unpacking files
    git checkout
    tar -xf venv.zip
    echo Starting client
    start venv/Scripts/python.exe rdisc.py
)