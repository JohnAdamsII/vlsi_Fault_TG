from read_Netlist import read_Netlist
from benchmarkrunner import benchmarkrunner,printCircuit

def main():
    ckt_file = "t4_21.ckt"
    ckt = read_Netlist(ckt_file)  #use to just one circuits data
    printCircuit(ckt,ckt_file)

    #benchmarkrunner()      #use to print data of all benchmark circuits
  
if __name__ == '__main__':
    main()