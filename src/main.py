from read_Netlist import read_Netlist
from benchmarkrunner import benchmarkrunner,printCircuit
from circuit import circuit
import sys

def main():

    menu = {
        0: "[0] Read the input net-list",
        1: "[1] Perform fault collapsing",
        2: "[2] List fault classes",
        3: "[3] Generate tests (D-Algorithm)",
        4: "[4] Generate tests (Boolean satisfaibility)",
        5: "[5] Exit"
    }
    
    print('\n')
    [print(x) for x in menu.values()]
    print('\n')
    
    ckt_read = False

    while(True):
        num = int(input("Enter a number from 0 to 5: "))

        if num == 0:
            ckt_file = benchmarkrunner()
            ckt_read = True
        elif num == 1:
            if ckt_read:
                ckt = circuit()
                ckt.makeCkt(ckt_file)
                print("Fault Universe after collapsing: ")
                print(ckt.collapseFaults())
            else:
                print("Please read in netlist first")
        elif num == 2:
            if ckt_read:
                ckt = circuit()
                ckt.makeCkt(ckt_file)
                print("All SSFs before collapsing: ")
                print(ckt.getFaultList())
            else:
                print("Please read in netlist first")
        elif num == 3:
            print("")
        elif num == 5:
            sys.exit(0)
        else:
            print("Invalid input!")
    

   
    



    #benchmarkrunner()      #use to print data of all benchmark circuits
    #ckt_file = "t4_21.ckt"
    #ckt = read_Netlist(ckt_file)  #use to read one circuits data
   
if __name__ == '__main__':
    main()