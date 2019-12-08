"""Takes 1-pixel photos given an eeg stream, stimulus frequency, shutter speed, etc"""

import psdthresh



def _grey(value, bot=0,top=150):
    return((value,value,value))

def bulb(data, shutter_speed, target_f, iso_anlg_top, data_fr=256, raw_out=False):
    useful_data = data[:shutter_speed*data_fr]
    photoquantity = psdthresh.getstats(useful_data, sample_f=data_fr, stim_f = target_f)
    if(raw_out):
        return photoquantity
    else:
        # convert to 8-bit rgb colour
        return _grey(int((photoquantity / iso_anlg_top) * 255))
