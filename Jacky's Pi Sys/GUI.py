import tkinter as tk
import time

def Pressurize():
    print("Pressurization process has started.")
    countP = 0 
    limitP = 5
    
    while(countP < limitP):
        print(countP)
        time.sleep(1)
        countP = countP + 1
    
        if(countP == limitP):
            print("DONE")
            break
            
root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

#Create a button to start the pressurization.
button1 = tk.Button(frame, text="QUIT", fg="red", command=quit)
button1.pack(side=tk.LEFT)
slogan = tk.Button(frame,text="Pressurization", command=Pressurize)
slogan.pack(side=tk.LEFT)

try:
    root.mainloop()
except SystemExit:
    print("The user has exited pressurization process!")
