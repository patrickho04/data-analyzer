from Data import Data
from tkinter import *
from tkinter import filedialog

def show_frame(frame):
    frame.tkraise()

def openFile() -> bool:
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
        dataset = Data(filepath)

root = Tk()
root.geometry("900x600") 
root.title("Statistics Analyzer")
root.resizable(False, False)

# Create the navbar
navbar = Frame(root, bg="lightgray")
navbar.pack(side=TOP, fill="x")

select_file_option = Button(navbar, text="Select File", command=lambda: show_frame(select_file_page))
select_file_option.pack(side="left", padx=10, pady=10)

basic_desc_option = Button(navbar, text="Basic Desc.", command=lambda: show_frame(basic_desc_page))
basic_desc_option.pack(side="left", padx=10, pady=10)

# Create the container to hold all the pages
container = Frame(root)
container.pack(fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# Frame setup
select_file_page = Frame(container)
basic_desc_page = Frame(container)

frames = [select_file_page, basic_desc_page]

# Stack the frames on top of each other
for frame in frames:
    frame.grid(row=0, column=0, sticky="nsew")

# Page 1 (Select File)
select_file_button = Button(select_file_page, text="Select File", command=openFile)
select_file_button.pack(expand=True)

# Page 2 (Basic Descriptions)
desc_label = Label(basic_desc_page, text="Basic Description Page")
desc_label.pack()

show_frame(select_file_page)
root.mainloop()  
