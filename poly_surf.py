import pygame
from pygame.locals import *
import numpy as np
from time import sleep
import time
import cmd
import sys
import os
import ast
import pixel_catcher
import subprocess
import threading
#import nature_article.psy_stim as psy_stim
import nature_article.sli_stim as sli_stim
import cv2
import psdthresh

pixc = pixel_catcher.pixel_catcher()
width = 400
height = 400

pygame.init()
window = pygame.display.set_mode((width,height), DOUBLEBUF)
screen = pygame.display.get_surface()

pygame.display.flip()

poly = []
col = ()
pos = ()

#stimp = psy_stim.stimulus()
stims = sli_stim.stimulus()

def grey(value, bot=0,top=150):
    return((value,value,value))

def draw_poly():
    global col, poly
    print("col", col)
    pygame.draw.polygon(screen, col, poly)
    pygame.display.flip()

def add_pos(pos):
    global poly, width, height
    p0 = max(0, pos[0])
    p0 = min(1, pos[0])
    p1 = max(0, pos[1])
    p1 = min(1, pos[1])

    p0 = p0 * width
    p1 = p1 * height

    poly.append((p0,p1)) 
    print("added pos", pos)

def colour_row(data, row=4, row_height=100):
    slate = cv2.imread('./nature_article/sphoto.png', cv2.IMREAD_COLOR)
    slate = data
    cv2.imwrite('sphoto.png', slate)

def take_line(mode, position):

    width = 1686
    height= 1060
    boxw = 100
    ppf = 1
    target_f = 15
    sample_f = 256

    if(mode == 'ud' or mode == 'du'):
        duration = (height-boxw)/(target_f*ppf)
        response = np.empty(int((height - 2*boxw) / ppf)) # 1450 pixels
    elif(mode == 'lr' or mode == 'rl'):
        duration = (width-boxw)/(target_f*ppf)
        response = np.empty(int((width - 2*boxw) / ppf)) # 1450 pixels
    else:
        print("direction must be in [lr,rl,ud,du]")
        return

    p1 = threading.Thread(target=stims.run, args = (duration,mode, position)).start()
    oldsampletime = pixc.samplingTime
    pixc.samplingTime = int(duration*sample_f)
    pixc.raw_cap = True
    pixc.active = True
    while(pixc.active):
        sleep(0.1)
    print("capture finished")

    raw = np.array(pixc.raw_result)
    print("eeg capture length", np.shape(raw), "calculating stimulus response...")
    starttime = stims.startstamp
    endtime = stims.endstamp

    samples_per_frame = (boxw * sample_f) / (ppf * target_f)
    samples_changed_per_frame = sample_f / target_f
    print("scpf:", samples_changed_per_frame)
    print("spf:", samples_per_frame)
    for i in range(np.size(response)):
        if(i*samples_changed_per_frame + samples_per_frame > np.size(raw)):
            print("response exceeded raw data range")
            break
        print("indexing eeg data: ", int(i*samples_changed_per_frame), ":", int(i*samples_changed_per_frame + samples_per_frame))
        response[i] = psdthresh.getstats15hz(raw[int(i*samples_changed_per_frame):int(i*samples_changed_per_frame + samples_per_frame)])
        print("resp:(iff no patern ->problem in response psds)", response[i])
    np.save('response.npy', response)
    pixc.samplingTime = oldsampletime

    if(mode == 'rl' or mode == 'du'):
        response = np.flip(response)

    newdata = np.empty((np.shape(response)[0],3))
    for i in range(np.size(response)):
        newdata[i] = grey(response[i]) 
    bob = np.tile(newdata, (boxw,1,1))
    ruth = np.swapaxes(bob,0,1)
    if(mode=='lr'):
        txt = './nature_article/take_1/no' + str(position) + 'lr.png'
    elif(mode=='rl'):
        txt = './nature_article/take_1/no' + str(position) + 'rl.png'
    elif(mode=='ud'):
        txt = './nature_article/take_1/no' + str(position) + 'ud.png'
    elif(mode=='du'):
        txt = './nature_article/take_1/no' + str(position) + 'du.png'
    if(mode=='ud' or mode=='du'): 
        cv2.imwrite(txt, ruth)
    else:
        cv2.imwrite(txt, bob)

    print("photo saved as", txt)

class commandline(cmd.Cmd):

    def do_EOF(self, line):
        print("got EOF")
        return True
    
    def do_quit(self, line):
        print("exiting")
        myMuse.connection.disconnect()
        myMuse.listen=False
        sys.exit()

    def do_q(self, line):
        self.do_quit(line)

    def do_poly(self, line):
        global poly
        try:
            poly_bounds = ast.literal_eval(line)
        except (ValueError, SyntaxError):
            print("gimme a list of points in form [(a1,a2), (b1,b2), ..., (w1,w2)]")
        else:
            print("adding polygon", poly_bounds)
            poly = poly_bounds
            
    def do_pos(self, line):
        global pos
        found = False
        while(not found):
            try:
                p = subprocess.Popen(['./tobii_reader'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
                result = p.stdout.readline().strip()
                pos = tuple(ast.literal_eval(result.decode("utf-8")))
            except SyntaxError:
                print("eyecatch couldn't find eyes")
            else:
                print(pos)
                add_pos(pos)
                found = True
    
    def do_add(self,line):
        global pos, poly, width, height
        p0 = max(0, pos[0])
        p0 = min(1, pos[0])
        p1 = max(0, pos[1])
        p1 = min(1, pos[1])

        p0 = p0 * width
        p1 = p1 * height

        poly.append((p0,p1))

    def do_fcust(self, line):
        global col
        try:
            colour = ast.literal_eval(line)
        except (ValueError, SyntaxError):
            print("gimme a list of points in form [(a1,a2), (b1,b2), ..., (w1,w2)]")
        else:
            print("filling er up with colour", colour)
            col = colour
            draw_poly()
     
    def do_f(self, line):
        global col, poly
        col = pixc.pixel_val
        try:
            draw_poly()
            poly = []
        except TypeError:
            print("invalid colour, select new colour with c")

    def do_stimsv(self, line):
        global stims
        try: 
            pix = ast.literal_eval(line)
        except(ValueError, SyntaxError):
            print("bad input, retry")
            return
        else:
            print("stim pixel:", pix)
        
        backup_images_cmd = 'tar -cf nature_article/backups/'+str(time.time()) + '.tar nature_article/take_1/'
        os.system(backup_images_cmd)
        
        take_line('ud', pix)
        sleep(5)
        take_line('du', pix)
        slate = cv2.imread('./nature_article/take_1/no' + str(pix) + 'ud.png', cv2.IMREAD_COLOR)
        slate2 = cv2.imread('./nature_article/take_1/no' + str(pix) + 'du.png', cv2.IMREAD_COLOR)
        slater = (slate + slate2) / 2 
        cv2.imwrite('./nature_article/take_1/no' + str(pix) + 'pass_2v.png', slater)
        print("photo saved: ./nature_article/take_1/no" + str(pix) + 'pass_2v.png')


    def do_stims(self, line):
        global stims
        try: 
            pix = ast.literal_eval(line)
        except(ValueError, SyntaxError):
            print("bad input, retry")
            return
        else:
            print("stim pixel:", pix)
        
        backup_images_cmd = 'tar -cf nature_article/backups/'+str(time.time()) + '.tar nature_article/take_1/'
        os.system(backup_images_cmd)
        
        take_line('lr', pix)
#        sleep(5)
#        take_line('rl', pix)
#        slate = cv2.imread('./nature_article/take_1/no' + str(pix) + 'lr.png', cv2.IMREAD_COLOR)
#        slate2 = cv2.imread('./nature_article/take_1/no' + str(pix) + 'rl.png', cv2.IMREAD_COLOR)
#        slater = (slate + slate2) / 2 
#        cv2.imwrite('./nature_article/take_1/no' + str(pix) + 'pass_2.png', slater)
#        print("photo saved: ./nature_article/take_1/no" + str(pix) + 'pass_2.png')


    def do_stimp(self, line):
        global stimp
        try: 
            pix = ast.literal_eval(line)
        except(ValueError, SyntaxError):
            print("this form for pixels: (a,b)")
        else:
            print("stim pixel:", pix)
            stimp.make_img(pix[0], pix[1])
#            stim.run(pixc.shutter_spd + 2)
            p1=threading.Thread(target=stimp.run, args = (int(pixc.shutter_spd + 3),)).start()
            sleep(2.5)
            pixc.active=True
            print("capture started")
            while(pixc.active):
                sleep(0.1)
            print("capture finished")
            colour = pixc.pixel_val
            print("colour val:", colour, "writing to image")
            img = cv2.imread("./nature_article/photo.png", cv2.IMREAD_COLOR)
            print(np.shape(img))
            img[pix[0]*stimp.pwid:(pix[0]+1)*stimp.pwid, pix[1]*stimp.phei:(pix[1]+1)*stimp.phei] = colour
            cv2.imwrite('./nature_article/photo.png', img)
            cv2.imwrite('./nature_article/saves/save'+str(time.time())+'.png', img)
        
    def do_save(self, line):
        try: 
            pygame.image.save(screen, line)
            print("saved image to", line)
        except:
            print("saving error, try again. did you specify a file?")

    oldst = pixc.samplingTime
    def do_set_shutter(self, line):
        
        try:
            newshut = int(line)
        except TypeError:
            print("ints only plz")
            return
        except ValueError:
            print("ints only plz")
            return
        
        pixc.shutter_spd = newshut
        pixc.samplingTime=int(pixc.samplingFreq*pixc.shutter_spd)
        print("set shutter speed to ", newshut)
        print("new frames/sample: ", pixc.samplingTime)

    def do_set_frequency(self, line):
        
        try:
#            newf = int(line)
            newf = float(line)
        except TypeError:
            print("ints only plz")
            return
        except ValueError:
            print("ints only plz")
            return
        
        pixc.target_f = newf
        print("set target frequency to ", newf)

    def do_set_iso(self, line):
        
        try:
            newiso = int(line)
        except TypeError:
            print("ints only plz")
            return
        except ValueError:
            print("ints only plz")
            return
        
        pixc.iso = newiso
        print("set iso to ", newiso)

    def do_capture(self, line):
        
        print("capturing...", line)
        pixc.active = True

    def do_info(self, line):
        global poly, col, pos
        print("-----INFO-----")
        print("shutter speed (s):", pixc.shutter_spd)
        print("target frequency:", pixc.target_f)
        print("iso:", pixc.iso)
        print("muse connected: ", pixc.myMuse.addr)
        print("shape:", poly)
        print("colour:", col)
        print("pos:", pos)
    
    def do_measure_connection(self,line):
        pixc.mode = 'rms'
        self.oldst = pixc.samplingTime
        pixc.samplingTime=int(pixc.samplingFreq*3)
        pixc.active = True
        print("entering connection test mode. press s to stop")
        print("Rule of thumb: (electrode aux on) rms <0.1 decent, <0.03 great")

    def do_connect_bg(self, line):
        pass

    def do_EOF(self, line):
        print("got EOF")
        return True
    
    def do_quit(self, line):
        print("exiting")
        pixc.myMuse.connection.disconnect()
        pixc.myMuse.listen=False
        sys.exit()

    def do_q(self, line):
        self.do_quit(line)

    def do_s(self, line):
        print("Exit measure mode")
        pixc.active = False
        pixc.samplingTime = self.oldst
        pixc.mode = 'capture'

    def do_c(self, line):
        self.do_capture(line)

    def do_mc(self,line):
        self.do_measure_connection(line)


commandline().cmdloop() 
