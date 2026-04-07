from smbus2 import SMBus
from mlx90614 import MLX90614
import time

bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)

OFFSET = 1.40


def get_stable_temp(sensor, samples=10):
    readings = []
    for _ in range(samples):
        readings.append(sensor.get_obj_temp())
        time.sleep(0.1)
    return sum(readings) / len(readings)


try:
    while True:
        ambient = sensor.get_amb_temp()
        object_temp = get_stable_temp(sensor)
        corrected = object_temp + OFFSET
        print(f"Temperature : {corrected:.2f} °C")
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped")
