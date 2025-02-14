import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import serial
import time
from collections import deque
import numpy as np

# 시리얼 포트 설정
# ser = serial.Serial('/dev/cu.usbserial-14210', 115200) 
ser2 = serial.Serial('/dev/cu.usbserial-14110', 115200) 
time.sleep(2)

history_x = deque(maxlen=10)
history_y = deque(maxlen=10)
history_z = deque(maxlen=10)

smooth_x = deque(maxlen=50)
smooth_y = deque(maxlen=50)
smooth_z = deque(maxlen=50)

fig = plt.figure(figsize=(12, 6))

ax1 = fig.add_subplot(121, projection='3d')
ax1.set_title("Original Data (Raw Magnetic Field)")
ax1.set_xlabel("X (mT)")
ax1.set_ylabel("Y (mT)")
ax1.set_zlabel("Z (mT)")
ax1.set_xlim(-1.2, 1.2)
ax1.set_ylim(-1.2, 1.2)
ax1.set_zlim(-1.2, 1.2)

ax2 = fig.add_subplot(122, projection='3d')
ax2.set_title("Smoothed Data (Moving Average)")
ax2.set_xlabel("X (mT)")
ax2.set_ylabel("Y (mT)")
ax2.set_zlabel("Z (mT)")
ax2.set_xlim(-1.2, 1.2)
ax2.set_ylim(-1.2, 1.2)
ax2.set_zlim(-1.2, 1.2)

def moving_average(data, window_size=10):
    return np.mean(data) if len(data) >= window_size else np.mean(data[:len(data)])

def update_plot():
    try:
        line = ser2.readline().decode().strip()
        magX, magY, magZ = map(float, line.split(","))
        print(f"X: {magX}, Y: {magY}, Z: {magZ}") 

        history_x.append(magX)
        history_y.append(magY)
        history_z.append(magZ)

        smooth_x.append(moving_average(history_x))
        smooth_y.append(moving_average(history_y))
        smooth_z.append(moving_average(history_z))

        ax1.clear()
        ax1.set_xlim(-1.2, 1.2)
        ax1.set_ylim(-1.2, 1.2)
        ax1.set_zlim(-1.2, 1.2)
        ax1.set_title("Raw Magnetic Field Data")
        ax1.set_xlabel("X (mT)")
        ax1.set_ylabel("Y (mT)")
        ax1.set_zlabel("Z (mT)")
        ax1.plot(history_x, history_y, history_z, c='b', label="Raw Path")
        ax1.scatter(history_x[-1], history_y[-1], history_z[-1], c='r', marker='o', label="Current Point")
        ax1.legend()

        
        ax2.clear()
        ax2.set_xlim(-1.2, 1.2)
        ax2.set_ylim(-1.2, 1.2)
        ax2.set_zlim(-1.2, 1.2)
        ax2.set_title("Moving Average")
        ax2.set_xlabel("X (mT)")
        ax2.set_ylabel("Y (mT)")
        ax2.set_zlabel("Z (mT)")
        ax2.plot(smooth_x, smooth_y, smooth_z, c='g', label="Smoothed Path")
        ax2.scatter(smooth_x[-1], smooth_y[-1], smooth_z[-1], c='r', marker='o', label="Current Point")
        ax2.legend()
    except Exception as e:
        print(f"Error reading serial data: {e}")


while True:
    update_plot()
    plt.pause(0.01)  
