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


UDEV_RULE = (
    'SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="%s", '
    'ATTR{dev_id}=="0x0", ATTR{type}=="1", KERNEL=="wlan*", NAME="wlan0"')


def get_iface_infos():
    """Get infos about local network interfaces

    Returns a list of dicts, each one providing: `iface`, `bus`, `driver`, and
    `mac` infos.
    """
    infos = []
    for dev in os.listdir("/sys/class/net/"):
        drivers_path = "/sys/class/net/%s/device/driver/module/drivers" % dev
        if not os.path.exists(drivers_path):
            continue
        with open("/sys/class/net/%s/address" % dev, "r") as fd:
            mac = fd.read().strip()
        for driver in os.listdir(drivers_path):
            bus, drivername = '-', driver
            if ":" in driver:
                bus, drivername = driver.split(':', 1)
            infos.append(
                dict(iface=dev, bus=bus, driver=drivername, mac=mac))
    return infos


for info in get_iface_infos():
    print(" ".join([info['iface'], info['bus'], info['driver'], info['mac']]))
    print(UDEV_RULE % info['mac'])
