from BadFileWindow import BadFileWindow
import tkinter as tk
from tkinter import filedialog
from FileChecker import FileChecker

class OpenFileWindow():
  def __init__(self, file_paths_org):
      '''
      allow user to load pdf files
      alter file_paths
      '''
      file_paths = file_paths_org
      files = filedialog.askopenfiles(
          initialdir="/", title="Select files", filetypes=(("PDF Files", "*.pdf"), ))
      for file in files:
          # don't allow duplicate file paths
          if file.name not in file_paths:
              file_paths.append(file.name)
      # check for bad files and remove them
      bad_files = []
      fc = FileChecker()
      for x in range(len(file_paths)):
          if fc.isGood(file_paths[x]) == False:
              bad_files.append(file_paths[x])
      bad_files.reverse()
      for bad_file in bad_files:
          if bad_file in file_paths:
              file_paths.remove(bad_file)
      if len(bad_files) > 0:
          self.showBadFiles(bad_files)
      return file_paths

  def showBadFiles(self, files):
    BadFileWindow(files)