from read_Netlist import read_Netlist
from benchmarkrunner import benchmarkrunner,printCircuit
from circuit import circuit

def main():
    #benchmarkrunner()      #use to print data of all benchmark circuits
    ckt_file = "t4_21.ckt"
    #ckt_file = "t4_3.ckt"
    ckt = read_Netlist(ckt_file)  #use to read one circuits data
   

    myckt = makeCkt(ckt_file)
    for k,v in myckt.items():
        print(k,v)
        #print(myckt[k][0]['type'])
        #print(myckt[k][1])
    
    


def makeCkt(ckt_file):
    ckt = read_Netlist(ckt_file)  #use to read one circuits data

    ckt_obj = circuit()
    ckt_obj.gates = [x[0] for x in ckt.wires]
    types = [x[1] for x in ckt.wires]
    ckt_obj.PIs = ckt.PIs
    ckt_obj.POs = ckt.POs

    type_map = {}
    input_map = {}
    PI_value_map = {}

    for gates in ckt_obj.PIs:
        PI_value_map[gates] = "x"
    
    for gates,ckt_type in zip(ckt_obj.gates,types):
        type_map[gates] = ckt_type
        
    for gates,inputs in zip(ckt_obj.gates,ckt.wires):
        input_map[gates] = inputs[2:]
   
    for k in input_map:
        if len(input_map[k]) == 2:
            input_map[k]= [input_map[k][0],"x",input_map[k][1],"x"]
        else:
            input_map[k] = [input_map[k][0],"x"]
    
    for k in input_map:
        #input_map[k].insert(0,{'type': type_map[k]})
        input_map[k].append({'type': type_map[k]})
        #input_map[k]['type'] = type_map[k]
        Type = type_map[k]
        getc = lambda x: 0 if x == 'and' or x == 'nand' else 1
        geti = lambda x: 0 if x == 'and' or x == 'or' else 1
        cXORi = lambda c,i: c ^ i
        cbarXORi = lambda c,i: int(not c ^ i)
        input_map[k].append( {"c" : getc(Type)} ) 
        input_map[k].append( {"i" : geti(Type)} )
        input_map[k].append ( {"cXORi" : cXORi(getc(Type),geti(Type)) } )
        input_map[k].append( {"cbarXORi": cbarXORi(getc(Type),geti(Type)) } )
        input_map[k].append({'output': 'x'})

    return input_map

if __name__ == '__main__':
    main()