from smbus2 import SMBus
from mlx90614 import MLX90614
import time

bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)

OFFSET = 1.4


# def get_stable_temp(samples=10):
#     readings = []
#     for _ in range(samples):
#         readings.append(sensor.get_obj_temp())
#         time.sleep(0.1)
#     return sum(readings) / len(readings)


# def send_temperature():
#     object_temp = get_stable_temp()
#     return object_temp + OFFSET


def get_stable_temp(samples=10):
    readings = [sensor.get_obj_temp() for _ in range(samples)]
    return sum(readings) / len(readings)


def send_temperature():
    return get_stable_temp() + OFFSET
