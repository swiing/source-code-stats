import unittest

from mock import *

from src.utils.count import *


class TestCount(unittest.TestCase):

    def test_count_match(self):
        with patch('builtins.open', 
                   mock_open(read_data='aa\nbb\cc\naa\nbb\cc\n')):
            with open('foo') as file:
                self.assertEqual(count_match(file,"aa"), 2)
