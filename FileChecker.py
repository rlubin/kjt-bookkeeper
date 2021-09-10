import tabula

class FileChecker():
  def __checkPdf(self, path):
    if path.endswith('.pdf'):
      return {'checkPdf': True}
    return {'checkPdf': False}

  def __checkHasTable(self, path):
    try:
      df = tabula.read_pdf(path, pages='all')
      if df:
        return {'checkHasTable': True}
      return {'checkHasTable': False}
    except:
      return {'checkHasTable': False}

  def isGood(self, path):
    errors = []
    errors.append(self.__checkPdf(path))
    errors.append(self.__checkHasTable(path))
    for key in errors:
      if False in key.values():
        return False
    return True