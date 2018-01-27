# Pi Systems
This folder contains all systems that will be running on the main airlock computer

## Current Systems
Currently, systems in place include:
 - Door
 - Pressurization
 
## Creating a Service
Each service should contain a class of type `Service` and should implement its associated methods. Within a generic service file, this setup is performed as shown below:

<pre><code>
import pi-systems_service-base as service_base
 
 # ...

class MyServiceThread(service_base.Service):
     
     # This method must be defined for the service to perform properly
     def thread_task():
          print(self.serivce_thread.name + " is running as expected!")
          
          # Your code here

</code></pre>

To create an instance of this Service and its associated thread task, simply create a new variable of the Service's class:

<code><pre>
threadID = 2 # or any other unique number
myThread = MyServiceThread("ThreadName", threadID)
</code></pre>

To start this Service, simply type:

<code><pre>
myThread.start()
</code></pre>
