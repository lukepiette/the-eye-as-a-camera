import numpy as np
import scipy.stats
import sys

def calculatePSD(array,sample_f):
    ps = np.abs(np.fft.fft(array))**2

    time_step = 1 / sample_f 
    freqs = np.fft.fftfreq(array.size, time_step)
    idx = np.argsort(freqs)

    return freqs[idx], ps[idx], idx

def filter1of(psd):
    logpsd = np.log(psd)
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(freq,logpsd)
    sublogpsd = logpsd - (slope*freq + intercept)
    psdnew = np.exp(sublogpsd)
    return psdnew


def getstats(array, sample_f=256, stim_f=12):
    if(stim_f == 15):
        return(getstats15hz(array, sample_f))
    elif(stim_f==20):
        return(getstats20hz(array,sample_f))
    elif(stim_f==14):
        return(getstats14hz(array, sample_f))
    elif(stim_f == 15.25):
        return(getstats1525hz(array, sample_f))
    elif(stim_f!=12):
        print("Nope")
        sys.exit()   
    freq,psd,idx=calculatePSD(array, sample_f=sample_f);
    psd=psd[freq>11];
    freq=freq[freq>11];
    psd = psd[freq<50]
    freq = freq[freq<50]    
    #psd = filter1of(psd)
    avg=np.average(psd);
    id1=np.where(freq>11.9);
    id2=np.where(freq>12.1);
    psdband=psd[id1[0][0]:id2[0][0]];
    maxval=np.max(psdband)
    maxindex=np.where(psd==maxval);
    divide = maxval/avg
    
    return divide 

def getstats14hz(array, sample_f=256):
        
    freq,psd,idx=calculatePSD(array, sample_f=sample_f);
    psd=psd[freq>13];
    freq=freq[freq>13];
    psd = psd[freq<50]
    freq = freq[freq<50]    
   # psd = filter1of(psd)
    avg=np.average(psd);
    
    id1=np.where(freq>13.9);
    id2=np.where(freq>14.1);
    psdband=psd[id1[0][0]:id2[0][0]];
    peak15=np.max(psdband)
    
#    id1=np.where(freq>29.9);
#    id2=np.where(freq>30.1);
#    psdband=psd[id1[0][0]:id2[0][0]];
#    peak30=np.max(psdband)
    
    peaksum = peak15 #+ peak30
    
    divide = peaksum/avg
    
    return divide
 
def getstats1525hz(array, sample_f=256):
        
    freq,psd,idx=calculatePSD(array, sample_f=sample_f);
    psd=psd[freq>13];
    freq=freq[freq>13];
    psd = psd[freq<50]
    freq = freq[freq<50]    
   # psd = filter1of(psd)
    avg=np.average(psd);
    
    id1=np.where(freq>15.15);
    id2=np.where(freq>15.35);
    psdband=psd[id1[0][0]:id2[0][0]];
    peak15=np.max(psdband)
    
#    id1=np.where(freq>29.9);
#    id2=np.where(freq>30.1);
#    psdband=psd[id1[0][0]:id2[0][0]];
#    peak30=np.max(psdband)
    
    peaksum = peak15 #+ peak30
    
    divide = peaksum/avg
    
    return divide

"""for 15Hz. Also includes 2nd harmonic and 1/f filtering"""
def getstats15hz(array, sample_f=256):
        
    freq,psd,idx=calculatePSD(array, sample_f=sample_f);
    psd=psd[freq>14];
    freq=freq[freq>14];
    psd = psd[freq<50]
    freq = freq[freq<50]    
   # psd = filter1of(psd)
    avg=np.average(psd);
    
    id1=np.where(freq>14.9);
    id2=np.where(freq>15.1);
    psdband=psd[id1[0][0]:id2[0][0]];
    peak15=np.max(psdband)
    
    id1=np.where(freq>29.9);
    id2=np.where(freq>30.1);
    psdband=psd[id1[0][0]:id2[0][0]];
    peak30=np.max(psdband)
    
    peaksum = peak15 + peak30
    
    divide = peaksum/avg
    
#    from time import sleep
#    import mne
#    channels = 1
#    info = mne.create_info(channels,sample_f,['eeg'],montage='standard_1005')
#    custom_raw = mne.io.RawArray(array, info);
#    custom_raw.plot_psd(fmin=14,fmax=50,area_mode='range')
#    sleep(1)

    return divide
    
def getstats20hz(array, sample_f=256):
        
    freq,psd,idx=calculatePSD(array, sample_f=sample_f);
    psd=psd[freq>14];
    freq=freq[freq>14];
    psd = psd[freq<50]
    freq = freq[freq<50]    
   # psd = filter1of(psd)
    avg=np.average(psd);
    
    id1=np.where(freq>19.9);
    id2=np.where(freq>20.1);
    psdband=psd[id1[0][0]:id2[0][0]];
    peak20=np.max(psdband)
    
    id1=np.where(freq>39.9);
    id2=np.where(freq>40.1);
    psdband=psd[id1[0][0]:id2[0][0]];
    peak40=np.max(psdband)
    

    peaksum = peak20 + peak40
    
    divide = peaksum/avg
    
    return divide
 
def test_window(present, absent):
    for window_size in range(1,20):
        numsplits = np.shape(present)[1] / ( 256.0 * window_size )
        bob = np.array_split(present, numsplits, axis=1)
        bobdiv = getstats(bob)
        

