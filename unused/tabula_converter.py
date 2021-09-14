import tabula
import os
import pandas as pd
import datetime
import csv
import subprocess

def convertPdfToDf(file):
  return tabula.read_pdf(file, pages='all')[0]

def convertPdfsToDfs(files):
  dfs = []
  for file in files:
    dfs.append(convertPdfToDf(file))
  return dfs

def mergeDfs(dfs):
  return pd.concat(dfs, ignore_index=True)

def createAmountColumn(df):
  df['AMOUNT'] = -df['DEBIT'].fillna(
            0) + df['CREDIT'].fillna(0)
  return df

def removeUnusedColumns(df):
  return df.drop(columns=['DEBIT', 'CREDIT','BALANCE'])

def removeZeroAmountRows(df):
  return df[df['AMOUNT'] != 0]

def isCheque(description):
    '''
    used to filter cheques from data
    '''
    chq = "CHEQUE"
    if chq in str(description):
        return False
    else:
        return True

def splitIntoCategories(df):
    '''
    split dataframe into smaller dfs based on description
    return categories and df_categories
    '''
    # split data into sub dataframe for like descriptions
    descriptions = df["DESCRIPTION"].values
    unique_descriptions = []
    for description in descriptions:
        if description not in unique_descriptions:
            unique_descriptions.append(description)

    # create group that the data will be split into
    # group all cheques
    categories = None
    categories = filter(isCheque, unique_descriptions)
    categories = list(categories)
    categories.append("CHEQUES")
    categories.append("OTHER")
    categories = list(categories)

    # fill NaN's in dataframe with OTHER (should be for description)
    df = df.fillna("OTHER")

    df_categories = []
    for cat in categories:
        if cat == "CHEQUES":
            df_categories.append(pd.DataFrame(
                df.loc[df["DESCRIPTION"].str.contains("CHEQUE")]))
        else:
            df_categories.append(pd.DataFrame(
                df.loc[df["DESCRIPTION"] == cat]))

    return categories, df_categories

def calculateTotals(df):
  revenue = df.loc[df["AMOUNT"] > 0]["AMOUNT"].sum()
  expenses = df.loc[df["AMOUNT"] < 0]["AMOUNT"].sum()
  income = revenue + expenses
  return {'revenue': revenue, 'expenses': expenses, 'income': income}

def formatTotals(totals):
  return [['', 'Revenue', '{:.2f}'.format(totals['revenue'])],
    ['', 'Expenses', '{:.2f}'.format(totals['expenses'])],
    ['', 'Income', '{:.2f}'.format(totals['income'])]]

def createFilePath():
  date = datetime.date.today().strftime('%Y-%m-%d')
  ext = 'csv'
  file_name = f'kjt-report-{date}.{ext}'
  desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
  file_path = os.path.join(desktop, file_name)
  file_duplication_number = 1

  while os.path.isfile(file_path):
      file_name = f'kjt-report-{date}({file_duplication_number}).{ext}'
      file_path = os.path.join(desktop, file_name)
      file_duplication_number += 1
  
  return file_path

def saveFile(path, totals, categories, df_categories):
  with open(path, 'w', newline='') as f:
      writer = csv.writer(f)

      writer.writerows(totals)
      writer.writerow({})

      cat_totals = []
      for x in range(len(categories)):
          cat_totals.append(df_categories[x]["AMOUNT"].sum())

      for x in range(len(categories)):
          writer.writerow(['', categories[x], cat_totals[x]])
          writer.writerows(df_categories[x].values.tolist())
          writer.writerow({})

def openFileInExplorer(path):
  subprocess.Popen(f'explorer /select, "{path}"')

# create files list
dir = os.path.join(os.getcwd(), os.pardir, 'kjtbk-files', 'NBC')
files = []
for file_path in os.listdir(dir):
    files.append(os.path.join(dir, file_path))

# work
dfs = convertPdfsToDfs(files)
aggregate_df = mergeDfs(dfs)
df_with_amount = createAmountColumn(aggregate_df)
df_pruned = removeUnusedColumns(df_with_amount)
df_no_zeros = removeZeroAmountRows(df_pruned)
categories, df_categories = splitIntoCategories(df_no_zeros)
totals = calculateTotals(df_no_zeros)
formatted_totals = formatTotals(totals)
path = createFilePath()
saveFile(path, formatted_totals, categories, df_categories)
openFileInExplorer(path)