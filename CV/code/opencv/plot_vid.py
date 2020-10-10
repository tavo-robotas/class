import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

df = pd.DataFrame({"time": np.linspace(0,20, num=100),
                   "force" : np.cumsum(np.random.randn(100))})

def grab_frame(cap):
    ret,frame = cap.read()
    return frame # or cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

#Initiate
vidcap = cv2.VideoCapture(0)
# vidcap.set(1,590)

fig, (ax,ax2) = plt.subplots(ncols=2,figsize=(20, 10))

x=df["time"][7:100]
y=df["force"][7:100]

#create two image plots
im1 = ax.imshow(grab_frame(vidcap),extent=[0,200,0,100], aspect='auto')
line, = ax2.plot(x[0:1],y[0:1],'or')
ax2.set_xlim(x.min(), x.max())
ax2.set_ylim(y.min(), y.max())

def update(i):
    im1.set_data(grab_frame(vidcap))
    line.set_data(x[0+i:1+i],y[0+i:1+i])
    return im1, line


ani = FuncAnimation(fig, update, frames=len(x), interval=1, blit=True)
plt.show()