#!/bin/bash

ls -d /sys/class/net/*/device/driver/module/drivers/* | cut -d '/' -f "5,10" --output-delimiter " " | cut -d ':' -f "1-" --output-delimiter " "
