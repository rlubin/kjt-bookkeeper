import tkinter as tk
from tkinter import filedialog
# import utilities as ut


class App():

    file_paths = []

    def __init__(self):
        '''
        window setup
        '''
        self.root = tk.Tk()
        self.root.title("KJT Bookkeeper")
        self.root.geometry("300x500")
        self.root.resizable(0, 0)

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.load_button = tk.Button(self.frame, text="Load",
                                     command=self.loadFiles)
        self.load_button.pack()

        self.listbox = tk.Listbox(
            self.frame, selectmode=tk.EXTENDED, width=40)
        # self.y_scrollbar = tk.Scrollbar(self.listbox)
        # self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # self.listbox.config(yscrollcommand=self.y_scrollbar.set)
        # self.y_scrollbar.config(command=self.listbox.yview)
        # self.x_scrollbar = tk.Scrollbar(
        #     self.listbox, orient=tk.HORIZONTAL)
        # self.x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        # self.listbox.config(xscrollcommand=self.x_scrollbar.set)
        # self.x_scrollbar.config(command=self.listbox.xview)
        self.listbox.pack()

        self.del_button = tk.Button(
            self.frame, text="Delete file(s)", command=self.deleteFiles)
        self.del_button.pack()

        self.root.mainloop()

    def loadFiles(self):
        '''
        allow user to load csv files
        '''
        csv_files = filedialog.askopenfiles(
            initialdir="/", title="Select files", filetypes=(("CSV Files", "*.csv"), ))
        for csv_file in csv_files:
            # don't allow duplicate file paths
            if csv_file.name not in self.file_paths:
                self.file_paths.append(csv_file.name)
        self.updateListbox()

    def updateListbox(self):
        '''
        clear and update listbox
        '''
        # clear listbox
        self.listbox.delete(0, "end")
        # populate listbox
        for file_path in self.file_paths:
            # just output the file name, not path
            file_name = file_path[file_path.rfind("/")+1:]
            self.listbox.insert("end", file_name)

    def deleteFiles(self):
        '''
        delete highlighted file(s) from listbox and files
        '''
        indexes = self.listbox.curselection()
        files = []
        indexes = list(indexes)
        indexes.reverse()
        for index in indexes:
            files.append(self.listbox.get(index))
        # must delete largest number first then work way down
        for index in indexes:
            self.listbox.delete(index)
        for file_path in self.file_paths:
            file_name = file_path[file_path.rfind("/")+1:]
            if file_name in files:
                self.file_paths.remove(file_path)


app = App()
