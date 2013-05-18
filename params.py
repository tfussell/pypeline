from tkinter import *
from tkinter.ttk import *

class ParamSelectWidget(Frame):
    def __init__(self, parent, task, parameters):
        Frame.__init__(self, parent)

        self.label = Label(self, text=task)
        self.label.grid(row=0, column=0)

        self.selected = StringVar()

        for i, param_name in enumerate(parameters):
            Label(self, text=param_name).grid(row=i+1, column=1, sticky=E)

            if parameters[param_name]:
                Label(self, text=parameters[param_name]).grid(row=i+1, column=2, sticky=W)
            else:
                Entry(self).grid(row=i+1, column=2, sticky=W)

class App:
    def __init__(self):
        self.tasks = ['A', 'B', 'C']

    def run(self):
        root = Tk()

        params_file = open('params', 'r')
        params = dict()

        for line in params_file:
            split = line.split()
            name = split[0]
            value = split[1:] if len(split) > 1 else None
            params[name] = value

        self.title = Label(root, text='Parameters:')
        self.title.pack()

        for task in self.tasks:
            param_widget = ParamSelectWidget(root, task, params)
            param_widget.config(border=2, relief=SUNKEN)
            param_widget.pack()

        root.mainloop()

if __name__ == '__main__':
    a = App()
    a.run()
