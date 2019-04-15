from read_Netlist import read_Netlist
from sympy import to_cnf,symbols,sympify,Xor
import os, subprocess

dir_path = os.path.dirname(os.path.realpath(__file__)) #path to file
parent_dir = os.path.abspath(os.path.join(dir_path, os.pardir)) #path to parent dir of file


class circuit:

    gate_map = {}
    expr_map = {}
    fault_exp_map = {}
    gate_values = {}
    fault_list = []
    collapsed_fault_list = []

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
            type_map[gates] = ckt_type

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
        all_gates = self.gates + self.PIs
        fault_list = []
        
        for gate in all_gates:
            fault_list.extend( [str(gate)+'-0',str(gate)+'-1'] )
          
        self.fault_list = sorted(fault_list, key=lambda x: x[0][0])
        return self.fault_list

    def collapseFaults(self):
        fault_set = set()
        for gate in self.gates:
            eq = self.func_eq(gate)
            if eq:
                fault_set.add(eq[0])
                    
        for gate in self.gates:
            dom = self.dom(gate)
            if dom:
                fault_set.update((dom[1], dom[2]))

        self.collapsed_fault_list = sorted(fault_set, key=lambda x: x[0][0])
        return self.collapsed_fault_list

    def func_eq(self, gate):
        if self.getType(gate) == 'not':
            return None
        else:
            inputs = self.getInputs(gate)
            return (str(gate)+"-"+str(self.cXORi(gate)), inputs[0]+'-'+str(self.c(gate)), inputs[1]+'-'+str(self.c(gate)))

    def dom(self, gate):
        if self.getType(gate) == 'not':
            return None
        else:
            inputs = self.getInputs(gate)
            return (str(gate)+"-"+str(self.cbarXORi(gate)), inputs[0]+'-'+str(int(not(self.c(gate)))), inputs[1]+'-'+str(int(not(self.c(gate)))))

    def D_algo(self):
        pass
    
    def build_Expr_map(self):
        """ Needs to be tested with a ckt with a not gate """
        for gate in self.gates:
            if self.getType(gate) == 'not':

                in1 = self.getInputs(gate)[0]
                s1 = symbols(in1)
            
                str_repr = str(to_cnf( ~s1 ))
                
                self.expr_map[gate] = [to_cnf(~s1)]
                self.expr_map[gate].append(str_repr)

            if self.getType(gate) == 'nor':
                inputs = []
                for Input in self.getInputs(gate):
                    if Input in self.expr_map.keys():
                        inputs.append(self.expr_map[Input][0])
                    else:
                        inputs.append(symbols(Input))
                
                self.expr_map[gate] = [to_cnf(  ~(inputs[0] | inputs[1]), True)]
                str_repr = str(to_cnf(~(inputs[0] | inputs[1]), True))
                self.expr_map[gate].append(str_repr)

            if self.getType(gate) == 'nand':
                inputs = []
                for Input in self.getInputs(gate):
                    if Input in self.expr_map.keys():
                        inputs.append(self.expr_map[Input][0])
                    else:
                        inputs.append(symbols(Input))
                
                self.expr_map[gate] = [to_cnf(  ~(inputs[0] & inputs[1]), True)]
                str_repr = str(to_cnf(~(inputs[0] & inputs[1]), True))
                self.expr_map[gate].append(str_repr)
        
            if self.getType(gate) == 'and':
                inputs = []
                for Input in self.getInputs(gate):
                    if Input in self.expr_map.keys():
                        inputs.append(self.expr_map[Input][0])
                    else:
                        inputs.append(symbols(Input))
                
                self.expr_map[gate] = [to_cnf(  (inputs[0] & inputs[1]), True)]
                str_repr = str(to_cnf( (inputs[0] & inputs[1]),True))
                self.expr_map[gate].append(str_repr)

            if self.getType(gate) == 'or':
                inputs = []
                for Input in self.getInputs(gate):
                    if Input in self.expr_map.keys():
                        inputs.append(self.expr_map[Input][0])
                    else:
                        inputs.append(symbols(Input))
                
                self.expr_map[gate] = [to_cnf(  (inputs[0] | inputs[1]), True)]
                str_repr = str(to_cnf( (inputs[0] | inputs[1]),True))
                self.expr_map[gate].append(str_repr)

        
        return self.expr_map



    def get_faulty_Expr(self):
        
        """ Needs to be tested with a ckt with a not gate """
        for gate in self.gates:
            if gate in self.fault_exp_map.keys():
                    print("setting fault for ",gate,"stuck at ",0)
                    self.fault_exp_map[gate] = 0 #! this needs to change!!!
                    continue
            if self.getType(gate) == 'not':

                in1 = self.getInputs(gate)[0]
                s1 = symbols(in1)
                
                self.fault_exp_map[gate] = [(~s1)]
                self.fault_exp_map[gate].append(str_repr)

            if self.getType(gate) == 'nor':
                inputs = []
                for Input in self.getInputs(gate):
                    if Input in self.fault_exp_map.keys():
                        inputs.append(self.fault_exp_map[Input])
                    else:
                        inputs.append(symbols(Input))
                
                self.fault_exp_map[gate] = ~(inputs[0] | inputs[1])

            if self.getType(gate) == 'nand':
                inputs = []
                for Input in self.getInputs(gate):
                    if Input in self.fault_exp_map.keys():
                        inputs.append(self.fault_exp_map[Input][0])
                    else:
                        inputs.append(symbols(Input))
                
                self.fault_exp_map[gate] = ~(inputs[0] & inputs[1])
               
            if self.getType(gate) == 'and':
                inputs = []
                for Input in self.getInputs(gate):
                    if Input in self.fault_exp_map.keys():
                        inputs.append(self.fault_exp_map[Input])
                    else:
                        inputs.append(symbols(Input))
                
                self.fault_exp_map[gate] = (inputs[0] & inputs[1])
              
            if self.getType(gate) == 'or':
                inputs = []
                for Input in self.getInputs(gate):
                    if Input in self.fault_exp_map.keys():
                        inputs.append(self.fault_exp_map[Input])
                    else:
                        inputs.append(symbols(Input))
                
                self.fault_exp_map[gate] = (inputs[0] | inputs[1])

        return self.fault_exp_map[self.POs[0]] #! ONLY WORKS WITH ONE PO right now


    def get_ckt_expr_str(self):
        """ only works currently if ckt has only one PO """
        return self.expr_map[self.POs[0]][1]
    def get_expr(self):
        return self.expr_map[self.POs[0]][0]
    
    def get_clauses(self,gate,stuck_at_value):
        """ need to modify to handle different gate names in other circuits """
        self.fault_exp_map[gate]= stuck_at_value #set fault
        faulty_expr = ckt.get_faulty_Expr() #get fault expression
        print("faulty expression is: ",faulty_expr)
        self.fault_exp_map = {} #reset map
        ff_ckt = self.get_faulty_Expr() #get free faulty circuit
        print("fault free expression is: ",ff_ckt)
        
        xor_expr = Xor(ff_ckt,faulty_expr) #get xor expr
        xor_expr = to_cnf(xor_expr,simplify=True) #get xor expr in CNF
       
        clauses = str(xor_expr).split("&")

        for index,item in enumerate(clauses):
            clauses[index] = item.strip()
            clauses[index] = clauses[index].replace("(","")
            clauses[index] = clauses[index].replace(")","")
            clauses[index] = clauses[index].replace("~","-")
            clauses[index] = clauses[index].replace("|","")
            clauses[index] = clauses[index].replace("  "," ")
            clauses[index] = clauses[index].replace("gat","")
        return clauses

    def write_to_CNF_file(self,gate,stuck_at_value):
        """ need to modify to take in expression from get_XOR function """
        clauses = self.get_clauses(gate,stuck_at_value)

        num_Vars = len(self.PIs)
        num_Clasues = len(clauses)
     
        with open(os.path.join(parent_dir+'/bin/','cnf_file'), "w") as f:
            f.write("p cnf "+str(num_Vars)+" "+str(num_Clasues)+'\n')
            for clause in clauses:
                f.write(clause+" 0\n")
        
        self.runMiniSAT()

    def runMiniSAT(self):
        miniSAT_path = parent_dir + '/bin/minisat'
        cnf_path = parent_dir + '/bin/'
        runminiSAT = subprocess.call(miniSAT_path +" -verb=0 "+cnf_path+'/cnf_file'+" "+cnf_path+"out.txt", shell=True)

        self.getSAT()

   
    def get_xor_CNF_expr(self,gate,stuck_at_value):
        ff_ckt = self.get_expr()
        faulty_ckt = ff_ckt.subs(gate,stuck_at_value)
        final_expr = Xor(faulty_ckt,ff_ckt)
        final_expr = to_cnf(final_expr,simplify=True)
        return str(final_expr)

    def get_Faulty_ckt(self,gate,stuck_at_value):
        ff_ckt = self.get_expr()
        return ff_ckt.subs(gate,stuck_at_value)
    
        

    def getSAT(self):
        with open(parent_dir+'/bin/out.txt','r') as f:
            lines = f.read().splitlines()
        SAT = True if lines[0] == 'SAT' else False
        vector = lines[1][:-1].split()
        print(SAT,vector)

        final_vec = [0 if '-' in x else 1 for x in vector ]
        if SAT:
            print("input vector: ",final_vec," will detect fault!")
        else:
            print("Fault is undetectable! that suckkkkkkkkkks")


if __name__ == '__main__':

    ckt = circuit()
    ckt.makeCkt("t4_21.ckt")


    # fault_list = ckt.getFaultList()
    # #print(fault_list)
    # for fault in fault_list:
    #     myfault = fault.split('-')
    #     gate = myfault[0]
    #     stuck_at_value = myfault[1]
    #     print(gate,stuck_at_value)
    #     ckt.write_to_CNF_file(gate,stuck_at_value)
    
    ckt.write_to_CNF_file("7gat",1)
    #ckt.write_to_CNF_file("4gat",0)
    #ckt.makeCkt("t4_3.ckt")

    # expr_map = ckt.build_Expr_map()
    # [print(k,v) for k,v in expr_map.items()]

    #! try setting intermeidaite before!! eg non_cnf_map['3gat'] = 0
    # ckt.fault_exp_map['7gat']= 0 #set fault
    # faulty_expr = ckt.get_faulty_Expr() #get fault expression
    # ckt.fault_exp_map = {} #reset map
    # ff_ckt = ckt.get_faulty_Expr() #get free faulty circuit
    # xor_expr = Xor(ff_ckt,faulty_expr) #get xor expr
    # xor_expr = to_cnf(xor_expr,simplify=True) #get xor expr in CNF
    # print(xor_expr)



    #[print(k,v) for k,v in non_cnf_map.items()]
    #final_expr = non_cnf_map["9gat"][0]
    print("********************************")
    # expr1 = non_cnf_map['6gat'][0]
    # print(expr1)
    # expr2 = non_cnf_map['8gat'][0]
    # print(expr2)

    #dif_map = ckt.build_dif_Expr_map()
    #[print(k,v) for k,v in dif_map.items()]
  
    #final_expr = non_cnf_map['6gat'][0] | non_cnf_map['8gat'][0]
    #print(final_expr)
    #final_expr = non_cnf_map["9gat"][0]





    #print(final_expr, type(final_expr))
    #non_cnf_map['7gat'] = 0
    #target = non_cnf_map['8gat']
    #print(target)
    #print(target[0].subs('3gat',0))
    #[print(k,v) for k,v in non_cnf_map.items()]
    #new_expr = final_expr.subs('3gat',0)
    #print(new_expr)

    #! get the expr with inner wires for the expr map
    #! them compare and insert faults for inner wires by
    #! subbing in the innner wire and the fault value

    #[print(k,v) for k,v in ckt.gate_values.items()]
    #[print(k,v) for k,v in ckt.gate_map.items()]






    #ckt_expr = ckt.get_ckt_expr_str()
    #print(ckt_expr,type(ckt_expr))

    #output_expr = ckt.get_expr()
    #print(output_expr)

    #clauses = ckt.get_clauses()
    #print(clauses)

    #ckt.write_to_CNF_file("7gat",1)

    #fault_expr =ckt.get_xor_CNF_expr()

    #print(fault_expr,type(fault_expr[0]))

   

    #! WRITE DATA TO CNF_FILE
    #! PARSE OUTPUT FOR TEST VECTOR
    #! GET FAULT CIRCUIT EXPR
    #! XOR WITH CORRECT CIRCUIT
    

    #fault_list = ckt.getFaultList()
    #print(fault_list)
    # for fault in fault_list:
    #     myfault = fault.split('-')
    #     gate = myfault[0]
    #     stuck_at_value = myfault[1]
    #     print(gate,stuck_at_value)
    #     ckt.write_to_CNF_file(gate,stuck_at_value)
    #     print("********************************************************************\n")
    # #print(fault_list)
    #print(clauses)
    #print(expr_map)

    #ff_ckt = ckt.get_expr()
    #print(ff_ckt)
    #faulty_ckt = to_cnf(ff_ckt.subs("4gat",0),simplify=True)
    
    #print(faulty_ckt)

    #final_expr = Xor(faulty_ckt,ff_ckt)
    #print(final_expr)
    #final_expr = to_cnf(final_expr,simplify=True)
    #print(final_expr)
    #print(sympify(faulty_ckt))
    #print(to_cnf(faulty_ckt,simplify=True))


    #ff_ckt = (A & B) | C
    #print(ff_ckt)
    #faulty_ckt = ff_ckt.subs('A',0)
    #print(faulty_ckt)

    # print(sympify(faulty_expr))
    # print(to_cnf( Xor(faulty_expr,non_faulty_expr ),True ) )
    

    #ckt.setPIs([0,1,1,'x'])
    #[print(k,v) for k,v in ckt.gate_values.items()]

    # ckt.setPIs([1,1,1,1])
    # [print(k,v) for k,v in ckt.gate_values.items()]


    # fault_list = ckt.getFaultList()
    # print(fault_list)

    # collapsed_fault_list = ckt.collapseFaults()
    # print(collapsed_fault_list)
 
    #[print(k,v) for k,v in ckt.gate_values.items()]

    # for k,v in ckt.gate_map.items():
    # print(k,v)
