import os
import pandas as pd
import numpy as np
import datetime
import subprocess

# not currently in use
def isBadFile(file_path):
    '''
    check if incompatible files were uploaded
    '''
    df = pd.read_csv(file_path, skiprows=1, error_bad_lines=False)
    if df.empty():
        return True

    credit_account = ["Date", "Ref.no.", "Date carried to statement",
                      "Description", "Amount", "Original currency", "Original amount"]
    business_account = ["Date", "Description", "Reference", "Withdrawals",
                        "Deposits", "Balance", "Issuing transit", "Counterpart"]

    print(type(df.columns.values))
    print(df.columns.values)

    for col in df.columns.values:
        if col not in accepted_columns:
            return True
    return False


def fileTypes(columns):
    '''
    based on columns figure out file types included
    '''
    credit_account = ["Date", "Ref.no.", "Date carried to statement",
                      "Description", "Amount", "Original currency", "Original amount"]
    business_account = ["Date", "Description", "Reference", "Withdrawals",
                        "Deposits", "Balance", "Issuing transit", "Counterpart"]

    credit = True
    business = True

    for cat in credit_account:
        if cat not in columns:
            credit = False

    for cat in business_account:
        if cat not in columns:
            business = False

    if credit and business:
        return "both"
    elif credit:
        return "credit"
    elif business:
        return "business"


def pruneColumns(dataframe, file_types):
    '''
    remove unneeded columns based on file_types
    '''
    keep_cols = []
    if file_types == "both":
        keep_cols = ["Date", "Description", "Reference",
                     "Withdrawals", "Deposits", "Amount"]
    elif file_types == "credit":
        keep_cols = ["Date", "Description", "Amount"]
    elif file_types == "business":
        keep_cols = ["Date", "Description", "Reference",
                     "Withdrawals", "Deposits"]

    # shrink columns of data to keep_cols
    for col in dataframe.columns:
        if col not in keep_cols:
            del dataframe[col]


def combineColumns(df, file_types):
    '''
    combine columns
    '''
    if file_types == "both":
        # combine description and reference into description
        df["Temp1"] = np.nan
        # print(df["Description"])
        # print(df["Reference"])
        df["Temp1"] = df["Description"] + \
            " " + df["Reference"].fillna("")
        df["Temp1"] = df["Temp1"].str.strip()
        del df["Description"]
        del df["Reference"]
        # later column names
        new_columns = df.columns.values
        # these wont work for dataframes that arent both account csvs
        # print(type(new_columns))
        # print(new_columns)
        index = np.where(new_columns == "Temp1")
        # print(index[0])
        # find column index that is equal to Description then use it to change
        new_columns[index[0]] = "Description"
        df.columns = new_columns

        # combine withdrawals and deposits and amount into amount
        df["Temp2"] = np.nan
        # print(df["Withdrawals"])
        # print(df["Deposits"])
        # print(df["Amount"])
        df["Temp2"] = -df["Withdrawals"].fillna(
            0) + df["Deposits"].fillna(0) + df["Amount"].fillna(0)
        del df["Withdrawals"]
        del df["Deposits"]
        del df["Amount"]
        # later column names
        new_columns = df.columns.values
        # these wont work for dataframes that arent both account csvs
        # print(type(new_columns))
        # print(new_columns)
        index = np.where(new_columns == "Temp2")
        # print(index[0])
        # find column index that is equal to Amount then use it to change
        new_columns[index[0]] = "Amount"
        df.columns = new_columns
    elif file_types == "credit":
        pass
    elif file_types == "business":
        # combine description and reference into description
        df["Temp1"] = np.nan
        # print(df["Description"])
        # print(df["Reference"])
        df["Temp1"] = df["Description"] + \
            " " + df["Reference"].fillna("")
        df["Temp1"] = df["Temp1"].str.strip()
        del df["Description"]
        del df["Reference"]
        # later column names
        new_columns = df.columns.values
        # these wont work for dataframes that arent both account csvs
        # print(type(new_columns))
        # print(new_columns)
        index = np.where(new_columns == "Temp1")
        # print(index[0])
        # find column index that is equal to Description then use it to change
        new_columns[index[0]] = "Description"
        df.columns = new_columns

        # combine withdrawals and deposits and amount into amount
        df["Temp2"] = np.nan
        # print(df["Withdrawals"])
        # print(df["Deposits"])
        # print(df["Amount"])
        df["Temp2"] = -df["Withdrawals"].fillna(
            0) + df["Deposits"].fillna(0)
        del df["Withdrawals"]
        del df["Deposits"]
        # later column names
        new_columns = df.columns.values
        # these wont work for dataframes that arent both account csvs
        # print(type(new_columns))
        # print(new_columns)
        index = np.where(new_columns == "Temp2")
        # print(index[0])
        # find column index that is equal to Amount then use it to change
        new_columns[index[0]] = "Amount"
        df.columns = new_columns


def filter_cheques(description):
    '''
    used to filter cheques from data
    '''
    chq = "CHEQUE"
    if chq in str(description):
        return False
    else:
        return True


def splitIntoCategories(df, file_types):
    '''
    split dataframe into smaller dfs based on description
    return categories and df_categories
    '''
    # split data into sub dataframe for like descriptions
    descriptions = df["Description"].values
    # print(len(descriptions))
    # print(descriptions)
    unique_descriptions = []
    for description in descriptions:
        if description not in unique_descriptions:
            unique_descriptions.append(description)

    # print(len(unique_descriptions))
    # for ud in unique_descriptions:
    #     print(ud)

    # create group that the data will be split into
    # group all cheques
    categories = None
    if file_types == "buiness" or file_types == "both":
        categories = filter(filter_cheques, unique_descriptions)
        categories = list(categories)
        categories.append("CHEQUES")
    else:
        categories = unique_descriptions
        categories = list(categories)
    categories.append("OTHER")
    # print(type(categories))
    categories = list(categories)
    # print(categories)
    # print(len(categories))

    # if NaN values exist, remove them from dataframe
    if df.isnull().values.any():
        categories.remove(np.nan)

    # for cat in categories:
    # print(type(cat))
    # print(cat)

    # split df into categories
    # print(len(df))

    # fill NaN's in dataframe with OTHER (should be for description)
    df = df.fillna("OTHER")

    df_categories = []
    for cat in categories:
        # print(cat)
        if cat == "CHEQUES":
            # print(df.loc[df["Description"].str.contains("CHEQUE")])
            df_categories.append(pd.DataFrame(
                df.loc[df["Description"].str.contains("CHEQUE")]))
        else:
            # print(df.loc[df["Description"] == cat])
            df_categories.append(pd.DataFrame(
                df.loc[df["Description"] == cat]))

    return categories, df_categories


# def processAndSave(file_paths, save_file_path):
def processAndSave(file_paths):
    '''
    process csv files
    and save to specified location
    '''
    # create a massive dataframe from all of the files
    # date description amount

    files = []
    for fp in file_paths:
        files.append(fp)

    dfs = []

    for f in files:
        dfs.append(pd.read_csv(f, skiprows=1, error_bad_lines=False))

    data = pd.DataFrame()

    # create big df of all data
    for df in dfs:
        data = pd.concat([data, df], ignore_index=True)

    # figure out what files have been included
    file_types = fileTypes(data.columns)

    # remove unnessecary file
    pruneColumns(data, file_types)

    # combine columns in correct way
    combineColumns(data, file_types)

    # order data by date
    data = data.sort_values(by="Date")

    # remove rows where amount is 0
    data = data[(data[["Amount"]] != 0).all(axis=1)]
    # print(data)

    # remove df entries where description column contains word points
    data = data[data["Description"].str.contains("POINTS") == False]

    # split into different categories
    categories, df_categories = splitIntoCategories(data, file_types)
    # print(df_categories)

    # size = 0
    # for x in range(len(df_categories)):
    #     print(type(categories[x]))
    #     print(categories[x])
    #     print(df_categories[x])
    # print(len(df))
    # size += len(df)
    # print(size)

    # calculate revenue, expenses and income
    # print(data.loc[data["Amount"] > 0])
    # print(data.loc[data["Amount"] < 0])
    revenue = data.loc[data["Amount"] > 0]["Amount"].sum()
    expenses = data.loc[data["Amount"] < 0]["Amount"].sum()
    income = revenue + expenses
    # print("Revenue: {:.2f}".format(revenue))
    # print("Expenses: {:.2f}".format(expenses))
    # print("Income: {:.2f}".format(income))
    # print()

    # calculate cost or gain of each category
    # for x in range(len(df_categories)):
    #     amount = df_categories[x]["Amount"].sum()
    #     print(categories[x] + ": {:.2f}".format(amount))
    #     print(df_categories[x])
    #     print()

    # create and save document
    # with open(save_file_path, mode="w") as f:
    #     f.write("Revenue: {:.2f}\n".format(revenue))
    #     f.write("Expenses: {:.2f}\n".format(expenses))
    #     f.write("Income: {:.2f}\n".format(income))
    #     for x in range(len(df_categories)):
    #         amount = df_categories[x]["Amount"].sum()
    #         f.write("\n" + categories[x] + ": {:.2f}".format(amount) + "\n")
    #         for index, row in df_categories[x].iterrows():
    #             f.write(str(row["Date"]) + "\t" + str(row["Description"]
    #                                                   ) + "\t" + str(row["Amount"]) + "\n")

    date = datetime.date.today().strftime('%Y-%m-%d')
    file_name = f'kjt-report-{date}.txt'
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    file_path = os.path.join(desktop, file_name)
    file_duplication_number = 1

    while os.path.isfile(file_path):
        file_name = f'kjt-report-{date}({file_duplication_number}).txt'
        file_path = os.path.join(desktop, file_name)
        file_duplication_number += 1
        
    print(file_path)

    with open(file_path, mode="w") as f:
        f.write("Revenue: {:.2f}\n".format(revenue))
        f.write("Expenses: {:.2f}\n".format(expenses))
        f.write("Income: {:.2f}\n".format(income))
        for x in range(len(df_categories)):
            amount = df_categories[x]["Amount"].sum()
            f.write("\n" + categories[x] + ": {:.2f}".format(amount) + "\n")
            for index, row in df_categories[x].iterrows():
                f.write(str(row["Date"]) + "\t" + str(row["Description"]
                                                      ) + "\t" + str(row["Amount"]) + "\n")

    # subprocess.Popen(f'exploer /select, "{file_path}"')


# # business
# fp_acc1 = os.path.join(os.getcwd(), "kjtbk-files",
#                        "20200906160739.csv")
# # credit
# fp_acc2 = os.path.join(os.getcwd(), "kjtbk-files",
#                        "20200906161139.csv")
# # business
# fp_acc3 = os.path.join(os.getcwd(), "kjtbk-files",
#                        "20210430193744.csv")
# # credit
# fp_acc4 = os.path.join(os.getcwd(), "kjtbk-files",
#                        "20210430193830.csv")

# fp_acc5 = os.path.join(os.getcwd(), "kjtbk-files",
#                        "POINTS_TEST.csv")

# files = [fp_acc5]

# # files = [fp_acc1]
# # files = [fp_acc2]
# # files = [fp_acc1, fp_acc2]
# # files = [fp_acc2, fp_acc1]
# # files = [fp_acc3]
# files = [fp_acc4]
# # files = [fp_acc3, fp_acc4]
# # files = [fp_acc1, fp_acc2, fp_acc3, fp_acc4]

# save = os.path.join(os.getcwd(), "kjtbk-files", "t.txt")

# processAndSave(files, save)
