import os.path, sys
from collections import namedtuple

circuit = namedtuple("circuit","PIs POs wires") #named tuple definition, for example use ckt.PIs to get list of Primary inputs

dir_path = os.path.dirname(os.path.realpath(__file__)) #path to file
parent_dir = os.path.abspath(os.path.join(dir_path, os.pardir)) #path to parent dir of file

def read_Netlist(ckt):
    """ takes in ckt filename from benchmarks dir and returns PI, PO, and connections
    as a named tuple of lists (PIs,POs,wires) """

    netlist_file = parent_dir + '/benchmarks/'+ckt

    if not(os.path.isfile(netlist_file)):
        print("File not found please make sure file is in benchmarks folder")
        sys.exit(0)

    # Read file into list line by line
    with open(netlist_file,'r') as f:
        lines = f.read().splitlines()

    # initalize 3 empty lists
    PIs,POs,wires = ([] for i in range(3))
    
    for line in lines:
        splitline = line.split() #split each line from file into list of strings

        if len(splitline) == 0:
            continue

        else:
            if not('$' in splitline[0]):                                 
                if splitline[-1] == 'input' and splitline[0] != '$...':      #index -1 always gets the last element in the list
                    PIs.append(splitline[0])
                    continue
                if splitline[-1] == 'output' and splitline[0] != '$...':
                    POs.append(splitline[0])
                    continue
                wires.append(splitline)                      #if the line doesn't start with $ or end with input/output it's the wiring info

    return circuit(PIs=PIs,POs=POs,wires=wires)

if __name__ == '__main__':
    pass