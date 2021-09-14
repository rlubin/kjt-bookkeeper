import tkinter as tk

class InstructionsWindow():
  def __init__(self, x, y):
    '''
    explain how to use the app
    '''
    # new toplevel window setup
    insturctions = tk.Toplevel()
    insturctions.title("Instructions")
    insturctions.geometry(f'325x225+{int(x)+10}+{int(y)+10}')
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
        insturctions, text="Process file(s):\nAggegrates all the files you have selected and saves it to your\ndesktop under the name kjt-report-DD-MM-YYYY.csv", anchor=tk.W, justify=tk.LEFT)
    proc_label.pack(expand=True, fill=tk.X)