# onion-pi
Turn a standard Raspbian install into a [tor](https://torproject.org)-ified
wifi access point with [ansible](https://www.ansible.com/).

This is the ``Zwiebelkuchen`` (German for onion pie) edition of stock adafruit
onion-pi.

This build is different from the original in some minor details. See the list
at end of this document for details.

## Ingredients

We will make use of

* 1 RaspberryPi 3
* 1 micro SD card (min. 4 GB, SDHC, class 10, UHS-I)
* 1 USB wifi adapter
* 1 USB TTL connection cable (see below)

If no such connection cable is at hand, we need additionally:

* 1 power adapter
* 1 keyboard (bluetooth or USB)
* 1 TV or other device able to display HDMI signals from your RaspberryPi

To setup everything, we additionally need a computer with USB and an SD-card
reader. If your computer does not have a built-in card-reader, you can use any
cheap USB-pluggable SD-card reader available at paper stores and similar.


## Preparation

### 1) Download and install Raspbian Jessie Lite on an SD card

We will use the lite image of Raspbian Jessie as provided at

  https://www.raspberrypi.org/downloads/raspbian/

Afterwards you should have a file named ``2017-04-10-raspbian-jessie-lite.zip``
or similar (depending on the current date). This ZIP archive should contain one
big image file.

Check the sha1 sum of the file:

    $ sha1sum 2017-04-10-raspbian-jessie-lite.zip
    c24a4c7dd1a5957f303193fee712d0d2c0c6372d 2017-04-10-raspbian-jessie-lite.zip

and make sure it equals the number given on the website.

If so, you can unzip the file with

    $ unzip 2017-04-10-raspbian-jessie-lite.zip

but it is not neccessary for our purposes. We will unzip the file on-the-fly
and write the contents to a locally attached SD card:

    $ zcat 2017-04-10-raspbian-jessie-lite.zip | dd of=/dev/sdX bs=4M

where ``/dev/sdX`` refers to your SD-card.


### 2) Enable UART Access

You can skip this step, if you use external keyboard/screen for initial setup.
But if you use a TTL connection cable for it, you have to enable "serial"
access first.

Your freshly created SD-card should now contain two partitions: one for boot
files and one with the root filesystem. The boot filesystem should come first.
If you cannot see these partitions, eject your SD-card and reinsert it in your
computer.

Then, mount the boot partition (should be done automatically when the SD-card
is inserted in a running Ubuntu) and find a file named 'config.txt'. Edit this
file and add a line at end reading:

    enable_uart=1

There should be no spaces in this stanza.

When done, save the file and eject the SD-card properly.


## Basic Setup

### 1) Start Your RaspberryPi

Stick the prepared SD card into your RaspberryPi.

If you want to use a TTL cable, connect it now with your Raspi and then plug it
into a USB port at your computer. This will power up the RaspberryPi.

Otherwise plug in your keyboard and connect the HDMI port with an appropriate
device. Also plug in the power adapter, which will power up the RaspberryPi.


### 2) Setup basic settings

If you use a TTL connection cable, you can connect to your RaspberryPi doing

    $ sudo screen /dev/ttyUSB0 115200

where "/dev/ttyUSB0" should be the RaspberryPi as it appears to your system
when connected via USB.

If you use an external keyboard/screen, then you should see the startup
messages already.

Now you should be able to login into your new system (credentials
"pi"/"raspberry"),

Setup basic settings using

    (raspi) $ sudo raspi-config

In the appearing menu do at least the following:

- Under 'Change User Password'`, well, change your user password
- Under 'Localisation Options' set the timezone
- Under 'Localisation Options' set the wi-fi country
- Under 'Interfacing Options' enable SSH server
- Under 'Advanced Options' expand the filesystem to use all of the SD card

Optionally you may:

- Under 'Hostname' set a new hostname.
- Under 'Boot Options' pick console login without autologin
- Under 'Localisation Options' pick a special keyboard layout
- Under 'Localisation Options' pick a special locale

When done, choose "Finish" and reboot.


### 3) Setup first Wifi

If not done already, plug in the USB wifi adapter into your raspi.

We need internet access to complete the next steps. This step depends on your
local networks.

A list of available networks should be provided with:

    (raspi) $ sudo iwlist wlan0 scan | grep ESSID

We then have to edit

    (raspi) $ sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

To add a network without password add something like:

    network={
        ssid="Freifunk"
        key_mgmt=NONE
    }

For networks with a password you want to run `wpa_passphrase`:

    (raspi) $ sudo bash
    (raspi) # wpa_passphrase '<SSID>' '<PASSWORD>' >> /etc/wpa_supplicant/wpa_supplicant.conf
    (raspi) # exit

Afterwards a wifi restart is required. This can be done with:

    (raspi) $ sudo wpa_cli reconfigure
    Selected interface 'wlan0'
    OK

The negotiations might take some seconds, so you should wait for some time,
until the new connection will be established. Keep the displayed interface name
in mind (``wlan0`` or ``wlan1``).

You can get the IP number assigned by running

    (raspi) $ ifconfig wlan0

where `wlan0` is the interface name displayed before.

There should be one line starting with `inet` or `inet6` stating the current
IP.

Now try to connect to your zwiebelkuchen via SSH:

    $ ssh pi@<IP-OF-YOUR-RASPBERRY-PI>

You must complete this step at least once to enable flawless `ansible` runs
later on.


## Prepare `ansible`


We will use `ansible` to provision `zwiebelkuchen` with all software/settings
needed. Make sure you have version 2.x installed on the host where you also
have SSH access to the `zwiebelkuchen`.

In the end the following command should succeed without any error message:

    (laptop) $ ansible -i <RASPI-IP>, all -b -k -u pi -m setup

and output lots of infos gathered about the raspi (please mind the trailing
comma behind the IP).


## Run `ansible` turn ordinary raspi into a `zwiebelkuchen`

Before we proceed, we need internet access from the `zwiebelkuchen`.

Log into your `raspi` and update the system:

    (raspi) $ sudo apt-get update
    (raspi) $ sudo apt-get upgrade

If packages have been upgraded during this step (consult the display output), a
system restart is recommended or even required before you proceed.

    (raspi) $ sudo reboot

After reboot, run the ansible playbook `setup_zwiebelkuchen.yml` from the computer
which has SSH access to your `zwiebelkuchen`:

    $ ansible-playbook -i <RASPI-IP>, -b -u pi -k setup_zwiebelkuchen.yml

This step will normally take some time. Afterwards restart the raspi

    (raspi) $ sudo reboot

and enjoy.


## Access your `zwiebelkuchen`

Did it work? You can try with your laptop.

First, look what networks are available to connect to. There should be an
additional network called ``zwiebelkuchen``. Connect to it.

The network is encrypted and therefore we need a password. The default password is

    tor

and set in `/etc/hostapd/hostapd.conf`.

If you can connect to the network, try to browse some site. As `ping` does not
work, you can for instance browse

    https://check.torproject.org

to check under which IP you are seen in the internet. This page can tell
whether you look like using `tor` or not. It might also complain that you do
not use the `torbrowser`.


# Differences to Regular Adafruit Onion-pi Setup

The deployment shown here tries to follow closely the more or less canonical
'Adafruit' recipe as described at:

    https://learn.adafruit.com/onion-pi/overview

Some things, however, were changed:

- IPv4 forwarding is not activated. Instead we make sure its turned off.

  There is no reason to forward all ipv4 packets if they cannot be handled as
  regular tor traffic.

- `/etc/init.d/hostapd` script is not changed.

  We do not set a default `DAEMON_CONF` in the init.d-script, because this
  value should be set only in `/etc/default/hostapd`.

- We additionally install and configure `unattended-upgrades`.

  Updates are triggered by a cronjob every other hour.
