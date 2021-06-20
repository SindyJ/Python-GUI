import os
from tkinter import *

root = Tk()
root.title("Untitled - Notepad")
root.geometry("640x480")

# open, save file name
filename = "mynote.txt"

def open_file():
    if os.path.isfile(filename): # if file exist -> True. if not -> False
        with open(filename, "r", encoding="utf8") as file:
            txt.delete("1.0", END) # FROM first line 0 column to END
            txt.insert(END, file.read())

def save_file():
    with open(filename, "w", encoding="utf8") as file:
        file.write(txt.get("1.0", END)) # Save from 1(first) line 0 column to END

# Menu
menu = Menu(root)

menu_file = Menu(menu, tearoff=0)
menu_file.add_command(label="Open", command=open_file)
menu_file.add_command(label="Save", command=save_file)
menu_file.add_separator()
menu_file.add_command(label="Exit", command=root.quit)
menu.add_cascade(label="File", menu=menu_file)

# Create empty tabs on menu
menu.add_cascade(label="Edit")
menu.add_cascade(label="Format")
menu.add_cascade(label="View")
menu.add_cascade(label="Help")

# Scroll bar
scrollbar = Scrollbar(root)
scrollbar.pack(side="right", fill="y")

# Text area (Note)
txt = Text(root, yscrollcommand=scrollbar.set)
txt.pack(side="left", fill="both", expand=True)

scrollbar.config(command=txt.yview)

root.config(menu=menu)
root.mainloop()