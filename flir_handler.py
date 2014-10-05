#!/usr/bin/env python

# Copyright (c) 2014 Christos Zalidis 
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# 
# Author: Christos Zalidis <zalidis@gmail.com>

import time
import sys
import gps_controller
import gige_camera
import aravis
import image_exif
import RPi.GPIO as GPIO
import socket

FOLDER = '/images/'
EXTENSION = '.jpg'

try:
    # setup trigger, using GPIO
    pin = 12
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # setup gps client
    gpsc = gps_controller.GpsController()
    gpsc.start()

    while True:
        try:
            #raw_input('Press Enter to take snapshot')
            print 'Waiting for external trigger on pin %s...' % pin
            GPIO.wait_for_edge(pin, GPIO.FALLING)
            print 'BOOM!'

            # Test if we have a gps fix, if we don't, proceed
            if gpsc.fix.latitude == 0.0 or not gpsc.utc:
                 filename = FOLDER + time.strftime('%d-%m-%Y_%H-%M-%S') + EXTENSION
            else:
                # replace ':' with '-', so Windows understands the filename
                utc = gpsc.utc.replace(':', '-')
                filename = FOLDER + utc + EXTENSION
            
            # Take a frame using GigE Vision protocol
            frame = gige_camera.take_snapshot()

            # Save above frame to file
            gige_camera.save_image(frame, filename)
            
            # Test if we have a gps fix, if we don't, proceed
            if gpsc.fix.latitude !=  0.0 or gpsc.utc:
                # Set gps coordinates to image's exif
                image_exif.set_gps_location(filename, gpsc.fix.latitude, gpsc.fix.longitude, gpsc.fix.altitude, gpsc.utc)
        except KeyboardInterrupt:
            break
            
        except aravis.AravisException:
            print 'Error: No camera found!'
            # blink a led for 10 secs
            continue

except KeyboardInterrupt:
    print '\nAborting...'
    pass

except socket.error:
    print 'Error: GPS not found!'
    print 'Aborting...'
    # blink a led here
    sys.exit(1)

except:
    # blink a different led 
    raise

# stop gps controller
gpsc.stop_controller()
# wait for the tread to finish
gpsc.join()

# cleanup GPIO
GPIO.cleanup()

