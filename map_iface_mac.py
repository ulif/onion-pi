#
# For all local network devices output
#
#   devicename bustype drivername mac-address
#
# if these infos are provided by system. bustype is normally "usb", "pci",
# "sdio" or "-". `mac-address` comes in "aa:bb:cc..." notation.
#
# This script requires a fairly recent Debian (or derived) system. Tested with
# Raspbian.
#
import os


UDEV_RULE = (
    'SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="%s", '
    'ATTR{dev_id}=="0x0", ATTR{type}=="1", KERNEL=="wlan*", NAME="wlan0"')


UDEV_RULES_PATH = "/etc/udev/rules.d/70-persistent-net.rules"


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


def is_udev_rule_installed(info, rule):
    """Check whether our specific udev rule is installed already.
    """
    if not os.path.exists(UDEV_RULES_PATH):
        return False
    with open(UDEV_RULES_PATH, "r") as fd:
        rules = fd.read()
    for installed_rule in rules:
        if rule == installed_rule:
            return True
    return False


def get_builtin_wlan_dev():
    for info in get_iface_infos():
        if info['driver'] != 'brcmfmac':
            continue
        if info['bus'] != 'sdio':
            continue
        if not info['mac'].startswith('b8:27'):
            continue
        return info
    return None


for info in get_iface_infos():
    print(" ".join([info['iface'], info['bus'], info['driver'], info['mac']]))
    rule = UDEV_RULE % info['mac']
    print(rule)
    print(is_udev_rule_installed(info, rule))

print(get_builtin_wlan_dev())
