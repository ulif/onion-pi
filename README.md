# onion-pi
Turn a standard Raspbian install into a [tor](https://torproject.org)-ified
wifi access point with [ansible](https://www.ansible.com/).


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
or similar. This ZIP archive should contain one big image file.

Check the sha1 sum of the file:

    $ sha1sum 2017-04-10-raspbian-jessie-lite.zip
    c24a4c7dd1a5957f303193fee712d0d2c0c6372d 2017-04-10-raspbian-jessie-lite.zip

and make sure it equals the number given on the website.

If so, you can unzip the file with

    $ unzip 2017-04-10-raspbian-jessie-lite.zip

but it is not neccessary for our purposes. We will unzip the file on-the-fly
and write the contents to a locally attached SD card:

    $ zcat 2017-04-10-raspbian-jessie-lite.zip | dd of=/dev/sdXX bs=4M

where ``/dev/sdXX`` refers to your SD-card.


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
    (raspi) # wpa_passphrase <SSID> <PASSWORD> >> /etc/wpa_supplicant/wpa_supplicant.conf
    (raspi) # exit

Afterwards a wifi restart is required. This can be done with:

    (raspi) $ sudo wpa_cli reconfigure
    Selected interface 'wlan0'
    OK

The negotiations might take some seconds, so you should wait for some time,
until the new connection will be established.


## Install Accesspoint

## Install tor

