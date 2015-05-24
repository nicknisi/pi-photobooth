#!/bin/sh

BASEDIR=$(dirname $0)

# make sure the photo directories exist
mkdir -p $BASEDIR/photos
mkdir -p $BASEDIR/.photos

# give it a bit of time... 
sleep 6

# start up the photobooth
sudo python $BASEDIR/photobooth.py
