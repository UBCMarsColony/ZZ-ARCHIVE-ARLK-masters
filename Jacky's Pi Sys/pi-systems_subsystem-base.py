import threading

from abc import ABC, abstractmethod
import importlib
import random
import time
from enum import Enum
subsys_pool = importlib.import_module("pi-systems_subsystem-pool")

"""
Author: ThomasJFR (Thomas Richmond)
Purpose: Define, contain and execute a subprocess of the airlock.
More information on this is included in the README file of the directory.
"""


class Subsystem(ABC):

    """
    name: Verbose name of subsystem. Can be used to
        get a subsystem from the pool
    thread_id: ID to associate to a thread once it
        enters the thread pool. Immediately
        tunneled to SubsystemThread object.
    loop_delay_ms: The amount of time to wait between
        loops while operational. Immedaitely
        tunneled to SubsystemThread object.
    on_start: Callback invoked once the subsystem
        thread begins.
    on_stop: Callback invoked once the subsystem
        thread stops.
    on_loop: Callback invoked every time the thread loop runs.
    """
    def __init__(
        self,
        name,
        *,
        thread_id,
        loop_delay_ms,
        on_start=None,
        on_stop=None,
        on_loop=None,
    ):
        self.name = name
        self.thread = Subsystem.SubsystemThread(
            thread_id=thread_id,
            loop_delay_ms=loop_delay_ms,
            loop=self._loop)

        def empty(): pass
        self.on_start = on_start if callable(on_start) else empty
        self.on_stop = on_stop if callable(on_stop) else empty
        self.on_loop = on_loop if callable(on_loop) else empty

        subsys_pool.add(self)

    """
    Starts the thread loop and invokes the on_start method if it exists.
    """
    def start(self):
        if self.thread.running:
            return

        self.thread.start()

        if (self.on_start):  # Run callback method if it exists
            self.on_start()

    def stop(self):
        self.thread.stop()

        if (self.on_stop):  # Run callback method if it exists
            self.on_stop()

    """
    Definition contains the code which will be looped
    during the thread's active life.
    """
    @abstractmethod
    def loop(self):
        pass

    """
    Wrapper function to call both the loop and the loop callback
    for each loop cycle.
    """
    def _loop(self):
        self.loop()
        if self.on_loop:
            self.on_loop()

    """
    __enter__, __exit__ and __lock__ are constructs which allow the
    "with" statement to be used on a subsystem. While acquired, a
    subsystems data can be accessed and modified.
    """
    def __enter__(self):
        self.lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()

    @property
    def lock(self):
        return self.thread.lock

    """
    Allow the subsystem's state to be represented in human-readable format.
    """
    def __repr__(self):
        return "{ \n\tname: \"%s\", \n\tthread_id: %i, \n\trunning: %s \n}" \
            % (self.name, self.thread.thread_id, str(self.thread.running))

    """
    Purpose: SubsystemThread is a composition-based helper class that
        implements additional threading functionality. It includes a
        predefined "run" method which loops over a target method, rather
        than calling it just once. It also holds a lock object unique to
        the subsystem.
    """
    class SubsystemThread():
        DEFAULT_LOOP_DELAY_MS = 750

        """
        thread_id: ID to associate to a thread once it
         enters the thread pool. Can be a string or number.
        loop: The target method to call while looping.
        loop_delay_ms:  The amount of time to wait between
            loops while operational.
        """
        def __init__(
            self,
            thread_id,
            loop,
            loop_delay_ms=DEFAULT_LOOP_DELAY_MS
        ):
            # Thread Data
            self.thread_id = thread_id
            self.running = False

            # Create Objects
            self.lock = threading.Lock()
            self._thread = threading.Thread(
                name=thread_id,
                target=self._run,
                args=(loop, loop_delay_ms))

        def start(self):
            self.running = True
            self._thread.start()

        def stop(self):
            self.running = False

        def _run(self, loop, loop_delay_ms):
            # Wrapper function to make loop logic statement look nicer
            def millis():
                return time.time() * 1000

            last_runtime = millis()
            while self.running:
                # convert loop_delay_ms to seconds.
                if millis() - last_runtime >= loop_delay_ms:
                    try:
                        loop()
                    except Exception as e:
                        print(
                            'Error: Subsystem exception has occured for subsystem thread %s: %s' %
                            (self.thread_id, e))
                    last_runtime = millis()

                time.sleep(0.05)
