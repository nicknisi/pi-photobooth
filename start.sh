#!/bin/sh

BASEDIR=$(dirname $0)

# make sure the photo directories exist
mkdir -p $BASEDIR/photos
mkdir -p $BASEDIR/.photos

# remove any existing photos that may exist in the temp directory
# rm $BASEDIR/.photos/*.jpg

# give it a bit of time... 
sleep 6

# start up the photobooth
sudo python $BASEDIR/photobooth.py
