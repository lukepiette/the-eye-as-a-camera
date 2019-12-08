import muse2
import threading
import numpy as np
import time
import muse_MACs
from datetime import datetime

class blink_finder():
    def __init__(self):
        self.count = 0

        self.myMuse = muse2.Muse(callback=self.eeg, address=muse_MACs.myaddress)
        self.p1=threading.Thread(target=self.myMuse.runListener).start()
        print("setup complete")

    def eeg(self, data, trash=False):
        for i in range(12):
            if(data[0][i] < -150):
                self.count += 1
            elif(self.count > 0):
                print("blink! time: ", datetime.now().strftime("%s, %f"), "width(ms):", self.count*4)
                self.count = 0

bob = blink_finder()

