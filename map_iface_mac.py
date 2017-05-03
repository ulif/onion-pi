#
# Output
#
#   devicename bustype drivername mac-address
#
# for all network devices that provide these infos. bustype is normally "usb",
# "pci" or "-". `mac-address` comes in "aa:bb:cc..." hexadecimal notation.
#
import os

for dev in os.listdir("/sys/class/net/"):
    drivers_path = "/sys/class/net/%s/device/driver/module/drivers" % dev
    if not os.path.exists(drivers_path):
        continue
    drivers = os.listdir(drivers_path)
    for driver in drivers:
        bus, drivername = '', driver
        if ":" in driver:
            bus, drivername = driver.split(':', 1)
        with open("/sys/class/net/%s/address" % dev, "r") as fd:
            mac = fd.read()
        print(" ".join([dev, bus, drivername, mac]))
