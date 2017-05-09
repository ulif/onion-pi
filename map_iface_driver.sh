#!/bin/bash

set -e

MAC=`ls -d /sys/class/net/*/device/driver/module/drivers/* \
        | cut -d '/' -f "5,10" --output-delimiter " " \
        | grep "sdio" \
        | head -1  \
        | awk '{ print("/sys/class/net/" $1 "/address");}' \
        | xargs cat`

if [ -z "$MAC" ] ; then
    echo "no suitable device found" ;
    exit 1 ;
fi

RULE='SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="'$MAC'", '
RULE+='ATTR{dev_id}=="0x0", ATTR{type}=="1", KERNEL=="wlan*", NAME="wlan0"'

echo "$RULE" >> "/etc/udev/rules.d/70-persistent-net.rules"
