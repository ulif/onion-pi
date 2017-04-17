# onion-pi
Turn a standard Raspbian install into a tor-ified wifi access point with `ansible`

## Ingredients

We will make use of

* 1 RaspberryPi 3
* 1 micro SD card (min. 4 GB, SDHC, class 10, UHS-I)
* 1 USB wifi adapter
* 1 USB TTL connection cable

If no such connection cable is at hand, we need additionally:

* 1 power adapter
* 1 blue tooth or USB keyboard
* 1 device able to display HDMI sighnals from your RaspberryPi

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
and write the contents to a locally attached SD card.

Make sure, you know the device name of your SD card.
