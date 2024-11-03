This is for the TEZBA Platine

In the firmware the uf2 file is located to init the raspberry pi pico
In the examples folder there are the test program to use

To create a uf2 file, copy all the content from the uf2template folder when not in the bootloader mode and
with the help of the picotool do

  picotool save --all tezba.uf2
