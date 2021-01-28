import csv
import os

files = []
data = {
    "Date": [],
    "Description": [],
    "Amount": []  # +amount representing a deposit, -amount representing a withdrawal
}


def getFiles():
    '''
    read csv files in from desktop
    and store in files
    '''
    desktop_location = os.path.join(os.environ['HOMEPATH'], 'Desktop')
    folder_location = os.path.join(desktop_location, 'kjtbk-files')
    os.chdir(folder_location)
    for f in os.listdir():
        files.append(f)
    # print(files)


def readFilesIntoData():
    '''
    read files and convert them
    store relevant info in data
    '''
    for f in files:
        with open(f, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)
            header = next(csv_reader)
            # print(header)
            file_type = fileType(header)
            # print(file_type)
            if file_type == "chequings":
                handleChequingsFile(csv_reader)
            if file_type == "credit":
                handleCreditFile(csv_reader)


def fileType(header):
    '''
    check if file is credit or chequings
    they are grouped differently
    '''
    try:
        header.index("Description") >= 0 and header.index(
            "Reference") >= 0
        return "chequings"
    except ValueError:
        return "credit"


def handleChequingsFile(csv_reader):
    '''
    convert chequings account info into data
    ['Date', 'Description', 'Reference', 'Withdrawals', 'Deposits', 'Balance', 'Issuing transit', 'Counterpart']
    '''
    for row in csv_reader:
        amount = 0.0
        # print(type(row[3]))
        # print(type(row[4]))
        if row[3] != "" and float(row[3]) > 0.0:  # withdrawal
            amount = "-" + str(float(row[3]))
        elif row[4] != "" and float(row[4]) > 0.0:  # desposit
            amount = float(row[4])
        description = row[1] + " " + row[2]
        # print(row[0], description, amount)
        data["Date"].append(row[0])
        data["Description"].append(description)
        data["Amount"].append(amount)


def handleCreditFile(csv_reader):
    '''
    convert credit account info into data
    ['Date', 'Ref.no.', 'Date carried to statement', 'Description', 'Amount', 'Original currency', 'Original amount']
    '''
    for row in csv_reader:
        # print(row[0], row[3], row[4])
        data["Date"].append(row[0])
        data["Description"].append(row[3])
        data["Amount"].append(float(row[4]))


getFiles()
readFilesIntoData()

# for x in range(0, len(data["Date"])):
# print(data["Date"][x], data["Description"][x], data["Amount"][x])
# print(data["Date"][x])
# print(data["Description"][x])
# print(data["Amount"][x])
