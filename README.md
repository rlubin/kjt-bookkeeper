# KJT-bookkeeper

## Description

Basic bookkeeping app that processes National Bank of Canada business and credit pdf files and aggregates them into one easy to read csv file.

## Technologies

- Python
- Pandas
- Tabula
- PyInstaller

## Setup

### Requirements

1.  [Python](https://www.python.org/)
2.  [Pandas](https://pypi.org/project/pandas/)

        pip install pandas

3.  [Tabula](https://pypi.org/project/tabula-py/)

        pip install tabula-py

4.  [Pyinstaller](https://pypi.org/project/pyinstaller/)

        pip install pyinstaller

5.  Build executable

        pyinstaller -w -F -n kjt-bookkeeper main.py

## Run

The executable file located /dist/kjt-bookkeeper.exe
py main.py

## Testing

Basic unit tests are included for all classes.

    pytest

## Screenshots

![gui1](screenshots/gui1.PNG 'gui1')
![instructions](screenshots/instructions.PNG 'instructions')
![load](screenshots/load.PNG 'load')
![error](screenshots/error.PNG 'error')
![gui2](screenshots/gui2.PNG 'gui2')
![save](screenshots/save.PNG 'save')