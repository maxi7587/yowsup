#!/bin/bash
export PYTHONPATH=`pwd`

while [[ 1 ]];do
    python ./whatsapp_daemon/run.py
    # pid=$!
    sleep 10
    # kill -9 $pid
done
