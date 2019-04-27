# vlsi_Fault_TG

This Project includes software to test very large scale digital circuits. Testing includes generating test vectors for the circuit
and discovering faults.

compile instructions 

    1. Download and unzip our project named “vlsi_Final_Project”
    
    2. Run command $ cd vlsi_Final_Project
    
    3. Run command $ pip3 install sympy
    
    4. Run command $ sudo apt-get install libz-dev
    
    5. Run command $ cd vender/minisat
    
    6. Run command $ make config prefix=$PREFIX
    
    7. Run command $ sudo make install
    
    8. Run command $ mv build/dynamic/bin/minisat $PATH TO vlsi_Final_Project/bin
    
    9. move benchmark (.ckt files) to the project vlsi_Fault_TG/benchmarks
    
    10. cd to project directory vlsi_Final_Project/src
    
    11. run command "python3 main.py"

NOTE: the project only supports .ckt files with gate naming convention of [int]gat and [letter]gat
example: 1gat 2gat 3gat 
or       agat bgat 3gat
