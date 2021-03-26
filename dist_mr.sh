#!/bin/bash

python worker.py --name 1 &
python worker.py --name 2 &
python worker.py --name 3 &
python worker.py --name 4 &

python driver.py $@
