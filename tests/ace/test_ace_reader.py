"""
Data files are taken from the ENDF.B-VII.1 release provided by BNL
http://www.nndc.bnl.gov/endf/b7.1/acefiles.html
Files from copied from the 300K data
http://www.nndc.bnl.gov/endf/b7.1/aceFiles/ENDF-B-VII.1-neutron-300K.tar.gz

This is NOT equivalent the MCNP 6.0 files, which were not used due to export controls
However for testing purposes there should be no difference
"""

import unittest

from mcnpy.ace import reader

class TestAceReader(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()
