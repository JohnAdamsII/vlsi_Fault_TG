from read_Netlist import read_Netlist
from sympy import to_cnf,symbols,sympify,Xor
import os, subprocess
import string

dir_path = os.path.dirname(os.path.realpath(__file__)) #path to file
parent_dir = os.path.abspath(os.path.join(dir_path, os.pardir)) #path to parent dir of file


class circuit:

    gate_map = {}
    gate_values = {}
    fault_list = []
    collapsed_fault_list = []
    J_frontier = []
    D_frontier = []

    def __init__(self, PIs=[], POs=[], gates=[]):
        self.PIs = PIs
        self.POs = POs
        self.gates = gates

    def makeCkt(self, ckt_file):
        ckt = read_Netlist(ckt_file)  # use to read one circuits data

        self.gates = [x[0] for x in ckt.wires]
        types = [x[1] for x in ckt.wires]
        self.PIs, self.POs = ckt.PIs, ckt.POs

        type_map, input_map = ({} for i in range(2))

        for gates, ckt_type in zip(self.gates, types):
            type_map[gates] = ckt_type.lower()

        for gates, inputs in zip(self.gates, ckt.wires):
            input_map[gates] = inputs[2:]

        for k in input_map:
            if len(input_map[k]) == 2:
                input_map[k] = [[input_map[k][0], input_map[k][1]]]
            else:
                input_map[k] = [[input_map[k][0]]]

        for k in input_map:
            input_map[k].append(type_map[k])
            Type = type_map[k]
            def getc(x): return 0 if x == 'and' or x == 'nand' else (None if x == 'not' else 1)
            def geti(x): return 0 if x == 'and' or x == 'or' else (None if x == 'not' else 1)

            def cXORi(c, i): return None if c == None else c ^ i
            def cbarXORi(c, i): return None if c == None else int(not c ^ i) 
            input_map[k].extend(  [getc(Type),geti(Type),cXORi(getc(Type), geti(Type)),cbarXORi(getc(Type), geti(Type))] )

        for k in input_map:
            if input_map[k][1] == 'not':
                self.gate_values[k] = {input_map[k][0][0]: 'x', 'output': 'x'}
            else:
                self.gate_values[k] = {input_map[k][0][0]: 'x', input_map[k][0][1]: 'x', 'output': 'x'}

        self.gate_map = input_map
        del type_map, input_map

    def c(self, gate):
        return self.gate_map[gate][2]
    
    def i(self, gate):
        #! check this
        return self.gate_map[gate][3]

    def cXORi(self, gate):
        return self.gate_map[gate][4]

    def cbarXORi(self, gate):
        return self.gate_map[gate][5]

    def getType(self, gate):
        return self.gate_map[gate][1]

    def getInputs(self, gate):
        return self.gate_map[gate][0]

    def getInputValue(self, gate, Input):
        return self.gate_values[gate][Input]

    def getFanouts(self, Input):
        fan_outs = []
        for k, v in self.gate_values.items():
            if Input in v:
                fan_outs.append(k)
        return fan_outs

    def setInput(self, gate, Input, value):
        fan_outs = self.getFanouts(Input)
        for fanouts in fan_outs:
            self.gate_values[fanouts][Input] = value
        self.assignOutput(gate)

    def assignOutput(self, gate):
        Inputs = self.getInputs(gate)  # list of inputs
        c = self.c(gate)  # c of gate

        values = []
        for Inputs in Inputs:
            values.append(self.getInputValue(gate, Inputs))

        if self.getType(gate) == 'not':
            self.gate_values[gate]['output'] = int(not(values[0]))
            self.propagate(gate, int(not(values[0])))
        elif c in values:
            self.gate_values[gate]['output'] = self.cXORi(gate)
            self.propagate(gate, self.cXORi(gate))
        elif not(c in values) and not('x' in values):
            self.gate_values[gate]['output'] = self.cbarXORi(gate)
            self.propagate(gate, self.cbarXORi(gate))

    def propagate(self, gate, value):
        fan_outs = self.getFanouts(gate)
        for inputs in fan_outs:
            self.gate_values[inputs][gate] = value

    def setPIs(self, PI_values):
        for index, PI in enumerate(self.PIs):
            for k, v in self.gate_values.items():
                if PI in v:
                    self.gate_values[k][PI] = PI_values[index]

        #! assign all outputs afer setting input
        for gate in self.gates:
            self.assignOutput(gate)

    def getFaultList(self):
        #! Need to add fanout to fault list!
        all_gates = self.gates + self.PIs
        fault_list = []
        
        for gate in all_gates:
            fault_list.extend( [str(gate)+'-0',str(gate)+'-1'] )
          
        self.fault_list = sorted(fault_list, key=lambda x: x[0][0])
        return self.fault_list
    
    def formatFaultlist(self,fault_list):
        new_fault_list = []
        for index,fault in enumerate(fault_list):
            fault = fault_list[index].split("-")
            new_fault_list.append(fault)
        return new_fault_list


    def collapseFaults(self):
         #! Need to add fanout to fault collapsing!
        fault_set = set()
        for gate in self.gates:
            if self.getType(gate) == 'not':
                #! add support for not gates here
                continue
            eq = self.func_eq(gate)
            print("functionally equivalent faults: ","{"+str(eq[0])+","+str(eq[1])+","+str(eq[2])+"}")
            print(str(eq[1])+","+str(eq[2])+" will be removed from fault list")
            if eq:
                fault_set.add(eq[0])

        print("\ndominating relationship such that f dominates g (f,g)") 
        print("f will be removed from fault list")         
        for gate in self.gates:
            if self.getType(gate) == 'not':
                continue
            dom = self.dom(gate)
            print("("+dom[0]+","+dom[1]+")")
            print("("+dom[0]+","+dom[2]+")")
            if dom:
                fault_set.update((dom[1], dom[2]))

        self.collapsed_fault_list = sorted(fault_set, key=lambda x: x[0][0]) #! This may break with different circuit names
        print("\nFault list after collapsing: ")
        return self.collapsed_fault_list

    def func_eq(self, gate):
        #* input s-a-c faults and the output s-a-(c XOR i) are functionally equivalent.
        if self.getType(gate) == 'not':
            return None
        else:
            inputs = self.getInputs(gate)
            return (str(gate)+"-"+str(self.cXORi(gate)), inputs[0]+'-'+str(self.c(gate)), inputs[1]+'-'+str(self.c(gate)))

    def dom(self, gate):
        #* the output s-a-(C' XOR i) fault dominates any input s-a-c'
        if self.getType(gate) == 'not':
            return None
        else:
            inputs = self.getInputs(gate)
            return (str(gate)+"-"+str(self.cbarXORi(gate)), inputs[0]+'-'+str(int(not(self.c(gate)))), inputs[1]+'-'+str(int(not(self.c(gate)))))

    def D_algo(self):
        pass
    
    def getExpr(self,PO,fault_gate="",stuck_at_value="",fanouts=[],fanout=False):

        expr = {}
        
        if len(fanouts) != 0:
            fanout = True
            print("Fanouts: ",fanouts)
            print(fanouts[0],fanouts[1]," Stuck at ",stuck_at_value)
        else:
            expr[fault_gate]= stuck_at_value #! set fault
        
        """ Needs to be tested with a ckt with a not gate """
        for gate in self.gates:

            if gate in expr.keys():
                print(gate," stuck at ",stuck_at_value)
                continue
    
            if self.getType(gate) == 'not':
                Input = self.getInputs(gate)[0]
                if fanout and fanouts[0] == gate and Input == fanouts[1]:
                    expr[gate] = bool(stuck_at_value)
                else:
                    in1 = self.getInputs(gate)[0]
                    s1 = symbols(in1)
                    expr[gate] = ~s1

            if self.getType(gate) == 'nor':
                inputs = []
                for Input in self.getInputs(gate):
                    if fanout and gate == fanouts[0] and Input == fanouts[1]:
                        inputs.append(stuck_at_value)
                    elif Input in expr.keys():
                        inputs.append(expr[Input])
                    else:
                        inputs.append(symbols(Input))

                expr[gate] = ~(inputs[0] | inputs[1])

            if self.getType(gate) == 'nand':
                inputs = []
                for Input in self.getInputs(gate):
                    if fanout and gate == fanouts[0] and Input == fanouts[1]:
                        inputs.append(stuck_at_value)
                    elif Input in expr.keys():
                        inputs.append(expr[Input])
                    else:
                        inputs.append(symbols(Input))
                
                expr[gate] = ~(inputs[0] & inputs[1])
               
            if self.getType(gate) == 'and':
                inputs = []
                for Input in self.getInputs(gate):
                    if fanout and gate == fanouts[0] and Input == fanouts[1]:
                        inputs.append(stuck_at_value)
                    elif Input in expr.keys():
                        inputs.append(expr[Input])
                    else:
                        inputs.append(symbols(Input))
                
                expr[gate] = (inputs[0] & inputs[1])
              
            if self.getType(gate) == 'or':
                inputs = []
                for Input in self.getInputs(gate):
                    if fanout and gate == fanouts[0] and Input == fanouts[1]:
                        inputs.append(stuck_at_value)
                    elif Input in expr.keys():
                        inputs.append(expr[Input])
                    else:
                        inputs.append(symbols(Input))
                
                expr[gate] = (inputs[0] | inputs[1])
                
        return expr[self.POs[PO]] #! ONLY WORKS WITH ONE PO right now

    def get_clauses(self,PO,gate,stuck_at_value,verb,fanouts=[]):
        """ formats circuit expressions into clauses to write to CNF file for set solving
        need to be modify to handle different gate names in other circuits """
        
        #! if no fanout
        if type(gate) != list:
            faulty_expr = self.getExpr(fault_gate=gate,stuck_at_value=stuck_at_value, PO=PO) #get fault expression
        else:
            #! if fanout
            faulty_expr = self.getExpr(stuck_at_value=stuck_at_value,fanouts=gate, PO=PO)
        if verb:
            print("faulty expression is: ",faulty_expr)
        ff_ckt = self.getExpr(PO=PO) #get fault free circuit expression
        if verb:
            print("fault free expression is: ",ff_ckt)
            
        xor_expr = Xor(ff_ckt,faulty_expr) #get xor expr
        xor_expr = to_cnf(xor_expr,simplify=True) #convert xor expr to CNF

        if verb:
            print("faulty XOR fault_free = ",xor_expr)

        if xor_expr == False:
            return "UNDECTECTABLE!"
       
        clauses = str(xor_expr).split("&")

        # if not("gat" in self.POs[0]):
            #call formating function to rename gates
        #     #! Handle stupid circuit names
  
        for index,item in enumerate(clauses):
            clauses[index] = item.strip()
            clauses[index] = clauses[index].replace("(","")
            clauses[index] = clauses[index].replace(")","")
            clauses[index] = clauses[index].replace("~","-")
            clauses[index] = clauses[index].replace("|","")
            clauses[index] = clauses[index].replace("  "," ")
            clauses[index] = clauses[index].replace("gat","") #! THIS WILL BREAK WITH DIFFERENT GATE NAMES!
        
        if self.POs[0][0].isalpha():             #! will need to change for t5_26a
            return self.formatClauses(clauses)  
        else:
            return clauses

    def formatClauses(self,clauses):
        new_clauses = []
        for clause in clauses:
            temp = []
            for index,char in enumerate(clause):
                if char.isalpha():
                    temp.append(string.ascii_lowercase.index(char)+1)
                elif char == " ":
                    temp.append(" ")
                else:
                    temp.append("-")
                if index == len(clause)-1:
                    new_clauses.append(''.join(str(elem) for elem in temp))
        return new_clauses


    def setSolver(self,gate,stuck_at_value,PO=0,verb=True,fanouts=[]):
        """ writes clauses to CNF file and calls miniSAT """
        if gate in self.PIs and verb:
            print(gate,"stuck at ",stuck_at_value)

        if type(gate) == list:
            clauses = self.get_clauses(PO,gate,stuck_at_value,verb,fanouts)
        else:
            clauses = self.get_clauses(PO,gate,stuck_at_value,verb)

        if clauses == "UNDECTECTABLE!":
            clauses = ['1','-1']

        num_Vars = len(self.PIs)
        num_Clasues = len(clauses)
     
        with open(os.path.join(parent_dir+'/bin/','cnf_file'), "w") as f:
            f.write("p cnf "+str(num_Vars)+" "+str(num_Clasues)+'\n')
            for clause in clauses:
                f.write(clause+" 0\n")
        
        return self.runMiniSAT(verb)

    def runMiniSAT(self,verb):
        """ sends cnf file with written clauses to miniSAT solver"""
     
        miniSAT_path = parent_dir + '/bin/minisat'
        cnf_path = parent_dir + '/bin/'
        if verb:
            runminiSAT = subprocess.call(miniSAT_path +" -verb=1 "+cnf_path+'/cnf_file'+" "+cnf_path+"out.txt", shell=True)
        else:
            runminiSAT = subprocess.call(miniSAT_path +" -verb=0 "+cnf_path+'/cnf_file'+" "+cnf_path+"out.txt", shell=True,stdout=open(os.devnull, 'wb'))

        return self.getSAT(verb)
    
    def getSAT(self,verb):
        """ read output of set solver and return if expression is SAT 
        and what vector makes expression true if any  """

        with open(parent_dir+'/bin/out.txt','r') as f:
            lines = f.read().splitlines()
        SAT = True if lines[0] == 'SAT' else False
        if SAT:
            vector = lines[1][:-1].split()
            #print(SAT,vector)
        if SAT:
            final_vec = [0 if '-' in x else 1 for x in vector ]
        if not(SAT):
            return (None,"UNDETECTABLE!")
      
        if SAT and len(final_vec) < len(self.PIs):
            final_vec.extend([0] * (len(self.PIs) - len(final_vec)) )
            if verb:
                print("input vector: ",final_vec," will detect fault!")
            return (SAT, final_vec)
        else: 
            if verb:
                print("input vector: ",final_vec," will detect fault!")   
            return (SAT,final_vec)
    
    
    def imply_and_check(self):
        pass

    def solve(self,l,v):
        test = self.setSolver(gate=l,stuck_at_value=v,verb=0)
        SAT = test[0]
        if SAT:
            print("D has propagated to PO and all lines justified!")
            VEC = test[1]
            print("Test vector: ",VEC," will detect ",l," stuck at ",v)
        
        
    
    def D_algo(self,l,v):

        print("initalizing all values to x")
        [print(k,v) for k,v in ckt.gate_values.items()]
     
        self.D_propagate(l,v)

        print("Assignments from propagation: ")
        [print(k,v) for k,v in ckt.gate_values.items()]

        ckt.makeJFrontier()
        print("J frontier is: ", ckt.J_frontier)

        ckt.makeDFrontier()
        print("D frontier is: ", ckt.D_frontier)
    
        self.solve(l=l,v=v)
    
    def D_propagate(self,l,v):
        PO = self.POs[0]
        
        #! Base case
        if self.gate_values[PO]['output'] == 'D' or self.gate_values[PO]['output'] == '~D':
            print("SUCCESSFUL PROPAGATIONS!")
            return "SUCCESS"
          
        g = self.getOutput(l) #! current gate output

        if g == None:
            return 'FAILURE'
        
        #! setting l to err
        if v == 0:
            self.gate_values[g][l] = 'D'
            for gate in self.getFanouts(l):
                self.gate_values[gate][l] = 'D'
        elif v == 1:
            self.gate_values[g][l] = '~D'
            for gate in self.getFanouts(l):
                self.gate_values[gate][l] = '~D'
        else:
            self.gate_values[g][l] = v
            for gate in self.getFanouts(l):
                self.gate_values[gate][l] = v


        #! set all inputs to ~c expect l
        for Input in self.getInputs(g):
            if Input == l:
                continue
            else:
                self.gate_values[g][Input] = int(not(self.c(g)))
                if not(Input in self.PIs):
                    self.gate_values[Input]['output'] = int(not(self.c(g)))
                if not(self.getFanouts(Input)):
                    print("No fanout!")
                else:
                    Fanouts = self.getFanouts(Input)
                    for fanout in Fanouts:
                        self.gate_values[fanout][Input] = int(not(self.c(g)))
        
        #! set current output to err   
        if self.i(g) == 1 and v == 'D':
            self.gate_values[g]['output'] = '~D'
        elif self.i(g) == 0 and v =='~D':
            self.gate_values[g]['output'] = '~D'
        else:
            self.gate_values[g]['output'] = 'D'
            
        return self.D_propagate(l=g,v=self.gate_values[g]['output'])
            
    def D_justify(self,l,v):
        #! NOT WORKING
        print(l)
        g = self.getOutput(l)

        if l in self.PIs:
            #! fanout ?
            self.gate_values[g][l] = v
            return self
        else:
            self.gate_values[l]['output'] = v
        
        c = self.c(l)
        i = self.i(l)
        print("print l= ",l,"print c= ",c,"print i= ",i)

        inval = v ^ i    #* v XOR i
        print("inval= ",inval)

        cbar = int(not(self.c(l)))
        print("cbar= ",cbar)

        if inval == int(not(self.c(l))):
            inputs = self.getInputs(l)
            for Input in inputs:
                return self.D_justify(l=Input,v=inval)
        else:
            print("DO SOMETHING?!?!!?")
            #! pick a random input of l and justify(input,inval) ??       
    
    def makeJFrontier(self):
        #! consider storing direction ?
        for k in self.gate_values.keys():
            if self.getType(k) == 'not':
                continue
            if self.gate_values[k]['output'] == 'x':
                #print(k,"will not be in J-frontier!")
                continue
            elif self.c(k) in self.getInputs(k):
                #print(k,"will not be in J-frontier!")
                continue
            elif self.gate_values[k]['output'] == self.cbarXORi(k):
                values = self.getValues()
                value = values[k]
                all_x = self.checkX(value)
                if all_x:
                    inputs = self.getInputs(k)
                    PIs = self.PIs
                    for Input in inputs:
                        if not(Input in PIs):
                            continue    
                        else:
                            self.J_frontier.append([k,self.gate_values[k]['output']])
                            #print(k,self.gate_values[k]['output'])
            #else:
                #print(k," will not be in J-frontier")
   
    def makeDFrontier(self):
        for k in self.gate_values.keys():
            if self.gate_values[k]['output'] == 'x':
                all_values = self.getValues()
                vals = all_values[k]
                for val in vals:
                    if val == 'D' or val == '~D':
                        self.D_frontier.append(k)

    def getValues(self):
        values = {}
        for k in self.gate_values.keys():
            inputs = self.getInputs(k)
            temp = []
            for Input in inputs:
                temp.append(self.getInputValue(k,Input))
            values[k] = temp
        return values

        
    def getOutput(self,Input):
        for k,v in self.gate_values.items():
            if Input in v:
                return k

    def checkX(self,values):
        bool_list = []
        for item in values:
            if item == 'x':
                bool_list.append(True)
            else:
                bool_list.append(False)
        return all(bool_list)


if __name__ == '__main__':

    ckt = circuit()
    ckt.makeCkt("t4_21.ckt")
 
    ckt.D_algo(l="3gat",v=1)
    #[print(k,v) for k,v in ckt.gate_values.items()]
    #prop = ckt.D_propagate(l="3gat",v=1)
    #print(prop)
    #print("Assignments from propagation: ")
   

    # ckt.makeJFrontier()
    # print("J frontier is: ", ckt.J_frontier)
    
    # l = ckt.J_frontier[0][0]
    # v = ckt.J_frontier[0][1]

    # ckt.D_justify(l,v)
    # [print(k,v) for k,v in ckt.gate_values.items()]
    
    #ckt.makeDFrontier()
    #print("D frontier is: ", ckt.D_frontier)
