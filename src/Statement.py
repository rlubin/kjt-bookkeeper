import tabula
# import os
# import datetime

class Statement():
  def __init__(self, path):
    self.path = path
    self.df = self.__buildDf()

  def __convertPdfToDf(self):
    return tabula.read_pdf(self.path, pages='all')[0]

  def __createAmountColumn(self, df):
    df['AMOUNT'] = -df['DEBIT'].fillna(
              0) + df['CREDIT'].fillna(0)
    return df

  def __removeUnusedColumns(self, df):
    return df.drop(columns=['DEBIT', 'CREDIT','BALANCE', 'MM DD'])

  def __removeZeroAmountRows(self, df):
    return df[df['AMOUNT'] != 0]

  def __createDateColumn(self, df):
    # year = os.path.split(self.path)[-1].split('_')[-2][0:4] # makes date from file name
    # year = os.path.getmtime(self.path)
    year = 2021
    df['DATE'] = df['MM DD'].apply(lambda x: x.split(' ')[1] + '-' + x.split(' ')[0] + f'-{year}')
    return df

  def __orderColumns(self, df):
    df = df[['DATE', 'DESCRIPTION', 'AMOUNT']]
    return df

  def __buildDf(self):
    df_init = self.__convertPdfToDf()
    df_date = self.__createDateColumn(df_init)
    df_amount = self.__createAmountColumn(df_date)
    df_cols = self.__removeUnusedColumns(df_amount)
    df_ord = self.__orderColumns(df_cols)
    df_final = self.__removeZeroAmountRows(df_ord)
    return df_final