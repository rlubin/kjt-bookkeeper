from Statement import Statement
from Report import Report
from ReportSaver import ReportSaver
import os
import datetime

file = os.path.join(os.getcwd(), 'test', 'files', 'Test.pdf')
s = Statement(file)
r = Report([s])
rs = ReportSaver(r)

date = datetime.date.today().strftime('%Y-%m-%d')
ext = 'csv'
desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')

def test_didSave():
  before_files = os.listdir(desktop)
  rs.save()
  after_files = os.listdir(desktop)
  difference = set(before_files).symmetric_difference(set(after_files))
  list_difference = list(difference)
  assert len(list_difference) == 1