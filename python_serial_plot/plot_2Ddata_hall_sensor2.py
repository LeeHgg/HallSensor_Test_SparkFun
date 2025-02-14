import matplotlib.pyplot as plt
import serial
import time
from collections import deque

# 시리얼 포트 설정
ser = serial.Serial('/dev/cu.usbserial-14110', 115200)  # Mac의 Serial 포트 사용
time.sleep(2)

# 데이터 저장
history_x = deque(maxlen=100)
history_y = deque(maxlen=100)
history_z = deque(maxlen=100)

# 플롯 설정
plt.ion()
fig, (ax_x, ax_y, ax_z) = plt.subplots(3, 1, figsize=(10, 8))

# 각 축 설정
ax_x.set_title("X Axis Magnetic Field")
ax_x.set_xlabel("Samples")
ax_x.set_ylabel("Magnetic Field (mT)")
ax_x.set_ylim(-1.5, 1.5)

ax_y.set_title("Y Axis Magnetic Field")
ax_y.set_xlabel("Samples")
ax_y.set_ylabel("Magnetic Field (mT)")
ax_y.set_ylim(-1.5, 1.5)

ax_z.set_title("Z Axis Magnetic Field")
ax_z.set_xlabel("Samples")
ax_z.set_ylabel("Magnetic Field (mT)")
ax_z.set_ylim(-1.5, 1.5)

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
        ax_x.clear()
        ax_x.plot(history_x, label="X Axis", color="red")
        ax_x.set_ylim(-1.5, 1.5)
        ax_x.legend()

        ax_y.clear()
        ax_y.plot(history_y, label="Y Axis", color="green")
        ax_y.set_ylim(-1.5, 1.5)
        ax_y.legend()

        ax_z.clear()
        ax_z.plot(history_z, label="Z Axis", color="blue")
        ax_z.set_ylim(-1.5, 1.5)
        ax_z.legend()

        plt.pause(0.01)

    except KeyboardInterrupt:
        print("Stopping plot...")
        break
    except Exception as e:
        print(f"Error: {e}")

ser.close()
