# Pi Systems
This folder contains all subsystems that will be running on the main airlock computer, such as lighting, pressurization, and sensor subsystems.
 
## Subsystems Explained.
A subsystem contains all the code related to a certain subroutine pertaining to airlock operation.

Each subsystem should be an extension of the abstract `Subsystem` class and should implement its associated methods. We do this, as making all subsystems an extension of a unified class:

&nbsp;&nbsp;&nbsp;*A)* Enables super easy setup and cleanup of systems at runtime.<br/>
&nbsp;&nbsp;&nbsp;*B)* Maintains convention across all subsystems, improving maintainability and scaleability.<br/>
&nbsp;&nbsp;&nbsp;*C)* Allows simple monitoring of systems throughout the life cycle.<br/><br/>

If you are unsure about Classes, Class Extensions or Abstract classes, refer to the official docs linked below. To fully understand the implementation, you should be familiar with the concepts of object-oriented programming, parent and child classes, constructors, inheritance, overriding and polymorphism. (Note that you can still use the code without knowing these things - this will just help if you need to add code to the subsystem base)

[Classes & Extension](https://docs.python.org/3/tutorial/classes.html)
[Abstract Classes](https://www.python-course.eu/python3_abstract_classes.php)


Subsystems are defined by the following traits:
 - Have a unique name and thread ID
 - Have a thread_task() function that will be run on a separate thread during runtime.
 - Have direct access to Pi GPIO.


## Creating a Subsystem

### Intial Setup
To create a new subsystem, we must first make a child of *Abstract Subsystem Base Class* (The parent of all Subsystem objects) and use that to build the foundation of the subsystem. First, we must make sure to import the subsystem base class:

<pre><code>
# Import the Subsystem class file for use.
import pi-systems_subsystem-base as subsys
</code></pre>

Then, you can define your child subsystem:

<pre><code> 
 # ...

# Create a child of the Subsystem class specifically tailored to your task. Don't forget to extend Subsystem!
class MyServiceThread(subsys.Subsystem):
     
     def __init__(self, gpio, name=None, threadID=None):
     
         # Put extra constructor code here
         
         super().__init__(gpio,name=name,threadID=threadID)
     
</code></pre>

(Note: You can choose to omit the `__init__` method (if you do, it is automatically called in the superclass), but in the example, it is overridden)

### Define the Task
Each subsystem can run a task on a separate thread. The code to be run is defined in the `thread_task` method. You must make sure to implement this method, or the system will not interpret properly. If the code should loop, use a `while` loop with `self.is_running` as its conditional (this enables automatic cleanup, as opposed to `while True`, which causes a lot of issues). The method is defined within the child subsystem itself:

<pre><code>
class MyServiceThread(subsys.Subsystem):
    #...
    
    def thread_task(self):
        while self.is_running:
            # Your code here
     
</code></pre>

### Creating and Running an Instance of your Subsystem
You'll need to create a new instance of this task to be run in the main loop. To do this, simply create a new instance of the Subsystem's class in your initialization method:

<code><pre>
threadID = 2 # or any other unique number
mySubsys = MySubsysThread("ThreadName", threadID)
</code></pre>

To start this Subsystem, simply `start()` it:
<code><pre>
mySubsys.start()
</code></pre>
