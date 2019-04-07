import unittest
import sys,os

dir_path = os.path.dirname(os.path.realpath(__file__)) #path to file
parent_dir = os.path.abspath(os.path.join(dir_path, os.pardir)) #path to parent dir of file
src_path = parent_dir+'/src/'
sys.path.insert(0,src_path)

import circuit

#unit test docs https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug
#run on terminal with python -m unittest test_circuit.py
#or if call unittest.main() (see below) to just run python3 test_circuit.py

class TestCalc(unittest.TestCase):

    def test_SetPIs(self):
        """  Test cases go here """
        pass
        #self.assertEqual(ckt.SetPIs([1,1,1,1]), CORRECT OUTPUT HERE)
    
    def test_collapseFaults(self):
        pass



if __name__ == '__main__':
    unittest.main(exit=False)