from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from trace import Load_Whiskers
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip
import os

try:
    os.makedirs("images")
except OSError:
    pass

print('Loading whiskers')
wv = Load_Whiskers('../../../bin/whisk/realtest.whiskers')
#wv = Load_Whiskers('../../../../whiskdata/test.whiskers')

print('Loading file')
clip = VideoFileClip('../../../../whiskdata/whiskitest.mp4')
#clip = VideoFileClip('../../../../whiskdata/movie.mp4')
print('Clip length:', clip.duration*clip.fps)
print('Whisker length:', len(wv))

for frame in range(100):
    print("Showing frame", frame)
    fig = plt.figure()
    fig.set_size_inches(6, 5)
    fig.set_dpi(56)
    ax = fig.add_axes([0.,0.,1.,1.])
    ax.axis('off')
    #ax.set_axis_off()
    #fig.add_axes(ax)

    for w in wv[frame]:
        if (min(wv[frame][w].x)+max(wv[frame][w].x))/2<149 and (min(wv[frame][w].y)+max(wv[frame][w].y))/2<82:
            continue
        ax.plot(wv[frame][w].x, wv[frame][w].y, color='white')

    plt.xlim([0,335])
    plt.ylim([0,279])
    fig.set_facecolor('black')
    plt.gca().invert_yaxis()
    plt.imshow(clip.get_frame(frame/clip.fps)//2)
    #plt.show()


    plt.savefig(os.path.join("images", str(frame)+".png"), facecolor=fig.get_facecolor(), dpi=56)
