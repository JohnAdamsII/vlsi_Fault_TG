import os
from read_Netlist import read_Netlist
dir_path = os.path.dirname(os.path.realpath(__file__)) #path to file
parent_dir = os.path.abspath(os.path.join(dir_path, os.pardir)) #path to parent dir of file

def benchmarkrunner():
    for file in os.listdir(parent_dir+'/benchmarks/'):
        if file.endswith(".ckt"):
            var = read_Netlist(file)
        
            #print(os.path.join(parent_dir+'/benchmarks/', file))






if __name__ == '__main__':
    benchmarkrunner()