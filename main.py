from tkinter import *
from tkinter import filedialog
from classes.Data import Data

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
        for F in (SelectFilePage, BasicDescPage, GraphPage):
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

        options = [select_file_option, basic_desc_option, graph_option]

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
        select_file_button.pack(expand=True)

    def open_file(self):
        global ds
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filepath:
            ds = Data(filepath)

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

        graph_validate_command = self.register(validate_input_list)

        colList_label = Label(self, text="Enter Column(s):")
        colList_label.pack()
        self.colList_input = Entry(self, validate="key", validatecommand=(graph_validate_command, '%S'), width=13, justify="center")
        self.colList_input.pack()

        colorList_label = Label(self, text="Enter Color(s):")
        colorList_label.pack()
        self.colorList_input = Entry(self, width=13, justify="center")
        self.colorList_input.pack()

        graph_options_frame = Frame(self)
        graph_options_frame.pack()
        scatter_btn = Button(graph_options_frame, text="Scatter Plot")
        line_btn = Button(graph_options_frame, text="Line Graph")

        graph_options = [scatter_btn, line_btn]

        for option in graph_options:
            option.pack(side="left", padx=10, pady=10)

# Helper functions
def validate_input_digit(new_value) -> bool:
    return new_value == "" or new_value.isdigit()

def validate_input_list(char):
    return char.isdigit() or char == " "

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
