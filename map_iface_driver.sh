#!/bin/bash

set -e

MAC=`ls -d /sys/class/net/*/device/driver/module/drivers/* \
        | grep "/sdio:brcmfmac" \
        | head -1  \
        | awk -F "/" '{ print("/sys/class/net/" $5 "/address");}' \
        | xargs cat`

if [ -z "$MAC" ] ; then
    echo "no suitable device found" ;
    exit 1 ;
fi

RULE='SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="'$MAC'", '
RULE+='ATTR{dev_id}=="0x0", ATTR{type}=="1", KERNEL=="wlan*", NAME="wlan0"'

echo "Pinning builtin wifi to name 'wlan0' via udev rule in /etc/udev/rules.d/70-persistent-net.rules"
echo "$RULE" >> "/etc/udev/rules.d/70-persistent-net.rules"
