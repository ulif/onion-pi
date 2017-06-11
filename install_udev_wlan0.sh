#!/bin/bash
#
# Set udev rule to persist raspberry pi 3 builtin wifi to name 'wlan1'.
#
# Copyright (C) 2017, ulif <uli@gnufix.de>, GPL v3
#
# We expect the builtin wifi device to be driven by "brcmfmac" driver and being
# active on the "sdio" bus.
#
# This script was written for use with a raspberrypi3 and raspbian.
#
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

RULE='KERNEL=="wlan*", ATTR{address}=="'$MAC'", NAME="wlan1"'

echo "Pinning builtin wifi to name 'wlan1' via udev rule in /etc/udev/rules.d/70-persistent-net.rules"
echo "$RULE" >> "/etc/udev/rules.d/70-persistent-net.rules"
