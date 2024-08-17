from classes.Data import Data
from tkinter import *
from tkinter import filedialog

def show_frame(frame):
    frame.tkraise()

def validate_input(new_value):                          # Validation function to allow only numbers
    if new_value == "" or new_value.isdigit():
        return True
    else:
        return False

def openFile() -> bool:
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
        dataset = Data(filepath)

def getColumnValue(e: Entry):
    global columnVal
    columnVal = e.get()

# Tkinter Setup
title_font = ('Bold', 13)

root = Tk()
root.geometry("900x600") 
root.title("Statistics Analyzer")
root.resizable(False, False)

# Create the navbar
navbar = Frame(root, bg="lightgray")
navbar.pack(side=TOP, fill="x")

select_file_option = Button(navbar, text="Select File", command=lambda: show_frame(select_file_page))
basic_desc_option = Button(navbar, text="Basic Desc.", command=lambda: show_frame(basic_desc_page))
graph_option = Button(navbar, text="Graphs", command=lambda: show_frame(graph_page))

options = [select_file_option, basic_desc_option, graph_option]

for option in options:
    option.pack(side="left", padx=10, pady=10)

# Create the container to hold all the pages
container = Frame(root)
container.pack(fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# Frame setup
select_file_page = Frame(container)
basic_desc_page = Frame(container)
graph_page = Frame(container)

frames = [select_file_page, basic_desc_page, graph_page]

for frame in frames:                                                                                                                # Stack the frames on top of each other
    frame.grid(row=0, column=0, sticky="nsew")

# Page 1 (Select File)
select_title = Label(select_file_page, text="Select CSV Title", font=title_font)
select_title.pack(pady=15)
select_file_button = Button(select_file_page, text="Select File", command=openFile)
select_file_button.pack(expand=True)

# Page 2 (Basic Descriptions)
desc_title = Label(basic_desc_page, text="Basic Description Page", font=title_font)
desc_title.pack(pady=15)

column_label = Label(basic_desc_page, text="Enter Column:")
column_label.pack()

validate_command = basic_desc_page.register(validate_input)                                                                         # Validate input (make sure it is a digit)
column_input = Entry(basic_desc_page, validate="key", validatecommand=(validate_command, '%P'),width=13, justify="center")
column_input.pack()

submit_column_btn = Button(basic_desc_page, text="Submit", command=lambda: getColumnValue(column_input))                            # Input stored as 'columnVal'
submit_column_btn.pack(pady=10)

# Page 3 (Graphs)
graph_title = Label(graph_page, text="Graphs", font=title_font)
graph_title.pack(pady=15)

show_frame(select_file_page)
root.mainloop()  
