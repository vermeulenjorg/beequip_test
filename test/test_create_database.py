import os
from create_database.create import readfile

def test_read_file():
    """
    Test if read file can read a file
    """
    assert len(readfile(os.getcwd() + '\\data\\customers.csv')) == 8