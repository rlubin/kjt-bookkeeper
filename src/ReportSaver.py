import os
import datetime
import csv
import subprocess

class ReportSaver:
  def __init__(self, report):
    self.report = report

  def __createFilePath(self):
    date = datetime.date.today().strftime('%d-%m-%Y')
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

  def __formatTotals(self, totals):
    return [['', 'Revenue', '{:.2f}'.format(totals['revenue'])],
      ['', 'Expenses', '{:.2f}'.format(totals['expenses'])],
      ['', 'Income', '{:.2f}'.format(totals['income'])]]

  def __save(self, path):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)

        formatted_totals = self.__formatTotals(self.report.totals)

        writer.writerows(formatted_totals)
        writer.writerow({})

        cat_totals = []
        for x in range(len(self.report.categories)):
            cat_totals.append(self.report.df_categories[x]["AMOUNT"].sum())

        for x in range(len(self.report.categories)):
            writer.writerow(['', self.report.categories[x], cat_totals[x]])
            writer.writerows(self.report.df_categories[x].values.tolist())
            writer.writerow({})

  def __openFileInExplorer(self, path):
    subprocess.Popen(f'explorer /select, "{path}"')

  def save(self):
    path = self.__createFilePath()
    self.__save(path)
    self.__openFileInExplorer(path)