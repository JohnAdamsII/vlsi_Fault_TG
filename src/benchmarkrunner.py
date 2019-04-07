import os
from read_Netlist import read_Netlist

dir_path = os.path.dirname(os.path.realpath(__file__)) #path to file
parent_dir = os.path.abspath(os.path.join(dir_path, os.pardir)) #path to parent dir of file

def benchmarkrunner():
    file_map = {}
    for index, file in enumerate(os.listdir(parent_dir+'/benchmarks/')):
        if file.endswith(".ckt"):
            file_map[index] = file
    
    for k,v in file_map.items():
        print('['+str(k)+']',v)
    
    num_Files = len(file_map.keys())
    print(num_Files,"circuits detected! Please select the corresponding number to read the netlist")
    selection = int(input(""))

    #print(file_map.get(selection, "Invalid input"))
    ckt = read_Netlist(file_map[selection])
    printCircuit(ckt,file_map[selection])
    return file_map[selection]
           
def printCircuit(ckt,file):
    print("Circuit: %s\n" % file)
    print("Primary Inputs: ")
    print(str(ckt.PIs)+"\n")
    print("Primary Ouputs: ")
    print(str(ckt.POs)+"\n")
    print("Gates: ")
    [print(x) for x in ckt.wires]
    print("\n")
                   
if __name__ == '__main__':
    benchmarkrunner()