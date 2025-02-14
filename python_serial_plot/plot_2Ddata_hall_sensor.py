import matplotlib.pyplot as plt
import serial
import time
from collections import deque

# 시리얼 포트 설정
ser = serial.Serial('/dev/cu.usbserial-14110', 115200)
time.sleep(2)

# 데이터 저장
history_x = deque(maxlen=200)  # 더 많은 데이터를 저장
history_y = deque(maxlen=200)
history_z = deque(maxlen=200)

# 플롯 설정
plt.ion()
fig, (ax_x, ax_y, ax_z) = plt.subplots(3, 1, figsize=(10, 8))

ax_x.set_title("X Axis Magnetic Field")
ax_x.set_xlabel("Samples")
ax_x.set_ylabel("Magnetic Field (mT)")
ax_x.set_ylim(-80, 80)

ax_y.set_title("Y Axis Magnetic Field")
ax_y.set_xlabel("Samples")
ax_y.set_ylabel("Magnetic Field (mT)")
ax_y.set_ylim(-80, 80)

ax_z.set_title("Z Axis Magnetic Field")
ax_z.set_xlabel("Samples")
ax_z.set_ylabel("Magnetic Field (mT)")
ax_z.set_ylim(-80, 80)

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

        # 각 플롯 업데이트
        ax_x.plot(history_x, label="X Axis", color="red")
        ax_y.plot(history_y, label="Y Axis", color="green")
        ax_z.plot(history_z, label="Z Axis", color="blue")

        ax_x.set_xlim(0, len(history_x))
        ax_y.set_xlim(0, len(history_y))
        ax_z.set_xlim(0, len(history_z))

        plt.pause(0.005)  # 빠른 플롯 업데이트

    except KeyboardInterrupt:
        print("Stopping plot...")
        break
    except Exception as e:
        print(f"Error: {e}")

ser.close()
