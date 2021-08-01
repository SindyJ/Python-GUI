import os
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import * # __all__
from tkinter import filedialog
from PIL import Image

root = Tk()
root.title("I'm GUI")

# Function on add an image button
def add_file():
    files = filedialog.askopenfilenames(title="Select an image file.", \
        filetypes=(("PNG file", "*.png"), ("All files", "*.*")), \
        initialdir=r"C:\Users\726772\Desktop\PythonWorkspace\images")

    # The list of selected files
    for file in files:
        list_file.insert(END, file)

# Function on delete an image button
def del_file():
    for index in reversed(list_file.curselection()):
        list_file.delete(index)
    
# Function on browse button : Browse a file explorer
def browse_dest_path():
    folder_selected = filedialog.askdirectory(initialdir=r"C:\Users\726772\Desktop\PythonWorkspace")
    
    if folder_selected == '': # When a user clicks the cancel button
        return
    # Delete an old value displayed    
    txt_dest_path.delete(0, END)
    # Add a new value
    txt_dest_path.insert(0, folder_selected)

# combind images
def merge_images():

    try:
        # width
        img_width = cmb_width.get()
        if img_width == "Original":
            img_width = -1 # when it's -1, original
        else:
            img_width = int(img_width)

        # Gap
        img_space = cmb_space.get()
        if img_space == "Narrow":
            img_space = 30
        elif img_space == "Regular":
            img_space = 60
        elif img_space == "Wide":    
            img_space = 90
        else: # None
            img_space = 0

        # Format
        img_format = cmb_format.get().lower() # Transfer a format value(PNG, JPG, BMP) to lower case

        images = [Image.open(x) for x in list_file.get(0, END)] # size -> size[0]: width, size[1]: height

        # image size to list
        image_sizes = [] # [(width1, height1), (width2, height2), ...]
        if img_width > -1:
            # change the width value
            image_sizes = [(int(img_width), int(img_width * x.size[1] / x.size[0])) for x in images]
        else:
            # Use the original size
            image_sizes = [(x.size[0], x.size[1]) for x in images]

        # calculation 100*60 img -> width 80, what is height?
        # original width : original height = changed width : changed height
        # x : y = x' : y' --> x*y' = x'*y

        # In our code
        # x = width = size[0]
        # y = height = size[1]
        # x' = img_width # has to change to this value
        # y' = x'y / x = img_width * size[1] / size[0]
    
        widths, heights = zip(*(image_sizes))

        # calculate max width, total height
        max_width, total_height = max(widths), sum(heights)

        # prepare the paper
        if img_space > 0 :
            total_height += (img_space * (len(images)-1))
        result_img = Image.new("RGB", (max_width, total_height), (255, 255, 255)) # Set a background white color
        y_offset = 0 # y location
        # for img in images:
        #     result_img.paste(img, (0, y_offset))
        #     y_offset += img.size[1] # add the image height so the next img can be pasted after the image

        for idx, img in enumerate(images):
            # if width is not original, we have to re-change the size
            if img_width > -1:
                img = img.resize(image_sizes[idx])

            result_img.paste(img, (0, y_offset))
            y_offset += (img.size[1] + img_space) # height + selected space

            progress = (idx + 1) / len(images) * 100 # calculate the percent
            p_var.set(progress)
            progress_bar.update()

        # Adjusting a format option
        file_name = "NewPhoto." + img_format
        dest_path = os.path.join(txt_dest_path.get(), file_name)
        result_img.save(dest_path)
        msgbox.showinfo("Alert", "Completed! The new image is created.")
    except Exception as err: # Exception
        msgbox.showerror("Error", err)

# Function on START button
def start():
    # Confirm all of the selected value for options.
    print("Width: ", cmb_width.get())
    print("Gap: ", cmb_space.get())
    print("Format: ", cmb_format.get())

    # Check the list of files
    if list_file.size() == 0:
        msgbox.showwarning("Warning", "Please, add image files.")
        return

    # Check the path to save
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning("Warning", "Please, set the path to save a combined image.")
        return

    # combine images
    merge_images()

# File frame
file_frame = Frame(root)
file_frame.pack(fill="x", padx=5, pady=5)

# Add an image button
btn_add_file = Button(file_frame, padx=5, pady=5, width=12, text="Add an image", command=add_file)
btn_add_file.pack(side="left")

# Delete an image button
btn_del_file = Button(file_frame, padx=5, pady=5, width=12, text="Delete an image", command=del_file)
btn_del_file.pack(side="right")

# List frame
list_frame = Frame(root)
list_frame.pack(fill="both", padx=5, pady=5)

# Scroll bar
scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

# Listbox to show selected images
list_file = Listbox(list_frame, selectmode="extended", height=15, yscrollcommand=scrollbar.set)
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview)

# Folder path frame
path_frame = LabelFrame(root, text="Folder path")
path_frame.pack(fill="x", padx=5, pady=5, ipady=5) # inner padding

# Entry widget to show a selected folder path
txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4)

# Browse button
btn_dest_path = Button(path_frame, text="Browse", width=10, command=browse_dest_path)
btn_dest_path.pack(side="right", padx=5, pady=5)

# Option frame
frame_option = LabelFrame(root, text="Options")
frame_option.pack(padx=5, pady=5, ipady=5)

# Width
## Width label
lbl_width = Label(frame_option, text="Width", width=8)
lbl_width.pack(side="left", padx=5, pady=5)
## Width Combobox - drop-down ["Original", "1024", "800", "640"]
opt_width = ["Original", "1024", "800", "640"]
cmb_width = ttk.Combobox(frame_option, state="readonly", values=opt_width, width=10)
cmb_width.current(0)
cmb_width.pack(side="left", padx=5, pady=5)

# Gap
## Gap label
lbl_space = Label(frame_option, text="Gap", width=8)
lbl_space.pack(side="left", padx=5, pady=5)
## Gap Combobox - drop-down ["None", "Narrow", "Regular", "Wide"]
opt_space = ["None", "Narrow", "Regular", "Wide"]
cmb_space = ttk.Combobox(frame_option, state="readonly", values=opt_space, width=10)
cmb_space.current(0)
cmb_space.pack(side="left", padx=5, pady=5)

# Image Format
## Image Format label
lbl_format = Label(frame_option, text="Format", width=8)
lbl_format.pack(side="left", padx=5, pady=5)
## Image Format Combobox - drop-down ["PNG", "JPG", "BMP"]
opt_format = ["PNG", "JPG", "BMP"]
cmb_format = ttk.Combobox(frame_option, state="readonly", values=opt_format, width=10)
cmb_format.current(0)
cmb_format.pack(side="left", padx=5, pady=5)

# Progress bar frame
frame_progress = LabelFrame(root, text="Progress")
frame_progress.pack(fill="x", padx=5, pady=5, ipady=5)

# Progress bar
p_var = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
progress_bar.pack(fill="x", padx=5, pady=5)

# Executing frame
frame_run = Frame(root)
frame_run.pack(fill="x", padx=5, pady=5)

# CLOSE button
btn_close = Button(frame_run, padx=5, pady=5, text="CLOSE", width=12, command=root.quit)
btn_close.pack(side="right", padx=5, pady=5)

# START button
btn_start = Button(frame_run, padx=5, pady=5, text="START", width=12, command=start)
btn_start.pack(side="right", padx=5, pady=5)

root.resizable(False, False) # false -> non-changable
root.mainloop()