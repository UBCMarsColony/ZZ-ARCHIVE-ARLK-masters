# Pi Systems
This folder contains all subsystems that will be running on the main airlock computer, such as lighting, pressurization, and sensor subsystems.
 
___
## Subsystems
<details><summary><b>Simplified</b></summary>
A subsystem manages and runs a single subroutine within the airlock (lighting, valves, sensor polling, etc...).  
<br/><br/>
To get started, here's a template for creating a new subsystem:

    import relative_path_to_subsystem_base as subsys
    # or
    import importlib
    subsys = importlib.import_module('relative_path_to_subsystem_base')
 
    # Your service class.
    class ExampleSubsystem(subsys.Subsystem):
   
        def __init__(self, name=None, threadID=None):
            super().__init__(name=name,thread_id=thread_id)
            
            # Run initialization here
            
            
        def run(self):
            # Subsystem's main loop code.

            # If you want to perform an action that modifies 
            # something accessed from outside the thread, 
            # wrap it as follows:
            with self.thread.lock:
                # Modify variable
                pass

The subsystem can be created and run as follows:
    
    # Creating the subsystem
    mySubsys = ExampleSubsystem(name="ExampleSubsystemName", thread_id=1)
    
    # Starting and stopping the subsystem
    mySubsys.start()
    mySubsys.stop()
    
If you want to access some data that is modified from within the thread, you should perform this with the `run_method_async(myMethod)` function. If you do not, the program may crash due to a sync error.
    
    def get_some_data():
        # Get the data

    mySubsys.run_method_async(get_some_data)


</details>


<details><summary><b>Technical</b></summary>
A subsystem contains all the code related to a certain subroutine in the airlock's life cycle. This could be lighting, valve control, and basically anything the airlock will do repeatedly.

Each subsystem should be an extension of the abstract `Subsystem` class and should implement its associated methods. We do this, as making all subsystems an extension of a unified class:
* Enables super easy setup and cleanup of systems at runtime.
* Maintains convention across all subsystems, improving maintainability and scaleability.
* Allows simple monitoring of systems throughout the life cycle.

If you are unsure about Classes, Class Extensions or Abstract classes, refer to the official docs linked below. To fully understand the implementation, you should be familiar with the concepts of object-oriented programming, parent and child classes, constructors, abstract classes, abstract methods, inheritance, overriding and polymorphism. (Note that you can still use the code without knowing these things - this will just help if you need to add code to the subsystem base)

[Classes & Extension](https://docs.python.org/3/tutorial/classes.html)

[Abstract Classes](https://www.python-course.eu/python3_abstract_classes.php)


Subsystems are defined by the following traits:
 - Have a unique name and thread ID
 - Have a thread_task() function that will be run on a separate thread during runtime.

## Creating a Subsystem
This will outline how a subsystem is created, and the purpose of each component. For a template, go to the bottom of the page.

### Intial Setup
To create a new subsystem, we must first make a child of the base Subsystem class (The basis of all Subsystem objects) and use that to build the foundation of our subsystem. 

First, we must make sure to import the subsystem base class:

    import pi-systems_subsystem-base as subsys

Then, you can define your child subsystem:

    class MySubsys(subsys.Subsystem):
     
    def __init__(self,  name=None, threadID=None):
     
         # Put extra constructor code here
         
         super().__init__(name=name,threadID=threadID)


Note: You don't have to include the `__init__` constructor call in your subsystem code. If you choose to do this, the superclass constructor is implicitly called instead.

### Define the Main Task
Each subsystem can run a task on a separate thread. The code to be run is defined in the `run` method - an abstract method in the subsystem base class. **You must make sure to implement this method, or the subsystem will not compile.** If the code should loop, use a `while` loop with `self.running` as its conditional (this enables automatic cleanup, as opposed to `while True`, which causes issues). The method is defined within the child subsystem itself:

    class MyServiceThread(subsys.Subsystem):
    #...
    
    def run(self):
        while self.running:
            # Your code here

            # If you want to perform an action that modifies 
            # something accessed from outside the thread, 
            # wrap it as follows:
            with self.thread.lock:
                # Modify variable
                pass
     

### Creating and Running an Instance of your Subsystem
You'll need to create a new instance of this task to be run in the main loop. To do this, simply create a new instance of the Subsystem's class in your initialization method:

    thread_id = 2 # or any other unique number
    mySubsys = MySubsys("MySubsysName", thread_id)

To start this Subsystem, simply `start()` it:
    mySubsys.start()

To stop this subsystem, simply `stop()` it:
    mySubsys.stop()

</details>