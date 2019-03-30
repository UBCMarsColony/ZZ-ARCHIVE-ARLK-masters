import importlib
subsys = importlib.import_module("pi-systems_subsystem-base")

# Try importing, gives error message if it fails
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print(
        "Error importing RPi.GPIO!  This is probably because you need \
         superuser privileges.  You can achieve this by using 'sudo' to \
         run your script")
except ModuleNotFoundError:
    print("Running on non-pi machine")


class LightingSubsystem(subsys.Subsystem):
    def __init__(self, name=None, thread_id=None, pins=None):
        super().__init__(name=name, thread_id=thread_id, loop_delay_ms=750)

        self.pins = pins if isinstance(pins, list) else [pins]

        self.light_state = GPIO.LOW
        GPIO.setmode(GPIO.BCM)
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

    # Check input signal, if high, turn lights on, if low, turn lights off
    def loop(self):
        with self.lock:
            for pin in self.pins:
                GPIO.output(pin, self.light_state)

    def toggle(self, state=None):  # State should be a bool or int 0/1
        if state is not None:
            self.light_state = state
        else:
            self.light_state = not self.light_state
