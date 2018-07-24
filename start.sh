#!/bin/sh

BASEDIR=$(dirname $0)

# make sure the photo directories exist
mkdir -p $BASEDIR/photos
mkdir -p $BASEDIR/.photos
mkdir -p $BASEDIR/my_photos
mkdir -p $BASEDIR/combined_photos

# remove any existing photos that may exist in the temp directory
# rm $BASEDIR/.photos/*.jpg

# give it a bit of time... 
sleep 6

# start up the photobooth
until `sudo python $BASEDIR/photobooth.py >> $BASEDIR/output.log`; do
    echo "Server crashed with exit code $?.  Respawning.." >&2
    sleep 1
done
