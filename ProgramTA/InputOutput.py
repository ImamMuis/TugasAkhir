import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

class Output:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def buka(self):
        GPIO.output(self.pin, 1)

    def kunci(self):
        GPIO.output(self.pin, 0)

class clean:
    GPIO.cleanup()