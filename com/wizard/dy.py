import numpy as np   
from matplotlib import pyplot as plt   
from matplotlib import animation   
import HuobiService as huobi
  
# first set up the figure, the axis, and the plot element we want to animate   
fig = plt.figure()   
ax = plt.axes()   
line, = ax.plot([], [], lw=2)   

test = huobi.get_kline('xrpusdt','1min',1200)
test['data'].reverse()

# initialization function: plot the background of each frame   
def init():   
    line.set_data([], [])   
    return line,   
  
# animation function.  this is called sequentially   
x = [0] 
y = [0] 
def animate(i):   
    
    x.append(i) 
    y.append(test['data'][i]['close']) 
    line.set_data(x, y)   
    return line,   
  
# call the animator.  blit=true means only re-draw the parts that have changed.   
anim = animation.FuncAnimation(fig, animate, init_func=init,   
                                 interval=20, blit=True)   
  
# save the animation as an mp4.  this requires ffmpeg or mencoder to be  
# installed.  the extra_args ensure that the x264 codec is used, so that  
# the video can be embedded in html5.  you may need to adjust this for   
# your system: for more information, see   
# http://matplotlib.sourceforge.net/api/animation_api.html   
  
plt.show()  