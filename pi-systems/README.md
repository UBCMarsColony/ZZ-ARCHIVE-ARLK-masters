# Pi Systems
This folder contains all subsystems that will be running on the main airlock computer, such as lighting, pressurization, and sensor subsystems.
 
## Creating a Subsystems
Each subsystem should be an extension of the abstract `Subsystem` class and should implement its associated methods. We do this, as making all subsystems an extension of a unified class:


A) Enables super easy setup and cleanup of systems at runtime.

B) Maintains convention across all subsystems, improving maintainability and scaleability.

C) Allows simple monitoring of systems throughout the life cycle

If you are unsure about Classes, Class Extensions or Abstract classes, refer to the official docs:

[Classes & Extension](https://docs.python.org/3/tutorial/classes.html)

[Abstract Classes](https://www.python-course.eu/python3_abstract_classes.php)

Subsystems are defined by the following traits:
 - Have a unique name and thread ID
 - Have a thread_task() function that will be run on a separate thread during runtime.
 - Have direct access to Pi GPIO.

To create a new subsystem, we must first import the *Subsystem Abstract Class* and use that to build the foundation of the subsystem, as shown below:

<pre><code>
# Import the Subsystem class file for use.
import pi-systems_subsystem-base as subsys
 
 # ...

# Create a new instance of the Subsystem class specifically tailored to your task. Don't forget to extend Subsystem!
class MyServiceThread(subsys.Subsystem):
     
     # Define the thread_task() method. The code put here will be run on a new thread by the subsystem.
     def thread_task():
          print(self.subsys_thread.name + " is running as expected!")
</code></pre>

By default, the only required argument for a subsystem is a GPIO reference. You can override the `__init__()` constructor method in a subsystem if you need more arguments - Just be sure to call `self.super()` once it finishes.

You'll need to create a new instance of this task to be run in the main loop. To do this, simply create a new instance of the Subsystem's class in your initialization method:

<code><pre>
threadID = 2 # or any other unique number
mySubsys = MySubsysThread("ThreadName", threadID)
</code></pre>

To start this Subsystem, simply `start()` it:
<code><pre>
mySubsys.start()
</code></pre>
