# Pi Systems
This folder contains all subsystems that will be running on the main airlock computer, such as lighting, pressurization, and sensor subsystems.
 
## Subsystems Explained.
A subsystem contains all the code related to a certain subroutine in the airlock's life cycle. This could be lighting, valve control, and basically anything the airlock will do repeatedly.

Each subsystem should be an extension of the abstract `Subsystem` class and should implement its associated methods. We do this, as making all subsystems an extension of a unified class:

&nbsp;&nbsp;&nbsp;*A)* Enables super easy setup and cleanup of systems at runtime.<br/>
&nbsp;&nbsp;&nbsp;*B)* Maintains convention across all subsystems, improving maintainability and scaleability.<br/>
&nbsp;&nbsp;&nbsp;*C)* Allows simple monitoring of systems throughout the life cycle.<br/>

If you are unsure about Classes, Class Extensions or Abstract classes, refer to the official docs linked below. To fully understand the implementation, you should be familiar with the concepts of object-oriented programming, parent and child classes, constructors, abstract classes, abstract methods, inheritance, overriding and polymorphism. (Note that you can still use the code without knowing these things - this will just help if you need to add code to the subsystem base)

[Classes & Extension](https://docs.python.org/3/tutorial/classes.html)

[Abstract Classes](https://www.python-course.eu/python3_abstract_classes.php)


Subsystems are defined by the following traits:
 - Have a unique name and thread ID
 - Have a thread_task() function that will be run on a separate thread during runtime.
 - Have direct access to Pi GPIO.

## Creating a Subsystem
This will outline how a subsystem is created, and the purpose of each component. For a template, go to the bottom of the page.

### Intial Setup
To create a new subsystem, we must first make a child of the base Subsystem class (The basis of all Subsystem objects) and use that to build the foundation of our subsystem. 

First, we must make sure to import the subsystem base class:

<pre><code>import pi-systems_subsystem-base as subsys
</code></pre>

Then, you can define your child subsystem:

<pre><code>class MyServiceThread(subsys.Subsystem):
     
     def __init__(self, gpio, name=None, threadID=None):
     
         # Put extra constructor code here
         
         super().__init__(gpio,name=name,threadID=threadID)
     
</code></pre>

Note: You don't have to include the `__init__` constructor call in your subsystem code. If you choose to do this, the superclass constructor is implicitly called instead.

### Define the Task
Each subsystem can run a task on a separate thread. The code to be run is defined in the `thread_task` method - an abstract method in the subsystem base class. **You must make sure to implement this method, or the subsystem will not compile.** If the code should loop, use a `while` loop with `self.is_running` as its conditional (this enables automatic cleanup, as opposed to `while True`, which causes a lot of issues). The method is defined within the child subsystem itself:

<pre><code>
class MyServiceThread(subsys.Subsystem):
    #...
    
    def thread_task(self):
        while self.is_running:
            # Your code here
     
</code></pre>

### Creating and Running an Instance of your Subsystem
You'll need to create a new instance of this task to be run in the main loop. To do this, simply create a new instance of the Subsystem's class in your initialization method:

<pre><code>
threadID = 2 # or any other unique number
mySubsys = MySubsysThread("ThreadName", threadID)
</code></pre>

To start this Subsystem, simply `start()` it:
<pre><code>
mySubsys.start()
</code></pre>


### Template
To get started, here's a template for creating a new subsystem.
<details>
<summary><b>Template</b></summary>
  <pre><code>
  
  #Put directory path here!
  import path_to_subsystem_base as subsys
 
  class MyServiceThread(subsys.Subsystem):
   
    def __init__(self, gpio, name=None, threadID=None):
         # My initialization code     
         super().__init__(gpio,name=name,threadID=threadID)
         
         
    def thread_task(self):
        while self.is_running:
            # Write task code here
            pass
  
  </code></pre>
</details>
