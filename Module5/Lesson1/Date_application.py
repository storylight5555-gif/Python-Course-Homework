from tkinter import*
from datetime import date

window = Tk()
window.title("What is the date? Application")
window.geometry("400x300")
lbl = Label(text="Hey there!", font=("Arial Bold", 20), fg="white", bg="black", width=300, height=1)
name_lbl = Label(text="Enter your name:", font=("Arial Bold", 15), fg="white", bg="black")
name_entry = Entry(fg="white", bg="black")
window.configure(bg="black")

def display():
    name = name_entry.get()
    global message
    message = "Welcome to the Application!\nTodays date is:" 
    greet = "Hello " + name + "\n"
    text_box.delete("1.0", END)
    text_box.insert(END, greet)
    text_box.insert(END, message)
    text_box.insert(END, date.today())
text_box = Text(height=3, fg="white", bg="blue")
btn = Button(text="Click Me!", font=("Arial Bold", 15), fg="white", bg="black", command=display, height=1)
lbl.pack()
name_lbl.pack()
name_entry.pack()
text_box.pack()
btn.pack()

window.mainloop()