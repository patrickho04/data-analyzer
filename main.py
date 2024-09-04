import csv
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from classes.Data import Data
from classes.PreprocessData import PreprocessData

class MainApp(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("900x600")
        self.title("Statistics Analyzer")
        self.resizable(False, False)

        # Create navbar
        navbar = Frame(self, bg="lightgray")
        navbar.pack(side=TOP, fill="x")

        # Container for pages
        container = Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to store frames
        self.frames = {}

        # Loop to initialize pages
        for F in (SelectFilePage, BasicDescPage, GraphPage, PreprocessPage, RegressionPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the initial frame
        self.show_frame("SelectFilePage")

        # Navbar options
        select_file_option = Button(navbar, text="Select File", command=lambda: self.show_frame("SelectFilePage"))
        basic_desc_option = Button(navbar, text="Basic Desc.", command=lambda: self.show_frame("BasicDescPage"))
        graph_option = Button(navbar, text="Graphs", command=lambda: self.show_frame("GraphPage"))
        preprocess_option = Button(navbar, text="Preprocess", command=lambda: self.show_frame("PreprocessPage"))
        regression_option = Button(navbar, text="Regression", command=lambda: self.show_frame("RegressionPage"))

        options = [select_file_option, basic_desc_option, graph_option, preprocess_option, regression_option]

        for option in options:
            option.pack(side="left", padx=10, pady=10)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class SelectFilePage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title_font = ('Bold', 13)
        select_title = Label(self, text="Select CSV Title", font=title_font)
        select_title.pack(pady=15)

        select_file_button = Button(self, text="Select File", command=self.open_file)
        select_file_button.pack(pady=15)

        self.selectTree = ttk.Treeview(self, show="headings")
        self.selectTree.pack(padx=20, pady=20, fill="both", expand=True)
    
    def display_csv_file(self,file_path):
        with open(file_path, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)                                                       # Read the header row
            self.selectTree.delete(*self.selectTree.get_children())                         # Clear the current data

            self.selectTree["columns"] = header
            for col in header:
                self.selectTree.heading(col, text=col)
                self.selectTree.column(col, width=100)

            for row in csv_reader:
                self.selectTree.insert("", "end", values=row)

    def open_file(self):
        global ds
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filepath:
            ds = PreprocessData(filepath)
            self.display_csv_file(filepath)

class BasicDescPage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title_font = ('Bold', 13)
        basic_desc_font = ('Times', 12)

        desc_title = Label(self, text="Basic Description Page", font=title_font)
        desc_title.pack(pady=10)

        basic_validate_command = self.register(validate_input_digit)

        colVal_label = Label(self, text="Enter Column:")
        colVal_label.pack()
        self.colVal_input = Entry(self, validate="key", validatecommand=(basic_validate_command, '%P'), width=13, justify="center")
        self.colVal_input.pack()

        qnt_label = Label(self, text="Enter Quantile (in %):")
        qnt_label.pack()
        self.qnt_input = Entry(self, validate="key", validatecommand=(basic_validate_command, '%P'), width=13, justify="center")
        self.qnt_input.pack()

        submit_colVal_btn = Button(self, text="Submit", command=self.set_basic_desc_vals)
        submit_colVal_btn.pack(pady=10)

        self.centralFrame = Frame(self)
        self.centralFrame.pack()

        self.max_desc = Label(self.centralFrame, text="MAX:\n0", font=basic_desc_font)
        self.min_desc = Label(self.centralFrame, text="MIN:\n0", font=basic_desc_font)
        self.mean_desc = Label(self.centralFrame, text="MEAN:\n0", font=basic_desc_font)
        self.median_desc = Label(self.centralFrame, text="MEDIAN:\n0", font=basic_desc_font)
        self.mode_desc = Label(self.centralFrame, text="MODE:\n0", font=basic_desc_font)

        centralMeasures = [self.max_desc, self.min_desc, self.mean_desc, self.median_desc, self.mode_desc]
        for measure in centralMeasures:
            measure.pack(side="left", padx=30, pady=10)

        self.dispersionFrame = Frame(self)
        self.dispersionFrame.pack()

        self.range_desc = Label(self.dispersionFrame, text="RANGE:\n0", font=basic_desc_font)
        self.std_desc = Label(self.dispersionFrame, text="STD:\n0", font=basic_desc_font)
        self.var_desc = Label(self.dispersionFrame, text="VARIABILITY:\n0", font=basic_desc_font)

        dispersionMeasures = [self.range_desc, self.std_desc, self.var_desc]
        for measure in dispersionMeasures:
            measure.pack(side="left", padx=30, pady=10)

        self.quantileFrame = Frame(self)
        self.quantileFrame.pack()

        self.qt_desc = Label(self.quantileFrame, text="QUANTILE:\n0", font=basic_desc_font)
        self.iqr_desc = Label(self.quantileFrame, text="IQR:\n0", font=basic_desc_font)

        qtMeasures = [self.qt_desc, self.iqr_desc]
        for measure in qtMeasures:
            measure.pack(side="left", padx=30, pady=10)

    def set_basic_desc_vals(self):
        global basic_vals, colVal, qtVal

        basic_vals = {'min': 0, 'max': 0, 'mean': 0, 'median': 0, 'mode': 0, 'range': 0, 'std': 0, 'var': 0, 'quantile': 0, 'iqr': 0}

        colVal = int(self.colVal_input.get())
        qtVal = int(self.qnt_input.get()) / 100

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

        self.update_basic_desc()

    def update_basic_desc(self):
        global basic_vals
        self.max_desc.config(text="MAX:\n" + str(basic_vals['max']))
        self.min_desc.config(text="MIN:\n" + str(basic_vals['min']))
        self.mean_desc.config(text="MEAN:\n" + str(basic_vals['mean']))
        self.median_desc.config(text="MEDIAN:\n" + str(basic_vals['median']))
        self.mode_desc.config(text="MODE:\n" + str(basic_vals['mode']))
        self.range_desc.config(text="RANGE:\n" + str(basic_vals['range']))
        self.std_desc.config(text="STD:\n" + str(basic_vals['std']))
        self.var_desc.config(text="VAR:\n" + str(basic_vals['var']))
        self.qt_desc.config(text="QUANTILE:\n" + str(basic_vals['quantile']))
        self.iqr_desc.config(text="IQR:\n" + str(basic_vals['iqr']))

class GraphPage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title_font = ('Bold', 13)
        graph_title = Label(self, text="Graphs", font=title_font)
        graph_title.pack(pady=15)

        graph_validate_command = self.register(validate_input_digList)

        # Graph inputs
        graphInputFrame = Frame(self)
        colList_label = Label(graphInputFrame, text="Enter Column(s):")
        colList_label.grid(row=0, column=0, padx=7)
        self.colList_input = Entry(graphInputFrame, validate="key", validatecommand=(graph_validate_command, '%S'), width=13, justify="center")
        self.colList_input.grid(row=1, column=0, padx=7)

        colorList_label = Label(graphInputFrame, text="Enter Color(s):")
        colorList_label.grid(row=0, column=1, padx=7)
        self.colorList_input = Entry(graphInputFrame, width=13, justify="center")
        self.colorList_input.grid(row=1, column=1, padx=7)

        xTitle_label = Label(graphInputFrame, text="X Title:")
        xTitle_label.grid(row=0, column=2, padx=7)
        self.xTitle_input = Entry(graphInputFrame, width=13, justify="center")
        self.xTitle_input.grid(row=1, column=2, padx=7)
        graphInputFrame.pack()

        graph_options_frame = Frame(self)
        graph_options_frame.pack()
        scatter_btn = Button(graph_options_frame, text="Scatter Plot",
                             command=lambda: (setColList(), setColorList(), setXTitle(), ds.scatter_plot(columns=colList, colors=colorList, xlabel=xTitle)))
        line_btn = Button(graph_options_frame, text="Line Graph",
                          command=lambda: (setColList(), setColorList(), setXTitle(), ds.line_chart(columns=colList, colors=colorList, xlabel=xTitle)))
        box_btn = Button(graph_options_frame, text="Box Plot", command=lambda: (setColList(), setXTitle(), ds.box_plot(column=colList[0], xlabel=xTitle)))

        graph_options = [scatter_btn, line_btn, box_btn]

        for option in graph_options:
            option.pack(side="left", padx=10, pady=10)

        def setColList():
            global colList
            colList = clean_string(self.colList_input.get()).split()
            colList = [int(item) for item in colList]

        def setColorList():
            global colorList
            colorList = clean_string(self.colorList_input.get()).split()    # fix (takes in int when not supposed to)

        def setXTitle():
            global xTitle
            xTitle = self.xTitle_input.get()

class PreprocessPage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title_font = ('Bold', 13)
        preprocess_title = Label(self, text="Preprocess Data", font=title_font)
        preprocess_title.pack(pady=15)

        # Preprocess input
        pp_input_label = Label(self, text="Enter paramaters:")
        pp_input_label.pack()
        pp_input = Entry(self)
        pp_input.pack()

        ppOptionsFrame = Frame(self)
        replace_missing_data_btn = Button(ppOptionsFrame, text="Replace Missing Data (lower, upper)",
                                      command=lambda: (setPpList(), ds.replace_missing_data(lower=ppList[0], upper=ppList[1]), display_ppdata()))
        one_hot_encode_btn = Button(ppOptionsFrame, text="One Hot Encode (column)",
                                    command=lambda: (setPpList(), ds.one_hot_encode(column=ppList[0]), display_ppdata()))
        label_encode_btn = Button(ppOptionsFrame, text="Label Encode (lower, upper)",
                                  command=lambda: (setPpList(), ds.label_encode(column=ppList[0]), display_ppdata()))
        split_sets_btn = Button(ppOptionsFrame, text="Split Sets ()",
                                command=lambda: (setPpList(), ds.split_train_test(), display_ppdata()))
        standardize_btn = Button(ppOptionsFrame, text="Standardize (list, lower, upper)",
                                 command=lambda: (setPpList(), ds.standardize(ppList[0], ppList[1], ppList[2]), display_ppdata()))

        pp_options = [replace_missing_data_btn, one_hot_encode_btn, label_encode_btn, standardize_btn]

        for btn in pp_options:
            btn.pack(padx=7, pady=10, side=LEFT)

        ppOptionsFrame.pack()

        ppTree = ttk.Treeview(self, show="headings")
        ppTree.pack(padx=20, pady=20, fill="both", expand=True)

        def setPpList():
            global ppList
            ppList = clean_string(pp_input.get()).split()
            ppList = [int(item) if item.isdigit() else item for item in ppList]

        def display_ppdata():
            ppTree.delete(*ppTree.get_children())

            columns = list(range(ds.npdataset.shape[1]))
            ppTree["columns"] = columns

            for col in columns:
                ppTree.heading(col, text=f"Column {col}")
                ppTree.column(col, width=500)

            for row in ds.npdataset:
                ppTree.insert("", "end", values=row)

class RegressionPage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title_font = ('Bold', 13)
        select_title = Label(self, text="Regression Modeling", font=title_font)
        select_title.pack(pady=15)

# Helper functions
def validate_input_digit(char) -> bool:
    # Only digits
    return char == "" or char.isdigit()

def validate_input_digList(char):
    # Only digits and spaces
    return char.isdigit() or char == " "

def validate_input_str(char) -> bool:
    #Only letters and spaces
    return char.isalpha() or char.isspace()          

def clean_string(string):
    # Split string by whitespace and join with a single space
    return ' '.join(string.split())

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
