#!/usr/bin/python3
import sys
import psutil
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

time_interval = 10000 # 10s
threads = sys.argv

def usage():
    print("usage:", threads[0], "<pid1 [pid2 ... pid5]>")

if (len(threads) < 2) or (len(threads) > 5) or (sys.argv[1] == "-h"):
    usage()
    exit(1)

del(threads[0])
cpuid = []
for i in range(len(threads)):
    cpuid.append([])

xtime = 0;
xdata = []
styles = ["dashed", "dashdot", "dotted", "solid"]
markers = ["+","*","x","v"]
colors = ["b","g","r","y"]

def time_plot(time, cpuid):
    global styles
    plt.cla()
    plt.title("threads-cpu-id")
    plt.xlabel("time(10s)")
    plt.ylabel("cpu-id")
    plt.yticks(range(psutil.cpu_count()))
    for i in range(len(threads)):
        #if(i == 2):
        #    plt.plot(time, cpuid[i], label=threads[i]+"-vcpu", color=colors[i], marker=markers[i], linewidth=1, linestyle=styles[i])
        #else:
            plt.plot(time, cpuid[i], label=threads[i], color=colors[i], marker=markers[i], linewidth=1, linestyle=styles[i])
    plt.legend()

def animate(j):
    global xtime, xdata
    for i in range(len(threads)):
        p = psutil.Process(int(threads[i]))
        cpuid[i].append(p.cpu_num())
    
    xtime += 1
    xdata.append(xtime)
    #print(cpuid)
    time_plot(xdata, cpuid)

anim = FuncAnimation(plt.figure(), animate, frames=None, interval=time_interval)
plt.show()
