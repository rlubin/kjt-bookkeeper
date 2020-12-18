import csv
import os

files = []


def getFiles():
    desktop_location = os.path.join(os.environ['HOMEPATH'], 'Desktop')
    folder_location = os.path.join(desktop_location, 'kjtbk-files')
    os.chdir(folder_location)
    for f in os.listdir():
        files.append(f)


def openFiles():
    for f in files:
        with open(f, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                print(', '.join(row))


getFiles()
print(files)
openFiles()
