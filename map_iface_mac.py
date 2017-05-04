#
# For all local network devices output
#
#   devicename bustype drivername mac-address
#
# if these infos are provided by system. bustype is normally "usb", "pci",
# "sdio" or "-". `mac-address` comes in "aa:bb:cc..." notation.
#
# This script requires a fairly recent Linux system.
import os

for dev in os.listdir("/sys/class/net/"):
    drivers_path = "/sys/class/net/%s/device/driver/module/drivers" % dev
    if not os.path.exists(drivers_path):
        continue
    drivers = os.listdir(drivers_path)
    for driver in drivers:
        bus, drivername = '-', driver
        if ":" in driver:
            bus, drivername = driver.split(':', 1)
        with open("/sys/class/net/%s/address" % dev, "r") as fd:
            mac = fd.read().strip()
        print(" ".join([dev, bus, drivername, mac]))
