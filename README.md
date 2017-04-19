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


### 2) Enable UART access

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
