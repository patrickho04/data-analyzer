from Data import Data
from tkinter import *
from tkinter import filedialog

def openFile():
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
        dataset = Data(filepath)
        print(filepath)

window = Tk()
window.geometry("600x400")

select_file_button = Button(text="Select File", command=openFile)
select_file_button.pack(expand=True)

window.mainloop()

