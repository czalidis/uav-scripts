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

import aravis
import time
import os
from PIL import Image
import numpy

def take_snapshot(config=None):
    camera = aravis.Camera()

    if camera:

        print 'Found camera: %s' % camera.name

        if config is not None and config['frame_bit_depth'] == 14:
            camera.set_feature('PixelFormat', 'Mono14')
            camera.set_feature('DigitalOutput', 'bit14bit')

        # get max width and height
        width = camera.get_width_bounds()[1]
        height = camera.get_height_bounds()[1]

        # set max region
        camera.set_region(0, 0, width, height)
        
        print 'Taking snapshot %dx%d...' % (width, height)

        camera.start_acquisition()

        frame = camera.pop()
        
        camera.stop_acquisition()

    return frame

def save_image(frame, filename, config=None):
    save_normalized = False
    if config is None:
        image = Image.fromarray(frame)
    else:
        if config['frame_bit_depth'] == 14:
            if config['out_image']['depth'] == 16:
                image = Image.fromarray(frame, 'I;16')
                save_normalized = config['out_image']['save_normalized']
            else:
                # scale image to 8-bits
                scaled_frame = numpy.copy(frame)
                min_value = config['out_image']['scale_min']
                max_value = config['out_image']['scale_max']
                scaled_frame -= min_value
                scaled_frame *= (255.0 / (max_value - min_value))
                image = Image.fromarray(numpy.clip(scaled_frame, 0, 255).astype('uint8'))
        else:
            image = Image.fromarray(frame)

    print 'Saving to ' + filename + '...'
    image.save(filename)

    # save a normalized copy; 16-bit also
    if save_normalized:
       norm_frame = numpy.copy(frame)
       frame_min = frame.min()
       frame_max = frame.max()
       norm_frame -= frame_min
       norm_frame *= (65535.0 / (frame_max - frame_min))
       norm_image = Image.fromarray(norm_frame, 'I;16')

       # save the normalized image with a -norm before extension
       path = os.path.splitext(filename)
       norm_image.save(path[0] + '-norm' + path[1])

if __name__ == '__main__':
    save_image(take_snapshot(), '/images/' + time.strftime('%d-%m-%Y_%H-%M-%S') + '.jpg')
