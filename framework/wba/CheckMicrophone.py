from testing import Test
from misctools import *
import time
import os
import pyaudio
import numpy as np
import math
import re
from scipy import signal
import matplotlib.pyplot as plt
from scipy.fftpack import fft

class CheckMicrophone(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check Microphone")

    def test(self):
        '''This function is to set the current station pls to the utc time stamp at the end of the test.'''
        exist = os.path.exists('./micro')
        if exist == False:
            try:
                os.makedirs("micro")
                self.logger.info( "fft data folder Created!")
            except IOError:
                self.logger.info(" fft folder create Error! Unable to creat the folder")
                return False
        ## ready to listen
        nb_point = 10000
        f0 = 5000
        self.dut.execute_command("power up micro")
        # self.dut.send_command("micro acquire %d"%(nb_point))
        self.dut.send_command("i2s acquire %d %d"%(f0,nb_point))
        self.logger.info("PLAY SOUND!!!")
        self.play_sound(2000,3)
        #w = chirpGen(3,44100,1000,12000)
        #play(w,44100)
        rc,text = self.dut.get_result(20000,prompt ="shell>",displayRX=False)

        # p= re.compile('\[I2S\] start(?P<fft>.*?)\[I2S\] stop',re.MULTILINE| re.DOTALL)
        p= re.compile("nb_samples = %d(?P<fft>.*?)rc=0"%nb_point,re.MULTILINE| re.DOTALL)
        m= p.search(text)
        if m:
            self.logger.info("Audio file found!!!")
            data = m.group('fft')
            with open("./micro/fft/data.txt","w") as f:
                f.write(data)
            data.strip()
            data_ = data.splitlines()
            self.logger.info("--%d---%s"%(len(data_),data_[0]))
            
            
            N = 4096
            audio = np.array(data_[2001:])
            # audio = audio/(2.**15)
            audio_fft = fft(audio,n = N)
            nyqui = math.ceil((N+1)/2)
            audio_fft = audio_fft[0:nyqui]
            mx = abs(audio_fft)/audio.size
            # mx =mx**2
            np.savetxt("./micro/fft/fft.txt",mx,delimiter=',')
            freqs = np.linspace(0,2500,nyqui)

            # d = len(audio)/2
            # audio_fft = abs(audio_fft[:(d-1)])
            plt.figure()
            plt.subplot(211)
            plt.plot(freqs, mx)
            plt.subplot(212)
            # plt.ylim(-10000000,10000000)
            plt.plot(audio)
            plt.show()
            '''
            index = audio.index(max_)
            frq = float(46000*(index/1024))
            self.logger.info("audio_frq point is %d, and value is %.2f"%(index, frq))
            mac = self.dut.getMac()
            with open("./fft/%s.csv"%(mac.replace(":","")),"w",newline='') as f:
                csvwriter = csv.writer(f, delimiter=',',quoting=csv.QUOTE_MINIMAL)
                for x in audio:
                    csvwriter.writerow([x])
            '''
            rt = 0
            ############################""


            
            ###############################
            return True if rt ==0 else False 
        else:
            self.logger.info("CSVFILE audio_frq [0.98;1.02] no_frq fail")
            return False
        
        
        
        
        
        id = configget("PLS_INFO","CURRENT_STATION_ID")
        current_utc = int(time.time())

        cmd_set_utc = "pls set %s %d"%(id,current_utc)
        r,text_ = self.dut.execute_command("pls set %s %d"%(id,current_utc),2000)
        if r != 0:
            self.logger.info( "CSVFILE pls_set_current_utc ok cmd_fail fail")
            return False
        else:
            self.logger.info( "CSVFILE pls_set_current_utc ok %d pass"%current_utc)
            return True
    def play_sound(self, f,duration):
        p = pyaudio.PyAudio()
        volume = 1.0     # range [0.0, 1.0]
        fs = 46000       # sampling rate, Hz, must be integer
        # duration = 6.0   # in seconds, may be float
        # f = 1000.0        # sine frequency, Hz, may be float

        # generate samples, note conversion to float32 array
        samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

        # for paFloat32 sample values must be in range [-1.0, 1.0]
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=fs,
                        output=True)
        # play. May repeat with different volume values (if done interactively)
        stream.write(volume*samples)
        stream.stop_stream()
        stream.close()
        p.terminate()

    def chirp_gen(self, duration, fs, Fstart, Fend):
        t = np.linspace(0, duration, fs*duration+1)
        w = signal.chirp(t, f0=Fstart, f1=Fend, t1=duration, method='quadratic')
        return w
    def play(self,y,fs):
        data = np.array(y, np.float32)
        data = (data / np.max(np.abs(data))).tostring()

        p = pyaudio.PyAudio()
        volume = 1
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=fs,
                        output=True)
        stream.write(data)
        stream.stop_stream()
        stream.close()
        p.terminate()