#!/bin/bash

pids_of_processes_with_mask() {
    mask=$1
    ps aux | grep $mask | awk '!/grep/ {print $2}'
}

kill_all_processes_with_mask() {
    mask=$1
    for pid in $(pids_of_processes_with_mask $mask); do
        kill -SIGTERM $pid
    done
}

kill_all_processes_with_mask "ssh -f -N proxy"
ssh -f -N proxy
