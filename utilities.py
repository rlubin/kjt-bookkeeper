import os
import csv

files = []
data = []  # [date, description, amount]
categories = []
groups = {}  # final form of the transaction data
totals = {
    "Revenue": 0.0,
    "Expenses": 0.0,
    "Income": 0.0
}  # rev, exp, inc


def getFiles():
    '''
    read csv files in from desktop
    and store in files
    '''
    desktop_location = os.path.join(os.environ['HOMEPATH'], 'Desktop')
    folder_location = os.path.join(os.getcwd(), 'kjtbk-files')
    # folder_location = os.path.join(desktop_location, 'kjtbk-files')
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
    ['Date', 'Description', 'Reference', 'Withdrawals',
        'Deposits', 'Balance', 'Issuing transit', 'Counterpart']
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
        data.append([row[0], description, amount])


def handleCreditFile(csv_reader):
    '''
    convert credit account info into data
    ['Date', 'Ref.no.', 'Date carried to statement', 'Description',
        'Amount', 'Original currency', 'Original amount']
    '''
    for row in csv_reader:
        # print(row[0], row[3], row[4])
        data.append([row[0], row[3], row[4]])


def categorizeData():
    '''
    go over data
    add all unique descriptions to categories
    '''
    sorted_data = sorted(data)
    for entry in sorted_data:
        if not entry[1] in categories:
            categories.append(entry[1])
        # print(entry)
    # print(data)
    # print(categories)
    # print(len(data))
    # print(len(categories))


def createNewGroups():
    '''
    create a group for each category
    add entries from data to category groups
    need to handle cheques differently
    '''
    groups["CHEQUE"] = []
    for category in categories:
        if category.find("CHEQUE") != -1:
            continue
        groups[category] = []
    for entry in data:
        if entry[1].find("CHEQUE") != -1:
            groups["CHEQUE"].append(entry)
            continue
        groups[entry[1]].append(entry)
    # for key in groups:  # see data
    #     print(key)
    #     for value in groups[key]:
    #         print(value)


def calculateIncome():
    '''
    calculate revenue, expenses and income
    '''
    revenue = 0.0
    expenses = 0.0
    for entry in data:
        amount = float(entry[2])
        if amount > 0:
            revenue += amount
        if amount < 0:
            expenses += abs(amount)
    income = revenue - expenses
    totals["Revenue"] = round(revenue, 2)
    totals["Expenses"] = round(expenses, 2)
    totals["Income"] = round(income, 2)
    # print(totals)
    # print("revenue", round(revenue, 2))
    # print("expenses", round(expenses, 2))
    # print("income", round(income, 2))


def createCSV():
    '''
    create CSV
    '''
    # desktop_location = os.path.join(os.environ['HOMEPATH'], 'Desktop')
    # f = os.path.join(desktop_location, "output.csv")
    f = os.path.join(os.getcwd(), "output.csv")
    if os.path.exists(f):
        os.remove(f)
    with open(f, "w") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["KJT Medicine Prof. Corp."])
        for total in totals.items():
            csv_writer.writerow([total[0], total[1]])
        for key in groups:
            csv_writer.writerow([key])
            for value in groups[key]:
                csv_writer.writerow(value)


def processCSVs(file_paths):
    for f in file_paths:
        files.append(f)
    readFilesIntoData()
    categorizeData()
    createNewGroups()
    calculateIncome()
    createCSV()


# getFiles()
# readFilesIntoData()
# categorizeData()
# createNewGroups()
# calculateIncome()
# createCSV()
