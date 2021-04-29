import tkinter as tk
from tkinter import filedialog
import utilities as ut


class App():

    file_paths = []

    def __init__(self):
        '''
        window setup
        '''
        self.root = tk.Tk()
        self.root.title("KJT Bookkeeper")
        self.root.geometry("300x250")
        self.root.minsize(300, 250)

        self.listbox_frame = tk.Frame(self.root)
        self.listbox = tk.Listbox(
            self.listbox_frame, selectmode=tk.EXTENDED)
        self.y_scrollbar = tk.Scrollbar(self.listbox_frame)
        self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.y_scrollbar.set)
        self.y_scrollbar.config(command=self.listbox.yview)
        self.x_scrollbar = tk.Scrollbar(
            self.listbox_frame, orient=tk.HORIZONTAL)
        self.x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.listbox.config(xscrollcommand=self.x_scrollbar.set)
        self.x_scrollbar.config(command=self.listbox.xview)
        self.listbox.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.listbox_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.button_frame = tk.Frame(self.root)
        self.load_button = tk.Button(self.button_frame, text="Load file(s)",
                                     command=self.loadFiles)
        self.load_button.pack(side=tk.TOP, fill=tk.X)
        self.del_button = tk.Button(
            self.button_frame, text="Delete file(s)", command=self.deleteFiles)
        self.del_button.pack(side=tk.TOP, fill=tk.X)
        self.proc_button = tk.Button(
            self.button_frame, text="Process file(s)", command=self.processFiles)
        self.proc_button.pack(side=tk.TOP, fill=tk.X)
        self.button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.root.mainloop()

    def loadFiles(self):
        '''
        allow user to load csv files
        '''
        csv_files = filedialog.askopenfiles(
            # initialdir="/", title="Select files", filetypes=(("CSV Files", "*.csv"), ))
            initialdir="C:/Users\Ryan/Google Drive/Software/In Progress/kjt-bookkeeper/kjtbk-files", title="Select files", filetypes=(("CSV Files", "*.csv"), ))
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
        delete highlighted file(s) from listbox and file_paths
        '''
        indexes = self.listbox.curselection()
        files = []
        indexes = list(indexes)
        indexes.reverse()
        # delete from listbox
        for index in indexes:
            files.append(self.listbox.get(index))
        for index in indexes:
            self.listbox.delete(index)
        # delete from file_paths
        to_del = []
        for file_path in self.file_paths:
            file_name = file_path[file_path.rfind("/")+1:]
            if file_name in files:
                to_del.append(self.file_paths.index(file_path))
        to_del.reverse()
        for i in to_del:
            self.file_paths.pop(i)

    def processFiles(self):
        '''
        process the selected files
        '''
        ut.processCSVs(self.file_paths)


app = App()
