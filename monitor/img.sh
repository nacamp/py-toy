#!/bin/sh
PYTHONPATH=/Users/jimmy/src/python/py-toy
export PYTHONPATH

while true
do
    echo "$@"
    webkit2png "$@" -o new -F -D "$PYTHONPATH/data"
    python3 "$PYTHONPATH/monitor/img.py" "$PYTHONPATH/data/org.png"  "$PYTHONPATH/data/new-full.png"
    #python3 "$PYTHONPATH/monitor/img.py" "$@"
    sleep 60
done