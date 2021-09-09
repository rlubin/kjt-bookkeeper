import pytest
from Statement import Statement
from Report import Report
import os
import pandas as pd

dir = os.path.join(os.getcwd(), 'kjtbk-files')
files = [os.path.join(dir, x) for x in os.listdir(dir)]
s = Statement(files[0])
s2 = Statement(files[1])
r = Report([s])
r2 = Report([s, s2])

def test_properties():
  assert isinstance(r.statements, Statement)
  assert isinstance(r.categories, list)
  assert isinstance(r.df_categories, list)
  assert hasattr(r.totals, 'revenue')
  assert hasattr(r.totals, 'expenses')
  assert hasattr(r.totals, 'income')