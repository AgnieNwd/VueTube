#!/bin/bash

# py is an aliases of python3
echo "hello world\n"
python3 -m venv env

source env/bin/activate

pip install --upgrade pip

# if this doesn't work, check that you're in the right directory
pip install -r requirements.txt

# if more packets are install after the setup is build, use this line in CLI
# pip freeze > requirements.txt

echo "All pip install has been done\n"