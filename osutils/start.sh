#!/bin/bash

# old command line argument code
#if [[ $# -eq 0 ]] ; then
#    echo 'give robot number as argument'
#    exit 0
#fi

interface=$(ls /sys/class/net | grep -o wl.*)
echo "found interface $interface"

id=$(grep -o "robot_id = .*$" ../client/config.txt | cut -c12-)
echo "found robot_id $id"

service network-manager stop
ip link set $interface down

iwconfig $interface mode ad-hoc
iwconfig $interface channel 4
iwconfig $interface essid geomars
iwconfig $interface key 7654321098

ip link set $interface up
ip addr add 192.168.76.$id/24 dev $interface

echo "192.168.76.$id connected if you don't see any errors"
echo "service network-manager start  to undo"

echo "starting python main"
cd ../client
python3 main.py
