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
            pass
            #! D algorithmn goes here
            pass
        elif num == 4:
            try:
                compilecppcode = subprocess.call("g++" + " main.cpp", shell=True)
                if compilecppcode < 0:
                    print("Process was terminated by signal", -compilecppcode, file=sys.stderr)
                else:
                    print("Compilation returned", compilecppcode, file=sys.stderr)
            except OSError as e:
                print("Compilation failed:", e, file=sys.stderr)

            runexe = subprocess.call("./a.out", shell=True)
        elif num == 5:
            sys.exit(0)
        else:
            print("Invalid input!")
    
if __name__ == '__main__':
    main()