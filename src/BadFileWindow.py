import tkinter as tk

class BadFileWindow():
  def __init__(self, files, x = None ,y = None):
      '''
      pop up that shows bad files
      '''
      # new toplevel window setup
      bad_file_window = tk.Toplevel()
      bad_file_window.title("Bad Files")
      width = 300
      init_height = 75
      height_per_line = 20
      if (x == None and y == None):
          bad_file_window.geometry(f"{width}x{init_height + (height_per_line*len(files))}")
      else:
        bad_file_window.geometry(f"{width}x{init_height + (height_per_line*len(files))}+{int(x)+10}+{int(y)+10}")
      bad_file_window.resizable(0, 0)

      title_label = tk.Label(bad_file_window, text="Bad Files")
      title_label.pack(side=tk.TOP)
      for file in files:
          file_name = file[file.rfind("/")+1:]
          label = tk.Label(
          bad_file_window, text=file_name, anchor=tk.W, justify=tk.LEFT)
          label.pack(expand=True, fill=tk.X)

      button = tk.Button(
          bad_file_window, text="OK", command=bad_file_window.destroy, width=10)
      button.pack(side=tk.BOTTOM)