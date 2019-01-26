import tkinter as tk
    
def Pressurize():
    print("Pressurization process has started.")
    # SET FLAGS/ BEGIN THE PRESSURIZATION BASED ON USER INPUT

def Depressuriza():
    print("Depressurization process has started. ")
    #continue here for dep

def CheckButtons(b1):
    if(b1)

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
