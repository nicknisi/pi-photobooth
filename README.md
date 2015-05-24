# pi-photobooth

A Raspberry Pi Powered photobooth

This work is inspired by the [drumminhands_photobooth](https://github.com/drumminhands/drumminhands_photobooth) project.

## Goal

Control a DSLR (Canon Rebel T3i in my case) with a Raspberry Pi. The Pi will trigger the camera to snap pictures and then will upload them to a server that will display them and make them available for download.

## Setup

If this is running as a photobooth, potentially at a venue, you're not going to want to have to ssh in or bring a keyboard and monitor to turn on the script. In this case, you'll want the photobooth to automatically start in the background when the pi starts. To do this, edit `/etc/rc.local` and the following before the `exit 0` line:

```shell
/home/user/path/to/photobooth/start.sh &
```
