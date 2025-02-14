import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import serial
import time
from collections import deque
import numpy as np

# 시리얼 포트 설정
ser = serial.Serial('/dev/cu.usbserial-14110', 115200)  # Mac의 Serial 포트 사용
time.sleep(2)

# 데이터 저장
history_x = deque(maxlen=50)
history_y = deque(maxlen=50)
history_z = deque(maxlen=50)

smooth_x = deque(maxlen=20)
smooth_y = deque(maxlen=20)
smooth_z = deque(maxlen=20)

# 플롯 설정
fig = plt.figure(figsize=(12, 6))
ax1 = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122, projection='3d')

def moving_average(data, window_size=10):
    return np.mean(data) if len(data) >= window_size else np.mean(data[:len(data)])

while True:
    try:
        # Serial 데이터 읽기
        line = ser.readline().decode().strip()
        magX, magY, magZ = map(float, line.split(","))
        print(f"X: {magX}, Y: {magY}, Z: {magZ}")

        # 데이터 저장
        history_x.append(magX)
        history_y.append(magY)
        history_z.append(magZ)

        smooth_x.append(moving_average(history_x))
        smooth_y.append(moving_average(history_y))
        smooth_z.append(moving_average(history_z))

        # 원본 데이터 플롯
        ax1.clear()
        ax1.set_title("Original Data (Raw Magnetic Field)")
        ax1.set_xlabel("X (mT)")
        ax1.set_ylabel("Y (mT)")
        ax1.set_zlabel("Z (mT)")
        ax1.set_xlim(-80, 80)
        ax1.set_ylim(-80, 80)
        ax1.set_zlim(-80, 80)
        ax1.plot(history_x, history_y, history_z, color='blue', label="Raw Path")
        ax1.scatter(history_x[-1], history_y[-1], history_z[-1], color='red', label="Current Point")
        ax1.legend()

        # 이동 평균 데이터 플롯
        ax2.clear()
        ax2.set_title("Smoothed Data (Moving Average)")
        ax2.set_xlabel("X (mT)")
        ax2.set_ylabel("Y (mT)")
        ax2.set_zlabel("Z (mT)")
        ax2.set_xlim(-80, 80)
        ax2.set_ylim(-80, 80)
        ax2.set_zlim(-80, 80)
        ax2.plot(smooth_x, smooth_y, smooth_z, color='green', label="Smoothed Path")
        ax2.scatter(smooth_x[-1], smooth_y[-1], smooth_z[-1], color='red', label="Current Point")
        ax2.legend()

        plt.pause(0.01)
        # plt.show()

    except KeyboardInterrupt:
        print("Stopping plot...")
        break
    except Exception as e:
        print(f"Error: {e}")

ser.close()
