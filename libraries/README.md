# Installing libraries

## aravis

You can find detailed instructions on how to configure and compile the aravis 
library [here](https://github.com/sightmachine/SimpleCV/wiki/Aravis-(Basler)-GigE-Camera-Install-Guide).
If you encounter any problems during compilation, you should check if the `libgirepository1.0-dev` package is
installed, which is not mentioned in the prerequisites. Note that compilation could take a lot of time
on a Raspberry Pi.


## python-aravis

Since `python-aravis` is a python module, you can install it using the standard way. 
Run inside the `python-aravis` folder:
```
sudo python setup.py install
```

## Other dependencies

```
sudo apt-get install gpsd gpsd-clients python-gps python-pyexiv2 python-pip libjpeg8 libjpeg8-dev
sudo pip install Pillow
```
