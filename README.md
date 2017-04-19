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

### Download and install Raspbian Jessie Lite on an SD card
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
