from read_Netlist import read_Netlist
from benchmarkrunner import benchmarkrunner,printCircuit
from circuit import circuit
import sys, subprocess

def main():

    menu = {
        0: "[0] Read the input net-list",
        1: "[1] Perform fault collapsing",
        2: "[2] List fault classes",
        3: "[3] Generate tests (D-Algorithm)",
        4: "[4] Generate tests (Boolean satisfaibility)",
        5: "[5] Exit"
    }
    
  
    ckt_read = False
    collapsed = False

    while(True):
        print('\n')
        [print(x) for x in menu.values()]
        print('\n')

        num = input("Enter a number from 0 to 5: ")

        #! Read netlist option
        if num == "0":
            ckt_file = benchmarkrunner()
            ckt_read = True
            ckt = circuit()
            ckt.makeCkt(ckt_file)
        #! perform fault collapsing option
        elif num == "1":
            if ckt_read:
                collapsed_fault_list = ckt.collapseFaults()
                print(collapsed_fault_list)
                collapsed = True
            else:
                print("Please read in netlist first")
        #! print fault list option
        elif num == "2":
            if ckt_read and not(collapsed):
                #ckt = circuit()
                #ckt.makeCkt(ckt_file)
                print("All SSFs before collapsing: ")
                [print(x) for x in ckt.getFaultList()]
            elif ckt_read and collapsed:
                print("Collapsed fault list: ")
                print(collapsed_fault_list)
            else:
                print("Please read in netlist first")
        #! perform D algorithmn option
        elif num == "3":
            pass
        #! use Set Solver option
        elif num == "4":
            if ckt_read and not(collapsed):
                #ckt = circuit()
                #ckt.makeCkt(ckt_file)
                fault_list = ckt.getFaultList()
                new_fault_list = ckt.formatFaultlist(fault_list)

                for fault in new_fault_list:
                    gate,stuck_at_value = fault[0],int(fault[1])
                    ckt.setSolver(gate,stuck_at_value)[1]
            
            elif ckt_read and collapsed:
                new_fault_list = ckt.formatFaultlist(collapsed_fault_list)

                for fault in new_fault_list:
                    gate,stuck_at_value = fault[0],int(fault[1])
                    ckt.setSolver(gate,stuck_at_value)[1]
            else:
                print("Please read in netlist first")
        #! exit option
        elif num == "5":
            sys.exit(0)
        else:
            print("Invalid input!")
    
if __name__ == '__main__':
    main()