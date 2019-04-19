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
        """
        ckt = circuit()
        ckt.makeCkt("t4_21.ckt")
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt.write_to_CNF_file("10gat",0)[1], [1,1,0,0,0])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt.write_to_CNF_file("10gat",1)[1], [0,0,0,0,0])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt.write_to_CNF_file("8gat",0)[1], [1,0,1,0,1])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt.write_to_CNF_file("8gat",1)[1], [1,1,0,0,0])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt.write_to_CNF_file("7gat",0)[1], [0,0,1,1,0])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt.write_to_CNF_file("7gat",1)[1], [1,1,0,0,0])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt.write_to_CNF_file("6gat",0)[1], [0,0,0,0,0])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt.write_to_CNF_file("6gat",1)[1], [1,1,0,0,0])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt.write_to_CNF_file("5gat",0)[1], [1,1,0,0,1])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt.write_to_CNF_file("5gat",1)[1], [1,1,0,0,0])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt.write_to_CNF_file("4gat",0)[1], [0,0,1,1,0])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt.write_to_CNF_file("4gat",1)[1], [0,0,1,0,0])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt.write_to_CNF_file("3gat",0)[1], [0,1,1,0,0])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt.write_to_CNF_file("3gat",1)[1], [0,1,0,0,0])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt.write_to_CNF_file("2gat",0)[1], [1,1,0,0,0])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt.write_to_CNF_file("2gat",1)[1], [1,0,0,0,0])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt.write_to_CNF_file("1gat",0)[1], [1,1,0,0,0])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt.write_to_CNF_file("1gat",1)[1], [0,1,0,0,0])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt.write_to_CNF_file(["6gat","3gat"],0)[1], [0,0,1,0,0])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt.write_to_CNF_file(["6gat","3gat"],1)[1], [0,0,0,0,0])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt.write_to_CNF_file(["7gat","3gat"],0)[1], [0,0,1,1,0])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt.write_to_CNF_file(["7gat","3gat"],1)[1], [1,1,0,1,0])
        print ("----------------------------------------\n========================================")
        
        del ckt
        """
        ckt2 = circuit()
        ckt2.makeCkt("t4_3.ckt") #the test it has a #before them they are MISSING a 4 bit
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt2.write_to_CNF_file("8gat",0)[1], [0,0,0,1])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt2.write_to_CNF_file("8gat",1)[1], [0,0,0,0])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt2.write_to_CNF_file("7gat",0)[1], [1,0,1,0])       # missing last input
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt2.write_to_CNF_file("7gat",1)[1], [0,0,0,0])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt2.write_to_CNF_file("6gat",0)[1], [0,0,0,1])
        print ("----------------------------------------\n========================================")
 
        self.assertEqual(ckt2.write_to_CNF_file("6gat",1)[1], [1,0,0,1])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt2.write_to_CNF_file("5gat",0)[1], [1,0,1,0])       # missing last input
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt2.write_to_CNF_file("5gat",1)[1], [1,0,0,0])       # missing last input
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt2.write_to_CNF_file("4gat",0)[1], [0,0,0,1])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt2.write_to_CNF_file("4gat",1)[1], [0,0,0,0])
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt2.write_to_CNF_file("3gat",0)[1], [1,0,1,0])       # missing last input
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt2.write_to_CNF_file("3gat",1)[1], [1,0,0,0])       # missing last input
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt2.write_to_CNF_file("2gat",0)[1], [1,1,0,0])       # missing last input
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt2.write_to_CNF_file("2gat",1)[1], [1,0,0,0])       # missing last input
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt2.write_to_CNF_file("1gat",0)[1], [1,0,1,0])       # missing last input
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt2.write_to_CNF_file("1gat",1)[1], [0,0,1,0])
        print ("----------------------------------------\n========================================")

        #self.assertEqual(ckt2.write_to_CNF_file(["7gat","1gat"],0)[1], [1,0,1,0])
        #print ("----------------------------------------\n========================================")

        self.assertEqual(ckt2.write_to_CNF_file(["7gat","1gat"],1)[1], [0,0,1,0])
        print ("----------------------------------------\n========================================")
        
        self.assertEqual(ckt2.write_to_CNF_file(["6gat","1gat"],0)[1], [0,0,0,1])        #Not gate fan out
        print ("----------------------------------------\n========================================")

        self.assertEqual(ckt2.write_to_CNF_file(["6gat","1gat"],1)[1], [1,0,0,1])        #Not gate fan out
        print ("----------------------------------------\n========================================")


if __name__ == '__main__':
    unittest.main(exit=False)