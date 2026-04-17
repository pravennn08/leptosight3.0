import RPi.GPIO as GPIO
import time

RELAY_PIN = 17


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.LOW)


def loop():
    try:
        while True:
            print("Relay ON")
            GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn ON
            # time.sleep(1)

            # print("Relay OFF")
            # GPIO.output(RELAY_PIN, GPIO.LOW)  # Turn OFF
            # time.sleep(1)

    except KeyboardInterrupt:
        print("\nExiting program...")

    finally:
        cleanup()


def cleanup():
    GPIO.output(RELAY_PIN, GPIO.LOW)  # Ensure relay is OFF
    GPIO.cleanup()


if __name__ == "__main__":
    setup()
    loop()


# import RPi.GPIO as GPIO
# from time import sleep

# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(17, GPIO.OUT)

# GPIO.output(17, 1)
# # sleep(1)
# while True:
#     GPIO.output(17, 0)
#     sleep(1)
#     pass
