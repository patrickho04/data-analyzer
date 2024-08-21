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

def setQtVal() -> None:
    global qtVal
    if int(qnt_input.get()) <= 0 or int(qnt_input.get()) >= 100:
        raise ValueError("Quantile value must be between 0 and 100.")
    qtVal = int(qnt_input.get())/100

def showError(page, errMessage: str) -> None:
    errLabel = Label(page, text=errMessage, fg="red")
    errLabel.pack()

# Tkinter Setup
title_font = ('Bold', 13)
basic_desc_font = ('Times', 12)

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
desc_title.pack(pady=10)

validate_command = basic_desc_page.register(validate_input)                                                                         # Validate input (make sure it is a digit)

colVal_label = Label(basic_desc_page, text="Enter Column:")
colVal_label.pack()
colVal_input = Entry(basic_desc_page, validate="key", validatecommand=(validate_command, '%P'),width=13, justify="center")
colVal_input.pack()

qnt_label = Label(basic_desc_page, text="Enter Quantile (in %):")
qnt_label.pack()
qnt_input = Entry(basic_desc_page, validate="key", validatecommand=(validate_command, '%P'),width=13, justify="center")
qnt_input.pack()

submit_colVal_btn = Button(basic_desc_page, text="Submit", command=lambda: set_basic_desc_vals())                                   # Input stored as 'colVal'
submit_colVal_btn.pack(pady=10)

centralFrame = Frame(basic_desc_page)                                                                                               # Set up Label widgets for cetral measure
max_desc = Label(centralFrame, text="MAX:\n0", font=basic_desc_font)
min_desc = Label(centralFrame, text="MIN:\n0", font=basic_desc_font)
mean_desc = Label(centralFrame, text="MEAN:\n0", font=basic_desc_font)
median_desc = Label(centralFrame, text="MEDIAN:\n0", font=basic_desc_font)
mode_desc = Label(centralFrame, text="MODE:\n0", font=basic_desc_font)

centralMeasures = [max_desc, min_desc, mean_desc, median_desc, mode_desc]
for measure in centralMeasures:
    measure.pack(side="left", padx=30, pady=10)
centralFrame.pack()

dispersionFrame = Frame(basic_desc_page)                                                                                            # Set up Label widgets for dispersion measure
range_desc = Label(dispersionFrame, text="RANGE:\n0", font=basic_desc_font)
std_desc = Label(dispersionFrame, text="STD:\n0", font=basic_desc_font)
var_desc = Label(dispersionFrame, text="VARIABILITY:\n0", font=basic_desc_font)

dispersionMeasures = [range_desc, std_desc, var_desc]
for measure in dispersionMeasures:
    measure.pack(side="left", padx=30, pady=10)
dispersionFrame.pack()

quantileFrame = Frame(basic_desc_page)                                                                                              # Set up Label widgets for quantile measure
qt_desc = Label(quantileFrame, text="QUANTILE:\n0", font=basic_desc_font)
iqr_desc = Label(quantileFrame, text="IQR:\n0", font=basic_desc_font)

qtMeasures = [qt_desc, iqr_desc]
for measure in qtMeasures:
    measure.pack(side="left", padx=30, pady=10)
quantileFrame.pack()

def setColValue() -> None:
    global colVal
    colVal = int(colVal_input.get())

def update_basic_desc():
    global basic_vals

    max_desc.config(text="MAX:\n" + str(basic_vals['max']))
    min_desc.config(text="MIN:\n" + str(basic_vals['min']))
    mean_desc.config(text="MEAN:\n" + str(basic_vals['mean']))
    median_desc.config(text="MEDIAN:\n" + str(basic_vals['median']))
    mode_desc.config(text="MODE:\n" + str(basic_vals['mode']))
    range_desc.config(text="RANGE:\n" + str(basic_vals['range']))
    std_desc.config(text="STD:\n" + str(basic_vals['std']))
    var_desc.config(text="VAR:\n" + str(basic_vals['var']))
    qt_desc.config(text="QUANTILE:\n" + str(basic_vals['quantile']))
    iqr_desc.config(text="IQR:\n" + str(basic_vals['iqr']))

def set_basic_desc_vals() -> None:                                                                                                  # Get all basic statistical description values  
    global basic_vals
    global colVal
    global qtVal

    basic_vals = {'min': 0, 'max': 0, 'mean': 0, 'median': 0, 'mode': 0, 'range': 0, 'std': 0, 'var': 0, 'quantile': 0, 'iqr': 0}

    setColValue()
    setQtVal()

    if colVal < 0 or colVal >= len(ds.dataset.columns):
        raise IndexError("Column does not exist.")
    
    basic_vals['min'] = ds.min(column=colVal)
    basic_vals['max'] = ds.max(column=colVal)
    basic_vals['mean'] = ds.mean(column=colVal)
    basic_vals['median'] = ds.median(column=colVal)
    basic_vals['mode'] = ds.mode(column=colVal)
    basic_vals['range'] = ds.range(column=colVal)
    basic_vals['std'] = ds.std(column=colVal)
    basic_vals['var'] = ds.var(column=colVal)
    basic_vals['quantile'] = ds.quantile(column=colVal, qt=qtVal)
    basic_vals['iqr'] = ds.iqr(column=colVal)

    update_basic_desc() 
    print(basic_vals)   

# Page 3 (Graphs)
graph_title = Label(graph_page, text="Graphs", font=title_font)
graph_title.pack(pady=15)

colList_label = Label(graph_page, text="Enter Column(s):")
colList_label.pack()
colList_input = Entry(graph_page, validate="key", validatecommand=(validate_command, '%P'),width=13, justify="center")
colList_input.pack()

submit_colList_btn = Button(graph_page, text="Submit", command=lambda: setColList())                                                # Input stored as 'colList'
submit_colList_btn.pack(pady=10)

def setColList():   # change to list
    global colList
    colList = int(colList_input.get())
    print(colList)  # int   

show_frame(select_file_page)
root.mainloop()  
