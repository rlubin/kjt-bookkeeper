# KJT-bookkeeper

## Description

Basic bookkeeping app that processes National Bank of Canada business and credit pdf files and aggregates them into one easy to read csv file.

## Technologies

- Python
- Pandas
- Tabula
- PyInstaller
- PyTest

## Setup

### Requirements

1.  [Python](https://www.python.org/)
2.  [Java](https://www.java.com/en/download/manual.jsp)
3.  [Pandas](https://pypi.org/project/pandas/)

        pip install pandas

4.  [Tabula](https://pypi.org/project/tabula-py/)

        pip install tabula-py

5.  [Pyinstaller](https://pypi.org/project/pyinstaller/)

        pip install pyinstaller

6.  Build executable

        pyinstaller -w -F -n kjt-bookkeeper main.py

7.  [PyTest](https://pypi.org/project/pytest/)

        pip install pytest

## Run

The executable file located at /dist/kjt-bookkeeper.exe <br />
or

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
