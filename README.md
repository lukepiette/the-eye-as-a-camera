# The Eye as a Camera

This is the group of scripts + img samples we collected from capturing human vision from EEG (using SSVEP at 12Hz).
This documentation covers the walkthrough for using this script to recreate your own images from EEG. You can read the full paper [here](https://drive.google.com/file/d/1bJjMUZSbjg48XHIoaQsqIHxOBN1tQ8ah/view?usp=sharing).

# What you'll need
1. A Muse2 EEG headset
2. A micro USB attached to an electrode (placed on the occipital lobe)

# How to use
1. Run `python poly_surf.py` in dir. It will look for the MAC address for the Muse in the 'muse_MACs.py' file. You might have to run:
```
bluetooth ctl
scan on
connect XX:XX:XX:XX:XX:XX
```
if the MAC address is not already on the list.

