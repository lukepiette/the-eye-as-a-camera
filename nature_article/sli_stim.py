from time import sleep
import time
import pygame
from pygame.locals import *
import numpy as np
import cv2
import math

class stimulus():

    def __init__(self, ppf = 1):
        self.xpix = 33 / 2
        self.ypix = 19 / 2
        self.width = 1686
        self.height = 1060
        self.boxsize = 100
        self.pwid = int(self.width/self.xpix)
        self.phei = int(self.height/self.ypix)
        self.freq = 1/15
        self.noa = pygame.image.load('./nature_article/flashing_imgs/myface_hor.jpg')
        self.nob = pygame.image.load('./nature_article/flashing_imgs/img2.jpg')
        self.xpos = 5*self.pwid
        self.ypos = 5*self.phei

        pygame.init()
        self.window = pygame.display.set_mode((self.width,self.height), DOUBLEBUF)
        self.screen = pygame.display.get_surface()
        self.ppf = ppf

        self.startstamp = None
        self.endstamp = None

    def close(self):
        pygame.display.quit()
        pygame.quit()

    def run(self, duration, mode='lr', position=0):
        durationframes = int(duration / self.freq)
        

        a = pygame.surfarray.array3d(self.noa)
        b = pygame.surfarray.array3d(self.nob)
        print("made surfaces")
 
        pygame.display.flip()
        prevtime = time.time()
        sleep(self.freq)
        
        self.startstamp = time.time()       
        

        if(mode=='lr'):
            # run for specified duration.
            for i in range(durationframes):

                while(time.time() - prevtime < self.freq):
                    sleep(0.00001)

                prevtime = time.time()

                if i % 2 ==0:
                    piece = a[int(i*self.ppf):int(i*self.ppf+self.boxsize),int(self.boxsize*position):int(self.boxsize*position+self.boxsize)]
                    surf = pygame.surfarray.make_surface(piece)

                    self.window.blit(surf, (i*self.ppf,int(self.boxsize*position)))
#                    self.window.blit(surf, (500,500))
                    pygame.display.update()

                elif i % 2 ==1:
                    piece = b[int(i*self.ppf):int(i*self.ppf+self.boxsize),int(self.boxsize*position):int(self.boxsize*position+self.boxsize)]
                    surf = pygame.surfarray.make_surface(piece)

                    self.window.blit(surf, (i*self.ppf,int(self.boxsize*position)))
#                    self.window.blit(surf, (500,500))
                    pygame.display.update()

#                patrick = np.array([(100,100,200)])
#                patricksurfsthewave = pygame.surfarray.make_surface(patrick)
#                self.window.blit(patricksurfsthewave, (540,540))
#                pygame.display.update()
                bob = np.array([(50,50,90)])
                bobsurfsthewave = pygame.surfarray.make_surface(bob)
                self.window.blit(bobsurfsthewave, (i*self.ppf + self.boxsize / 2, int(self.boxsize*position + self.boxsize / 2)))
                pygame.display.update()

        elif(mode=='rl'):
             # run for specified duration.
            for i in reversed(range(durationframes)):

                while(time.time() - prevtime < self.freq):
                    sleep(0.00001)

                prevtime = time.time()

                if i % 2 ==0:
                    piece = a[int(i*self.ppf):int(i*self.ppf+self.boxsize),self.boxsize*position:self.boxsize*position+self.boxsize]
                    surf = pygame.surfarray.make_surface(piece)

                    self.window.blit(surf, (i*self.ppf,self.boxsize*position))
                    pygame.display.update()

                elif i % 2 ==1:
                    piece = b[int(i*self.ppf):int(i*self.ppf+self.boxsize),self.boxsize*position:self.boxsize*position+self.boxsize]
                    surf = pygame.surfarray.make_surface(piece)

                    self.window.blit(surf, (i*self.ppf,self.boxsize*position))
                    pygame.display.update()

                bob = np.array([(50,50,90)])
                bobsurfsthewave = pygame.surfarray.make_surface(bob)
                self.window.blit(bobsurfsthewave, (i*self.ppf + self.boxsize / 2, self.boxsize*position + self.boxsize / 2))
                pygame.display.update()

        elif(mode=='ud'):
            for i in range(durationframes):

                while(time.time() - prevtime < self.freq):
                    sleep(0.00001)

                prevtime = time.time()

                if i % 2 ==0:
                    piece = a[self.boxsize*position:self.boxsize*position+self.boxsize, int(i*self.ppf):int(i*self.ppf+self.boxsize)]
                    surf = pygame.surfarray.make_surface(piece)

                    self.window.blit(surf, (self.boxsize*position, i*self.ppf))
                    pygame.display.update()

                elif i % 2 ==1:
                    piece = b[self.boxsize*position:self.boxsize*position+self.boxsize, int(i*self.ppf):int(i*self.ppf+self.boxsize)]
                    surf = pygame.surfarray.make_surface(piece)

                    self.window.blit(surf, (self.boxsize*position, i*self.ppf))
                    pygame.display.update()

                bob = np.array([(50,50,90)])
                bobsurfsthewave = pygame.surfarray.make_surface(bob)
                self.window.blit(bobsurfsthewave, (self.boxsize*position + self.boxsize / 2, i*self.ppf + self.boxsize / 2))
                pygame.display.update()

        elif(mode == 'du'):
            for i in reversed(range(durationframes)):

                while(time.time() - prevtime < self.freq):
                    sleep(0.00001)

                prevtime = time.time()

                if i % 2 ==0:
                    piece = a[self.boxsize*position:self.boxsize*position+self.boxsize, int(i*self.ppf):int(i*self.ppf+self.boxsize)]
                    surf = pygame.surfarray.make_surface(piece)

                    self.window.blit(surf, (self.boxsize*position, i*self.ppf))
                    pygame.display.update()

                elif i % 2 ==1:
                    piece = b[self.boxsize*position:self.boxsize*position+self.boxsize, int(i*self.ppf):int(i*self.ppf+self.boxsize)]
                    surf = pygame.surfarray.make_surface(piece)

                    self.window.blit(surf, (self.boxsize*position, i*self.ppf))
                    pygame.display.update()

                bob = np.array([(50,50,90)])
                bobsurfsthewave = pygame.surfarray.make_surface(bob)
                self.window.blit(bobsurfsthewave, (self.boxsize*position + self.boxsize / 2, i*self.ppf + self.boxsize / 2))
                pygame.display.update()


   

        self.endstamp = time.time()
        print("stim done")
##instance = stimulus()
#instance.run(39)

