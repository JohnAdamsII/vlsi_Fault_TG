import os
from read_Netlist import read_Netlist

dir_path = os.path.dirname(os.path.realpath(__file__)) #path to file
parent_dir = os.path.abspath(os.path.join(dir_path, os.pardir)) #path to parent dir of file

def benchmarkrunner():
    for file in os.listdir(parent_dir+'/benchmarks/'):
        if file.endswith(".ckt"):
            ckt = read_Netlist(file)
            printCircuit(ckt,file)
           
def printCircuit(ckt,file):
    print("Circuit: %s\n" % file)
    print("Primary Inputs: ")
    print(str(ckt.PIs)+"\n")
    print("Primary Ouputs: ")
    print(str(ckt.POs)+"\n")
    print("Wires: ")
    [print(x) for x in ckt.wires]
    print("\n")
                   
if __name__ == '__main__':
    benchmarkrunner()