from classes.Data import Data
from tkinter import *
from tkinter import filedialog

def show_frame(frame) -> None:
    frame.tkraise()

def validate_input(new_value) -> bool:                                                                                              # Validation function to allow only numbers
    if new_value == "" or new_value.isdigit():
        return True
    else:
        return False

def openFile() -> None:
    global ds
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
        ds = Data(filepath)

def setColValue() -> None:
    global colVal
    colVal = int(column_input.get())

def setQtVal() -> None:
    global qtVal
    if int(qnt_input.get()) <= 0 or int(qnt_input.get()) >= 100:
        raise ValueError("Quantile value must be between 0 and 100.")
    qtVal = int(qnt_input.get())/100

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

validate_command = basic_desc_page.register(validate_input)                                                                         # Validate input (make sure it is a digit)

column_label = Label(basic_desc_page, text="Enter Column:")
column_label.pack()
column_input = Entry(basic_desc_page, validate="key", validatecommand=(validate_command, '%P'),width=13, justify="center")
column_input.pack()

qnt_label = Label(basic_desc_page, text="Enter Quantile (in %):")
qnt_label.pack()
qnt_input = Entry(basic_desc_page, validate="key", validatecommand=(validate_command, '%P'),width=13, justify="center")
qnt_input.pack()

submit_column_btn = Button(basic_desc_page, text="Submit", command=lambda: set_basic_desc_vals())                                   # Input stored as 'colVal'
submit_column_btn.pack(pady=10)

def set_basic_desc_vals() -> None:                                                                                                  # Get all basic statistical description values  
    global basic_vals
    global colVal
    global qtVal

    basic_vals = {'min': 0, 'max': 0, 'mean': 0, 'mode': 0, 'median': 0, 'range': 0, 'std': 0, 'var': 0, 'quantile': 0, 'iqr': 0}

    setColValue()
    setQtVal()

    if colVal < 0 or colVal >= len(ds.dataset.columns):
        raise IndexError("Column does not exist.")
    
    basic_vals['min'] = ds.min(column=colVal)
    basic_vals['max'] = ds.max(column=colVal)
    basic_vals['mean'] = ds.mean(column=colVal)
    basic_vals['mode'] = ds.mode(column=colVal)
    basic_vals['median'] = ds.median(column=colVal)
    basic_vals['range'] = ds.range(column=colVal)
    basic_vals['std'] = ds.std(column=colVal)
    basic_vals['var'] = ds.var(column=colVal)
    basic_vals['quantile'] = ds.quantile(column=colVal, qt=qtVal)
    basic_vals['iqr'] = ds.iqr(column=colVal)

    print(basic_vals)

# Page 3 (Graphs)
graph_title = Label(graph_page, text="Graphs", font=title_font)
graph_title.pack(pady=15)

show_frame(select_file_page)
root.mainloop()  
