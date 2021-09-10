from Statement import Statement
import pandas as pd
import os

file = os.path.join(os.getcwd(), 'test', 'files', 'Test.pdf')
s = Statement(file)
df = pd.DataFrame.from_dict({'DATE': ['21-12-2021', '01-02-2021'], 'DESCRIPTION': ['One', 'Two'], 'AMOUNT': [-1234.43, 2.3]}) # associated to Test.pdf

def test_properties():
  assert s.path == file
  assert isinstance(s.df, pd.DataFrame)

def test_dfColumns():
  assert (s.df.columns.values == ['DATE', 'DESCRIPTION', 'AMOUNT']).all()

def test_dateTypes():
  assert s.df['DATE'].dtype == 'O'

def test_descriptionTypes():
  assert s.df['DESCRIPTION'].dtype == 'O'

def test_amountTypes():
  assert s.df['AMOUNT'].dtype == 'float64'

def test_zeroRows():
  assert 0 not in s.df['AMOUNT'].tolist()
  assert 'NaN' not in s.df['AMOUNT'].tolist()

def test_resultingDf():
  assert s.df.equals(df)