import pandas as pd
import numpy as np


def processAndSaveCSV(file_paths, save_file_path):
    '''
    process csv files
    and save to specified location
    '''
    # create a massive dataframe from all of the files
    # date description amount

    files = []
    for fp in file_paths:
        files.append(fp)

    # fp_acc1 = os.path.join(os.getcwd(), "kjtbk-files",
    #                        "20200906160739.csv")
    # fp_acc2 = os.path.join(os.getcwd(), "kjtbk-files",
    #                        "20200906161139.csv")

    # files = [fp_acc1, fp_acc2]
    dfs = []

    for f in files:
        dfs.append(pd.read_csv(f, skiprows=1, error_bad_lines=False))

    data = pd.DataFrame()

    # create big df of all data
    for df in dfs:
        data = pd.concat([data, df], ignore_index=True)

    keep_cols = ["Date", "Description", "Reference",
                 "Withdrawals", "Deposits", "Amount"]

    # shrink columns of data to keep_cols
    for col in data.columns:
        if col not in keep_cols:
            del data[col]

    # data.to_csv("./kjtbk-files/temp.csv")

    # combine description and reference into description
    data["Temp1"] = np.nan
    # print(data["Description"])
    # print(data["Reference"])
    data["Temp1"] = data["Description"] + \
        " " + data["Reference"].fillna("")
    data["Temp1"] = data["Temp1"].str.strip()
    del data["Description"]
    del data["Reference"]
    # later column names
    new_columns = data.columns.values
    new_columns[4] = "Description"
    data.columns = new_columns

    # combine withdrawals and deposits and amount into amount
    data["Temp2"] = np.nan
    # print(data["Withdrawals"])
    # print(data["Deposits"])
    # print(data["Amount"])
    data["Temp2"] = -data["Withdrawals"].fillna(
        0) + data["Deposits"].fillna(0) + data["Amount"].fillna(0)
    del data["Withdrawals"]
    del data["Deposits"]
    del data["Amount"]
    # later column names
    new_columns = data.columns.values
    new_columns[2] = "Amount"
    data.columns = new_columns

    # order data by date
    data = data.sort_values(by="Date")

    # data.to_csv("./kjtbk-files/temp.csv")

    # if rows where amount is 0
    data = data[(data[["Amount"]] != 0).all(axis=1)]

    # print(data)
    # data.to_csv("./kjtbk-files/data.csv")

    # split data into sub dataframe for like descriptions
    descriptions = data["Description"].values
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
    def filter_cheques(description):
        chq = "CHEQUE"
        if chq in str(description):
            return False
        else:
            return True
    categories = filter(filter_cheques, unique_descriptions)
    # print(type(categories))
    categories = list(categories)
    # print(categories)
    # print(len(categories))
    categories.append("CHEQUES")
    categories.append("OTHER")
    categories.remove(np.nan)
    # for cat in categories:
    # print(type(cat))
    # print(cat)

    # split data into categories
    # print(len(data))
    data = data.fillna("OTHER")
    df_categories = []
    for cat in categories:
        # print(cat)
        if cat == "CHEQUES":
            # print(data.loc[data["Description"].str.contains("CHEQUE")])
            df_categories.append(pd.DataFrame(
                data.loc[data["Description"].str.contains("CHEQUE")]))
        else:
            # print(data.loc[data["Description"] == cat])
            df_categories.append(pd.DataFrame(
                data.loc[data["Description"] == cat]))

    # size = 0
    # for x in range(len(df_categories)):
        # print(categories[x])
        # print(df_categories[x])
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

    # create document to present data cleanly
    with open(save_file_path, mode="w") as f:
        f.write("Revenue: {:.2f}\n".format(revenue))
        f.write("Expenses: {:.2f}\n".format(expenses))
        f.write("Income: {:.2f}\n".format(income))
        for x in range(len(df_categories)):
            amount = df_categories[x]["Amount"].sum()
            f.write("\n" + categories[x] + ": {:.2f}".format(amount) + "\n")
            for index, row in df_categories[x].iterrows():
                f.write(str(row["Date"]) + "\t" + str(row["Description"]
                                                      ) + "\t" + str(row["Amount"]) + "\n")
