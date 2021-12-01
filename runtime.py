#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

thread1 = sys.argv[1]
thread2 = sys.argv[2]
thread3 = sys.argv[3]
keywords = "sum_exec_runtime"
time_interval = 60000 # min

def read_sum_exec_runtime(pid,keyword):
    runtime = 0
    with open('/proc/'+str(pid)+'/sched') as procf:
        for line in procf.readlines():
            if keyword in line:
                runtime = float((line.split(':')[1]).strip())
    #print("pid:", pid, "runtime:", "%.2f" % runtime)
    return runtime

def time_plot(x, y, y1, y2, y3):
    plt.cla()
    plt.title(keywords)
    plt.xlabel("time(min)")
    plt.ylabel("runtime(ms)")
    plt.plot(x, y, color='b', label="real time", linewidth=1, linestyle='dashed')
    plt.plot(x, y1, color='g', label=thread1, linewidth=1)
    plt.plot(x, y2, color='y', label=thread2, linewidth=1)
    plt.plot(x, y3, color='r', label=thread3+"-vcpu", linewidth=1)
    plt.legend()

xtime = 0
ytime = 0
y1time0 = read_sum_exec_runtime(thread1, keywords)
y2time0 = read_sum_exec_runtime(thread2, keywords)
y3time0 = read_sum_exec_runtime(thread3, keywords)
xdata, ydata, y1data, y2data, y3data = [], [], [], [], []

def animate(i):
    global xtime, ytime, y1time0, y2time0, y3time0
    xtime += 1
    ytime += time_interval #ms
    y1time = read_sum_exec_runtime(thread1, keywords) - y1time0
    y2time = read_sum_exec_runtime(thread2, keywords) - y2time0
    y3time = read_sum_exec_runtime(thread3, keywords) - y3time0
    xdata.append(xtime)
    ydata.append(ytime)
    y1data.append(y1time)
    y2data.append(y2time)
    y3data.append(y3time)
    time_plot(xdata, ydata, y1data, y2data, y3data)

anim = FuncAnimation(plt.figure(), animate, frames=None, interval=time_interval)
plt.show()
#plt.savefig("CFS-"+thread3+"-vcpu.png",dpi=300)
#anim.save('runtime.gif', writer='imagemagick', fps=1)
