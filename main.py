import tkinter as tk
from tkinter import filedialog
import utilities as ut


class App():

    file_paths = []

    def __init__(self):
        '''
        window setup
        '''
        # main window setup
        self.root = tk.Tk()
        self.root.title("KJT Bookkeeper")
        self.root.geometry("300x250")
        self.root.minsize(300, 250)

        # listbox setup
        self.listbox_frame = tk.Frame(self.root)
        self.listbox = tk.Listbox(
            self.listbox_frame, selectmode=tk.EXTENDED)
        self.listbox.bind("<Button-1>", self.delButtonEvent)
        self.listbox.bind("<ButtonRelease-1>", self.delButtonEvent)
        self.listbox.bind("<Double-Button-1>", self.delButtonEvent)
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

        # button setup
        self.button_frame = tk.Frame(self.root)
        self.load_button = tk.Button(self.button_frame, text="Load file(s)",
                                     command=self.loadFiles)
        self.load_button.pack(side=tk.TOP, fill=tk.X)
        self.del_button = tk.Button(
            self.button_frame, text="Delete file(s)", command=self.deleteFiles, state=tk.DISABLED)
        self.del_button.pack(side=tk.TOP, fill=tk.X)
        self.desel_button = tk.Button(
            self.button_frame, text="Deselect file(s)", command=self.deselectFiles, state=tk.DISABLED)
        self.desel_button.pack(side=tk.TOP, fill=tk.X)
        self.proc_button = tk.Button(
            self.button_frame, text="Process file(s)", command=self.processFiles, state=tk.DISABLED)
        self.proc_button.pack(side=tk.TOP, fill=tk.X)
        self.howto_button = tk.Button(
            self.button_frame, text="Instructions", command=self.instructions)
        self.howto_button.pack(side=tk.TOP, fill=tk.X)
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
        # clear listbox
        self.listbox.delete(0, "end")
        # populate listbox
        for file_path in self.file_paths:
            # just output the file name, not path
            file_name = file_path[file_path.rfind("/")+1:]
            self.listbox.insert("end", file_name)
        # update button state
        if self.listbox.size() > 0:
            self.proc_button["state"] = tk.NORMAL

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
        # update button states
        self.del_button["state"] = tk.DISABLED
        if self.listbox.size() == 0:
            self.proc_button["state"] = tk.DISABLED

    def processFiles(self):
        '''
        process files and save document
        '''
        save_file = filedialog.asksaveasfile(
            initialdir="/", title="Save file", defaultextension=("Text files", "*.txt"), filetypes=(("Text files", "*.txt"),))
        # initialdir="/", title="Save file", defaultextension=("CSV files", "*.csv"), filetypes=(("CSV files", "*.csv"),))
        save_file_path = save_file.name
        ut.processAndSaveCSV(self.file_paths, save_file_path)

    def instructions(self):
        '''
        explain how to use the app
        '''
        # new toplevel window setup
        insturctions = tk.Toplevel()
        insturctions.title("Instructions")
        insturctions.geometry("325x200")
        insturctions.resizable(0, 0)

        # label setup
        title_label = tk.Label(insturctions, text="Instructions")
        title_label.pack(side=tk.TOP)
        load_label = tk.Label(
            insturctions, text="Load file(s):\nAllows you to upload NBC CSV files", anchor=tk.W, justify=tk.LEFT)
        load_label.pack(expand=True, fill=tk.X)
        del_label = tk.Label(
            insturctions, text="Delete file(s):\nAllows you to delete highlighted files that have been loaded", anchor=tk.W, justify=tk.LEFT)
        del_label.pack(expand=True, fill=tk.X)
        desel_label = tk.Label(
            insturctions, text="Deselect file(s):\nAllows you to deselect highlighted files", anchor=tk.W, justify=tk.LEFT)
        desel_label.pack(expand=True, fill=tk.X)
        proc_label = tk.Label(
            insturctions, text="Process file(s):\nProcesses files and choose where to save it", anchor=tk.W, justify=tk.LEFT)
        proc_label.pack(expand=True, fill=tk.X)

    def deselectFiles(self):
        '''
        clears listbox selection
        '''
        self.listbox.selection_clear(0, tk.END)
        self.del_button["state"] = tk.DISABLED
        self.desel_button["state"] = tk.DISABLED

    def delButtonEvent(self, event):
        '''
        control state of delete and deselect file(s)
        '''
        if self.listbox.size() == 0:
            self.del_button["state"] = tk.DISABLED
            self.desel_button["state"] = tk.DISABLED
        elif len(self.listbox.curselection()) > 0:
            self.del_button["state"] = tk.NORMAL
            self.desel_button["state"] = tk.NORMAL
        else:
            self.del_button["state"] = tk.DISABLED
            self.desel_button["state"] = tk.DISABLED


app = App()
