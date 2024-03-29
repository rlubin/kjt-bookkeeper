from src.Statement import Statement
from src.Report import Report
import pandas as pd
import os

file = os.path.join(os.getcwd(), 'test', 'files', 'Test.pdf')
s = Statement(file)
r = Report([s])

def test_statements():
  assert isinstance(r.statements, list)
  for statement in r.statements:
    assert isinstance(statement, Statement)

def test_categories():
  assert isinstance(r.categories, list)
  for category in r.categories:
    assert isinstance(category, str)

def test_df_categories():
  assert isinstance(r.df_categories, list)
  for category in r.df_categories:
    assert isinstance(category, pd.DataFrame)

def test_totals():
  keys = r.totals.keys()
  assert 'revenue' in keys
  assert 'expenses' in keys
  assert 'income' in keys