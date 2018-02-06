# Pi Systems
This folder contains all subsystems that will be running on the main airlock computer

## Current Subystems
Currently, subsystems in place include:
 - Door
 - Pressurization
 
## Creating a Subsystems
Each service should contain a class of type `Subsystem` and should implement its associated methods. Within a generic service file, this setup is performed as shown below:

<pre><code>
import pi-systems_subsystem-base as subsys
 
 # ...

class MyServiceThread(subsys.Subsystem):
     
     # This method must be defined for the service to perform properly
     def thread_task():
          print(self.subsys_thread.name + " is running as expected!")
          
          # Your code here

</code></pre>

To create an instance of this Service and its associated thread task, simply create a new variable of the Service's class:
<code><pre>
threadID = 2 # or any other unique number
mySubsys = MySubsysThread("ThreadName", threadID)
</code></pre>

To start this Subsystem, simply call:
<code><pre>
mySubsys.start()
</code></pre>
