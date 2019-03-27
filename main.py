import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
# get path to this file

def main():
    netlist = '/benchmarks/t4_21.ckt'

    # Read file into list line by line
    with open(dir_path+netlist,'r') as f:
        lines = f.read().splitlines()

    # initalize 3 empty lists
    PIs,POs,wires = ([] for i in range(3))
    
    for line in lines:
        #split each line from file into list of strings and remove empty strings
        splitline = list(filter(None, line.split(" ")))
    
        #if line doesn't begin with $
        if line[0] != '$':          
            
            # index -1 always gets the last element in the list
            if splitline[-1] == 'input':
                PIs.append(splitline[0])
                continue
            if splitline[-1] == 'output':
                POs.append(splitline[0])
                continue
            # if the line doesn't start with $ or end with input/output it's the wiring info
            wires.append(splitline)

    print("Primary inputs: ")
    print(PIs)
    print("Primary outputs: ")
    print(POs)
    print("Connections: ")
    print(wires)



if __name__ == '__main__':
    main()