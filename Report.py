import pandas as pd
import os
from Statement import Statement

class Report:
  def __init__(self, statements=[]):
    self.statements = statements
    self.categories = None
    self.df_categories = None
    self.totals = None

  def addStatement(self, statement):
    self.statements.append(statement)

  def __mergeStatementDfs(self):
    dfs = []
    for statement in self.statements:
      dfs.append(statement.df)
    return pd.concat(dfs, ignore_index=True)

  def __isCheque(self, description):
    '''
    used to filter cheques from data
    '''
    chq = "CHEQUE"
    if chq in str(description):
        return False
    else:
        return True

  def __splitIntoCategories(self, df):
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
    categories = filter(self.__isCheque, unique_descriptions)
    categories = list(categories)
    categories.append("CHEQUES")
    # categories.append("OTHER")
    categories = list(categories)

    # fill NaN's in dataframe with OTHER (should be for description)
    # df = df.fillna("OTHER")

    df_categories = []
    for cat in categories:
        if cat == "CHEQUES":
            df_categories.append(pd.DataFrame(
                df.loc[df["DESCRIPTION"].str.contains("CHEQUE")]))
        else:
            df_categories.append(pd.DataFrame(
                df.loc[df["DESCRIPTION"] == cat]))

    return categories, df_categories

  def __containsPositive(self, array):
    for ele in array:
      if ele > 0:
        return True
    return False

  def __sortCategories(self, categories, df_categories):
    '''
    sort categories first by largest to smallest positive
    then by largest to smallest negative
    '''
    category_totals = []
    for i in range(0, len(categories)):
      category_totals.append(df_categories[i]['AMOUNT'].sum())

    sorted_category_totals = []
    sorted_categories = []
    sorted_df_categories = []

    for i in range(0, len(categories)):
      if self.__containsPositive(category_totals):
        max_value = max(category_totals)
        max_index = category_totals.index(max_value)
      else:
        max_value = min(category_totals)
        max_index = category_totals.index(max_value)
      sorted_category_totals.append(category_totals[max_index])
      sorted_categories.append(categories[max_index])
      sorted_df_categories.append(df_categories[max_index])
      del category_totals[max_index]
      del categories[max_index]
      del df_categories[max_index]

    # for i in range(0, len(sorted_category_totals)):
    #   print(sorted_category_totals[i])
    #   print(sorted_categories[i])
    #   print(sorted_df_categories[i])

    return sorted_categories, sorted_df_categories
    

  def __calculateTotals(self, df):
    revenue = df.loc[df["AMOUNT"] > 0]["AMOUNT"].sum()
    expenses = df.loc[df["AMOUNT"] < 0]["AMOUNT"].sum()
    income = revenue + expenses
    return {'revenue': revenue, 'expenses': expenses, 'income': income}

  def buildReport(self):
    df = self.__mergeStatementDfs()
    categories, df_categories = self.__splitIntoCategories(df)
    self.categories, self.df_categories = self.__sortCategories(categories, df_categories)
    self.totals = self.__calculateTotals(df)
    


# create files list
# dir = os.path.join(os.getcwd(), 'kjtbk-files', 'NBC')
# files = []
# for file_path in os.listdir(dir):
#     files.append(os.path.join(dir, file_path))

# rp = Report()
# rp.addStatement(Statement(files[0]))
# rp.buildReport()

# build Statement objects
# for file in files:
#   st = Statement(file)
#   rp.addStatement(st)

# for statement in rp.statements:
#   print(statement)

# rp.buildReport()

# print(rp.categories)
# print(rp.df_categories)
# print(rp.totals)