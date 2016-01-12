"""
Data files are taken from the ENDF.B-VII.1 release provided by BNL
http://www.nndc.bnl.gov/endf/b7.1/acefiles.html
Files from copied from the 300K data
http://www.nndc.bnl.gov/endf/b7.1/aceFiles/ENDF-B-VII.1-neutron-300K.tar.gz

This is NOT equivalent the MCNP 6.0 files, which were not used due to export controls
However for testing purposes there should be no difference
"""

import unittest
from os import path
import numpy as np

from mcnpy.ace import reader
from tests import utils

ace_test_file = "../data_files/92235.710nc"
ace_test_file_path = path.dirname(__file__) + '/' + ace_test_file


class TestAceReaderFilename(unittest.TestCase):
    def test_extract_substrings(self):
        string = '333444455555'
        expected = ['333', '4444', '55555']
        result = reader.extract_substrings(string, [3, 4, 5])
        self.assertEqual(expected, result)

    def test_sza_to_string(self):
        s, z, a = 1, 92, 235
        expected = '001092235'
        result = reader.sza_to_string(s, z, a)
        self.assertEqual(expected, result)

    def test_string_to_sza(self):
        sza_string = '001092235'
        expected = (1, 92, 235)
        result = reader.string_to_sza(sza_string)
        self.assertEqual(expected, result)

    def test_ace_filename_to_szax(self):
        filename = '92235.711nc'
        expected = (0, 92, 235, 711, 'nc')
        result = reader.ace_filename_to_szax(filename)
        self.assertEqual(expected, result)


class TestAceReaderHeader(unittest.TestCase):
    def test_read_header(self):
        test_header = """\
                      2.0.0      92235.710nc              ENDFB-VII.1             
                      233.024800 2.5301E-08 12/19/12     3
                      The next two lines are the first two lines of 'old-style' ACE.
                       92235.80c  233.024800  2.5301E-08   12/19/12
                      U235 ENDF71x (jlconlin)  Ref. see jlconlin (ref 09/10/2012  10:00:53)    mat9228"""
        test_file = utils.MockFile(test_header)
        expected = reader.header(fmtversion='2.0.0', szax='92235.710nc', source='ENDFB-VII.1',
                                 atwgtr='233.024800', temp='2.5301E-08', date='12/19/12', n='3', 
                                 comments=["The next two lines are the first two lines of 'old-style' ACE.",
                                           "92235.80c  233.024800  2.5301E-08   12/19/12",
                                           "U235 ENDF71x (jlconlin)  Ref. see jlconlin (ref 09/10/2012  10:00:53)    mat9228"])

        result = reader.read_header(test_file)
        self.assertDictEqual(expected._asdict(), result._asdict())

#class TestAceReaderATWGTRTable(unittest.TestCase):
#    def test_read_atwgtr_table(self):
#        test_atwgtr_table = """\
#                                0         0.      0         0.      0         0.      0         0.
#                                0         0.      0         0.      0         0.      0         0.
#                                0         0.      0         0.      0         0.      0         0.
#                                0         0.      0         0.      0         0.      0         0."""
#        test_file = utils.MockFile(test_atwgtr_table)
#        expected = reader.atwgtr_table(za=np.zeros())

if __name__ == '__main__':
    unittest.main()
