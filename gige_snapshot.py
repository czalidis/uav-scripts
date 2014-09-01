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
from PIL import Image


def take_snapshot():
  camera = aravis.Camera()

  if camera:
    print 'Found camera: %s' % camera.name

    # get max width and height
    width = camera.get_width_bounds()[1]
    height = camera.get_height_bounds()[1]

    # set max region
    camera.set_region(0, 0, width, height)
    
    print 'Taking snapshot %dx%d...' % (width, height)

    camera.start_acquisition()

    frame = camera.pop()

    im = Image.fromarray(frame)

    filename = '/images/' + time.strftime('%d-%m-%Y_%H-%M-%S') + '.jpg'

    im.save(filename)

    camera.stop_acquisition()

  del camera

if __name__ == '__main__':
  take_snapshot()
