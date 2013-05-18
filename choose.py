from tkinter import *
from tkinter.ttk import *

class PipelineSelectWidget(Frame):
    def __init__(self, parent, task, pipelines):
        Frame.__init__(self, parent)

        self.label = Label(self, text=task)
        self.label.pack(side=LEFT)

        self.selected = StringVar()

        self.option_menu = OptionMenu(self, self.selected, *pipelines)
        self.option_menu.pack(side=RIGHT)

class App:
    def __init__(self):
        self.tasks = ['A', 'B', 'C']
        self.pipelines = ['', 'denovo', 'mapping']

    def run(self):
        root = Tk()

        self.title = Label(root, text='Choose Pipelines:')
        self.title.pack()

        for task in self.tasks:
            task_pipeline_widget = PipelineSelectWidget(root, task, self.pipelines)
            task_pipeline_widget.pack()

        root.mainloop()

if __name__ == '__main__':
    a = App()
    a.run()
