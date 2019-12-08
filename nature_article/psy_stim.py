from psychopy import visual, core, monitors, event, clock, logging
import numpy as np
import cv2
import math

class stimulus():

    def __init__(self):
        self.xpix = 33 / 2
        self.ypix = 19 / 2
        self.width = 1650
        self.height = 950
        self.pwid = int(self.width/self.xpix)
        self.phei = int(self.height/self.ypix)
        self.freq = 1/15
        self.fpstim = 60*self.freq 


    def make_img(self, xp, yp):

        noa = cv2.imread("noa.png", cv2.IMREAD_COLOR)
        nob = cv2.imread("nob.png", cv2.IMREAD_COLOR)
        
        noaval = np.array(noa[xp*self.pwid:(xp+1)*self.pwid, yp*self.phei:(yp+1)*self.phei])
        noa[:,:] = (30,30,30)
        noa[xp*self.pwid:(xp+1)*self.pwid, yp*self.phei:(yp+1)*self.phei] = noaval

        nobval = np.array(nob[xp*self.pwid:(xp+1)*self.pwid, yp*self.phei:(yp+1)*self.phei])
        nob[:,:] = (30,30,30)
        nob[xp*self.pwid:(xp+1)*self.pwid, yp*self.phei:(yp+1)*self.phei] = nobval

        cv2.imwrite('pa.png', noa)
        cv2.imwrite('pb.png', nob)

    def run(self, duration):
        win = visual.Window(size = (self.width,self.height), units='pix')
        win.recordFrameIntervals = True
        win.waitBlanking=True
        win.allowGUI = True
        win.mouseVisible = True
        durationframes = duration*60


        a = visual.ImageStim(win, image='pa.png', pos=(0, 0), size=(self.width, self.height))
        b = visual.ImageStim(win, image='pb.png', pos=(0, 0), size=(self.width, self.height))
        

        # Run for specified duration.
        for i in range(durationframes):
            # Check if user wants to quit
            keys_pressed = event.getKeys()
            if keys_pressed and keys_pressed[0] == 'q':
                win.close()
                core.quit()
                return 1

            if math.floor(i/self.fpstim) % 2 == 0:
                a.draw()

            elif math.floor(i/self.fpstim) % 2 == 1:
                b.draw()

            # Go to next frame
            win.flip()

        win.close()

instance = stimulus()
#instance.make_img(5,4)
instance.run(30)
