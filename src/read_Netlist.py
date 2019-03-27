import os.path, sys, re
dir_path = os.path.dirname(os.path.realpath(__file__)) #path to file
parent_dir = os.path.abspath(os.path.join(dir_path, os.pardir)) #path to parent dir of file

def read_Netlist(ckt):
    """ takes in ckt file from benchmarks dir in cwd and returns PI, PO, and connections
    as a tuple of lists (PI,PO,connections) """
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
        #split each line from file into list of strings and remove empty strings
        splitline = list(filter(None, line.split(" ")))

        if len(splitline) == 0:
            continue

        else:
        #if line doesn't begin with $
            if not('$' in splitline[0]):
                        
                # index -1 always gets the last element in the list
                if splitline[-1] == 'input' and splitline[0] != '$...':
                    PIs.append(splitline[0])
                    continue
                if splitline[-1] == 'output' and splitline[0] != '$...':
                    POs.append(splitline[0])
                    continue

                # if the line doesn't start with $ or end with input/output it's the wiring info
                wires.append(splitline)

    print("Primary Inputs: ")
    [print(x) for x in PIs]
    print("Primary Outputs: ")
    [print(x) for x in POs]
    print("Connections: ")

    #remove tabs due to bs formatting
    wires = list(filter(lambda a: len(a) != 1, wires))
    [print(x) for x in wires]
    
    return (PIs,POs,wires)

if __name__ == '__main__':
    pass