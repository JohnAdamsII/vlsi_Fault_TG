import unittest
import sys,os

dir_path = os.path.dirname(os.path.realpath(__file__)) #path to file
parent_dir = os.path.abspath(os.path.join(dir_path, os.pardir)) #path to parent dir of file
src_path = parent_dir+'/src/'
sys.path.insert(0,src_path)

from circuit import circuit

#unit test docs https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug
#run on terminal with python -m unittest test_circuit.py
#or if unittest.main() (see below) to just run python3 test_circuit.py

class test_circuit(unittest.TestCase):

    def test_write_to_CNF_file(self):
        ckt = circuit()
        ckt.makeCkt("t4_21.ckt")
        self.assertEqual(ckt.write_to_CNF_file("4gat",0)[1], [0,0,1,1,0])
        ckt.fault_exp_map = {}



if __name__ == '__main__':
    unittest.main(exit=False)