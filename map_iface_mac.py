#
# Helpers to determine local network devices.
#
# Can also install a udev rule to pin down a raspberrypi3 builtin nic to
# `wlan0` and check whether this rule was already applied to the system.
#
# Usage: <scriptname> [check|install]
#
# Without any command, we list all found devices with some data. For each
# device we show kernel name, bus type, driver name, and mac address.
#
# This script requires a fairly recent Debian (or derived) system. Tested with
# Raspbian.
#
import getopt
import json
import os
import sys


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
    """Returns info about the raspberrypi3 builtin wifi device (if found).

    If no such device is found, return None.
    """
    for info in get_iface_infos():
        if info['driver'] != 'brcmfmac':
            continue
        if info['bus'] != 'sdio':
            continue
        if not info['mac'].startswith('b8:27'):
            continue
        return info
    return None


def install_udev_rule():
    """Register the builtin wifi device of raspverrypi3 as `wlan0` on boot.
    """
    info = get_builtin_wlan_dev()
    rule = UDEV_RULE % info['mac']
    if is_udev_rule_installed(info, rule):
        return
    with open(UDEV_RULES_PATH, "a") as fd:
        fd.write(rule)
    print("written rule\n  %s\nto %s" % rule, UDEV_RULES_PATH)


def main():
    """Evaluate given commandline args and execute requested commands.
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", [])
    except getopt.GetoptError as err:
        print(err)
        print("Usage: %s [install|check]" % sys.argv[0])
        sys.exit(2)
    if len(args) != 1:
        print(json.dumps(get_iface_infos(), indent=4, sort_keys=True))
        sys.exit()
    if args[0] == "check":
        info = get_builtin_wlan_dev()
        rule = UDEV_RULE % info['mac']
        if is_udev_rule_installed(get_builtin_wlan_dev(), rule):
            print("installed")
        else:
            print("not installed")
            sys.exit()
    elif args[0] == "install":
        install_udev_rule()
        sys.exit()


if __name__ == '__main__':
    main()
