import RPi.GPIO as GPIO

RELAY_PIN = 17


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.LOW)


def send_relay_on():
    setup()
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    print("Relay ON")


def send_relay_off():
    setup()
    GPIO.output(RELAY_PIN, GPIO.LOW)
    print("Relay OFF")


def cleanup():
    setup()
    GPIO.output(RELAY_PIN, GPIO.LOW)
    GPIO.cleanup()
