# pi-photobooth

A Raspberry Pi Powered photobooth

This is a photobooth app to combine a:
1.)	Raspberry pi (I used a v3 for the extra horsepower)
2.)	A monitor (I used an older lcd with a dvi-to-hdmi cable
3.)	An SLR camera (I used an older Canon XS with the kit lens, locked on manual exposure and in raw file output, but otherwise in auto mode)
4.)	A Canon Selphy CP1200 photo printer (prints borderless 4x6’s for about $0.30 each)
4.) An "easy" button that I soldered a wire to and plugged into the gpio pin 17 and ground

My original idea was to shoot in raw+jpg as I wanted to keep the raw (.cr2) files from the camera for later editing, but I ran into an issue retrieving the resulting photo from gphoto2, so I switched to just raw and do the processing in the background while the pics are being taken.

## Setup

Any SLR camera that is supported by gphoto2 should work without any changes to the code. I think that’s most Canon and Nikons that do liveview.

Any printer should work, but you do have to manually configure it in CUPS.

I used the minimal install of Raspbian, this saves a lot of room on the SD card and keeps running processes to a minimum, as you are using the pi to do some fairly heavy image editing and don't need the xwindows system with pygame.

```shell
sudo apt-get update && apt-get install gphoto2 pygame python-pip sdl-config cups python-rpi.gpio python-pil python-gphoto2 python-cups ufraw-batch montage shutils

sudo vim /etc/cups/cupsd.conf
< add “Allow @local” to all of the location lines >
sudo /etc/init.d/cups restart
```

Plug your printer into the rpi and go to the cups web interface from another computer on your lan (https://<rpi IP address>:631/admin).
Add the printer to cups and set it as the default. I had to set it to do borderless prints.

If this is running as a photobooth, potentially at a venue, you're not going to want to have to ssh in or bring a keyboard and monitor to turn on the script. In this case, you'll want the photobooth to automatically start in the background when the pi starts. To do this, edit `/etc/rc.local` and the following before the `exit 0` line:

```shell
su - pi -c "/home/pi/pi-photobooth/start.sh &"
```

## Future updates that I’d like to see:
•	Liveview. I know this is possible with gphoto2, just need to figure out how to stream the liveview to pygame.
	```shell
  mkfifo fifo.mjpg
	gphoto2 --capture-movie --stdout> fifo.mjpg &
  ```
•	Fix the raw/jpg download and conversion. I’m sure this is just an issue with the gphoto2 commands, but I did read about a bug with pulling down images that are saved to the camera compared with taking a photo and saving it to the “client” (gphoto2)
•	Add a switch to go from raw mode to jpg mode (maybe query the camera to see what mode it’s in)
•	Switch out the GPIO python package to the newer version that doesn’t require sudo
