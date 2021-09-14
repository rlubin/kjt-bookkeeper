from src.FileChecker import FileChecker
import os

fc = FileChecker()
print(os.getcwd())

def test_pdfWithTable():
    assert fc.isGood(os.path.join(os.getcwd(), 'test', 'files', 'Test.pdf')) == True

def test_pdfWithoutTable():
    assert fc.isGood(os.path.join(os.getcwd(), 'test', 'files', 'Test2.pdf')) == False

def test_csvWithoutTable():
    assert fc.isGood(os.path.join(os.getcwd(), 'test', 'files', 'Test3.csv')) == False

def test_csvWithoutTable():
    assert fc.isGood(os.path.join(os.getcwd(), 'test', 'files', 'Test4.csv')) == False