'''
import unittest

from mcnpy.ptrac import reader

class Test_ptrac_reader(unittest.TestCase):

    def setUp(self):
        folder = 'data_files'
        filename = 'ptrac'
        path = folder + '/' + filename
        self.file = open(path, 'r')

    def tearDown(self):
        self.file.close()

    def test_header(self):
        header = reader.

if __name__ == '__main__':
    unittest.main()
'''