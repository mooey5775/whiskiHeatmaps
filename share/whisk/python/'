from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from trace import Load_Whiskers
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from moviepy.editor import VideoFileClip
from multiprocessing import Pool

import os
import random
from tqdm import tqdm

sessions = ['181214_001', '181213_001', '181004_001', '180905_001']
useSplit = 0.025
testSplit = 0.2

traceExe = '/Users/edwardli/Documents/Code/mice/whisk-1.1.0d-Darwin/bin/whisk/trace'
sessionDir = '/Volumes/sawtell_loco-locker/obstacleData/sessions'
processedWhiskers = '/Users/edwardli/Documents/Code/mice/whiskdata/processedWhiskers'
saveDir = '/Users/edwardli/Documents/Code/mice/whiskdata/images'

def processSession(session):
    print('Processing session', session)
    try:
        os.makedirs(os.path.join(processedWhiskers, session))
    except OSError:
        pass
    os.chdir(os.path.join(processedWhiskers, session))
    if os.path.exists('runWisk.mp4'):
        print('Cut video exist, skipping')
    else:
        print('Choosing session split')
        lenClip = VideoFileClip(os.path.join(sessionDir, session, 'runWisk.mp4'))
        starttime = (random.random()*0.6+0.15)*lenClip.duration
        runtime = useSplit*lenClip.duration
        lenClip.close()
        print('Cutting video starting at', starttime, 'for', runtime, 'seconds')
        os.system('ffmpeg -i '+os.path.join(sessionDir, session, 'runWisk.mp4')+' -acodec copy -vcodec copy -ss '+str(starttime)+' -t '+str(runtime)+' runWisk.mp4')
    if os.path.exists('analyzed.whiskers'):
        print('Whisker analysis exists, skipping')
    else:
        print('Analyzing whisker data')
        os.system(traceExe+' runWisk.mp4 analyzed.whiskers')
    print('Loading whiskers')
    wv = Load_Whiskers('analyzed.whiskers')
    print('Loading video')
    clip = VideoFileClip('runWisk.mp4')
    print('Clip length:', clip.duration*clip.fps)
    print('Whisker length:', len(wv))
    print('Exporting whisker images')
    if not os.path.exists(os.path.join(saveDir, 'labels', 'train')):
        os.makedirs(os.path.join(saveDir, 'labels', 'train'))
    if not os.path.exists(os.path.join(saveDir, 'labels', 'test')):
        os.makedirs(os.path.join(saveDir, 'labels', 'test'))
    if not os.path.exists(os.path.join(saveDir, 'data', 'train')):
        os.makedirs(os.path.join(saveDir, 'data', 'train'))
    if not os.path.exists(os.path.join(saveDir, 'data', 'test')):
        os.makedirs(os.path.join(saveDir, 'data', 'test'))


    for frame in tqdm(range(len(wv))):
        fig = plt.figure()
        fig.set_size_inches(6, 5)
        fig.set_dpi(56)
        ax = fig.add_axes([0.,0.,1.,1.])
        ax.axis('off')

        for w in wv[frame]:
            if (min(wv[frame][w].x)+max(wv[frame][w].x))/2<149 and (min(wv[frame][w].y)+max(wv[frame][w].y))/2<82:
                continue
            ax.plot(wv[frame][w].x, wv[frame][w].y, color='white')

        plt.xlim([0,335])
        plt.ylim([0,279])
        fig.set_facecolor('black')
        plt.gca().invert_yaxis()
        if random.random()<testSplit:
            plt.savefig(os.path.join(saveDir, 'labels', 'test', session+"-"+str(frame)+".png"), facecolor=fig.get_facecolor(), dpi=56)
            mpimg.imsave(os.path.join(saveDir, 'data', 'test', session+"-"+str(frame)+".png"), clip.get_frame(frame/clip.fps))
        else:
            plt.savefig(os.path.join(saveDir, 'labels', 'train', session+"-"+str(frame)+".png"), facecolor=fig.get_facecolor(), dpi=56)
            mpimg.imsave(os.path.join(saveDir, 'data', 'train', session+"-"+str(frame)+".png"), clip.get_frame(frame/clip.fps))
        plt.close(fig)
    clip.close()

pool = Pool(processes=4)
pool.map(processSession, sessions)
