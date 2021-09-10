from FileChecker import FileChecker

fc = FileChecker()

def test_pdfWithTable():
    assert fc.isGood('Test.pdf') == True

def test_pdfWithoutTable():
    assert fc.isGood('Test2.pdf') == False

def test_csvWithoutTable():
    assert fc.isGood('Test3.csv') == False

def test_csvWithoutTable():
    assert fc.isGood('Test4.csv') == False