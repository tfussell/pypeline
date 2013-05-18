import tkinter
from tkinter import ttk

class ScriptOptionsPane(ttk.Frame):
    def __init__(self, script, parent):
        # label: name
        name_frame = ttk.Frame(parent)
        ttk.Label(name_frame, text=script.get_name()).pack()
        tkinter.OptionMenu(name_frame, 'denovo', 'mapping')
        # dropdown: pipeline
        # per pipeline parameter widgets: label + text

class OptionsWindow(object):
    def __init__(self):
        self.options = {}

    def get_options(self, scripts):
        root = tkinter.Tk()

        for script in scripts:
            ScriptOptionsPane(script, root).pack()

        root.mainloop()
