from read_Netlist import read_Netlist
from benchmarkrunner import benchmarkrunner,printCircuit
from circuit import circuit

def main():
    #benchmarkrunner()      #use to print data of all benchmark circuits
    ckt_file = "t4_21.ckt"
    ckt = read_Netlist(ckt_file)  #use to read one circuits data
    #printCircuit(ckt,ckt_file)
    print(ckt.wires)

    ckt_obj = circuit()
    ckt_obj.gates = [x[0] for x in ckt.wires]
    types = [x[1] for x in ckt.wires]
    ckt_obj.PIs = ckt.PIs
    ckt_obj.POs = ckt.POs

    type_map = {}
    input_map = {}

    for gates,ckt_type in zip(ckt_obj.gates,types):
        type_map[gates] = ckt_type
        
    for gates,inputs in zip(ckt_obj.gates,ckt.wires):
        input_map[gates] = inputs[2:]

    for k,v in type_map.items():
        print(k,v)

    for k,v in input_map.items():
        print(k,v)

if __name__ == '__main__':
    main()