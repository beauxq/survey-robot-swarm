#!/bin/bash

if [[ $# -eq 0 ]] ; then
    echo 'give robot number as argument'
    exit 0
fi

interface=$(ifconfig | grep -o wl.*: | cut -d':' -f 1)
echo "found interface $interface"

service network-manager stop
ip link set $interface down

iwconfig $interface mode ad-hoc
iwconfig $interface channel 4
iwconfig $interface essid geomars
iwconfig $interface key 7654321098

ip link set $interface up
ip addr add 192.168.76.$1/24 dev $interface

echo "192.168.76.$1 connected if you don't see any errors"
echo "service network-manager start  to undo"

echo "starting python main"
python3 ../client/main.py
