from read_Netlist import read_Netlist
from benchmarkrunner import benchmarkrunner,printCircuit
from circuit import circuit

def main():
    #benchmarkrunner()      #use to print data of all benchmark circuits
    ckt_file = "t4_21.ckt"
    ckt = read_Netlist(ckt_file)  #use to read one circuits data
   
if __name__ == '__main__':
    main()