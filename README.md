# The Eye as a Camera

This is the group of scripts + img samples we collected from capturing human vision from EEG (using SSVEP at 12Hz).
This documentation covers the walkthrough for using this script to recreate your own images from EEG. You can read the full paper [here](https://drive.google.com/file/d/1bJjMUZSbjg48XHIoaQsqIHxOBN1tQ8ah/view?usp=sharing).

# What you'll need
1. A Muse2 EEG headset
2. A micro USB attached to an electrode (placed on the occipital lobe)

# How to use
1. Turn on the Muse and run `python poly_surf.py` in main dir. It will look for the MAC address for the Muse in the 'muse_MACs.py' file. You might have to run the lines bellow if the MAC address is not already on the list.
```
bluetooth ctl
scan on
connect XX:XX:XX:XX:XX:XX
```
2. A cmd should pop up after executing. This script performs 48 rasters across the image in 'nature_article/flashing_imgs/'. You manually enter which raster you would like to slide over with `stims X`, where `X` is a int or float. Ex: `stims 1.2... stims 1.4... stims 1.6...` until you have rastered the image 48 times. It can go by any interval, but intervales of 0.2 work best.
3. After rastering the image 48 times, run `combine_img.py` in the main dir. You can also run `weighted_av.py` to get a smoother, crisper image. The image will be generated in 'nature_article/raw_results/'. If using `weighted_av.py`, it will be generated in 'nature_article/transformed_results/'. 

# Important Notes
- You can change the image being rastered across in 'nature_article/flashing_imgs/'. The default is 'myface_hor.jpg'.
- All individual raster images are stored in 'nature_article/take_1/'. They are assembled and interpolated later to form one image.
- Backups are automatically stored in 'nature_article/backups'.
- You will probably have a headache trying to install all the packages required. There's a list of pip freezed packages [here](requirements.txt), but they are global packages and are not specific to this script, meaning 90% of them are useless for this application. If you have all of them installed, the script should run smoothly. Alternatively, you can keep trying to run it and install the missing packages until it works. Good luck! 

If you have any questions, email me at lukewpiette@gmail.com
