# onion-pi
Turn a standard Raspbian Lite install into a tor-ified wifi access point


## Preparation

### Download and install Raspbian Jessie Lite
We will use the lite image of Raspbian Jessie as provided at

  https://www.raspberrypi.org/downloads/raspbian/

Afterwards you should have a file named ``2017-04-10-raspbian-jessie-lite.zip``
or similar. This ZIP archive should contain one big image file.

Check the sha1 sum of the file:

    $ sha1sum 2017-04-10-raspbian-jessie-lite.zip
    c24a4c7dd1a5957f303193fee712d0d2c0c6372d 2017-04-10-raspbian-jessie-lite.zip

and make sure it equals the number given on the website.

You can unzip the file doing

    $ unzip 2017-04-10-raspbian-jessie-lite.zip

but it is not neccessary for our purposes. We will unzip the file on-the-fly
and write the contents to a locally attached SD card.

