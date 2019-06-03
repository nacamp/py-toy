#!/bin/sh
PYTHONPATH=/Users/jimmy/src/python/py-toy
export PYTHONPATH

while true
do
    echo "$@"
    webkit2png "$@" -o new -F
    python3 "$PYTHONPATH/monitor/img.py" "$PYTHONPATH/monitor/org.png"  "$PYTHONPATH/monitor/new-full.png"
    #python3 "$PYTHONPATH/monitor/img.py" "$@"
    sleep 60
done