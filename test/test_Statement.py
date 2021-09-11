import pytest
from Statement import Statement
import os
import pandas as pd

dir = os.path.join(os.getcwd(), 'kjtbk-files')
files = [os.path.join(dir, x) for x in os.listdir(dir)]
s = Statement(files[0])

def test_properties():
  assert s.path == files[0]
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