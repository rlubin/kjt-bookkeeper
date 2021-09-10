from Statement import Statement
from Report import Report
import pandas as pd

s = Statement('Test.pdf')
r = Report([s])

def test_statementsProp():
  assert isinstance(r.statements, list)
  for statement in r.statements:
    assert isinstance(statement, Statement)

def test_categoriesProp():
  assert isinstance(r.categories, list)
  for category in r.categories:
    assert isinstance(category, str)

def test_df_categoriesProp():
  assert isinstance(r.df_categories, list)
  for category in r.df_categories:
    assert isinstance(category, pd.DataFrame)

def test_totalsProp():
  keys = r.totals.keys()
  assert 'revenue' in keys
  assert 'expenses' in keys
  assert 'income' in keys