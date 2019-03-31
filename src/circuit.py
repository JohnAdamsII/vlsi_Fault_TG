from read_Netlist import read_Netlist

class circuit:

    gate_map = {}
    gate_values = {}

    def __init__(self,PIs=[],POs=[],gates=[],output="x"):
        self.PIs = PIs
        self.POs = POs
        self.gates = gates
        self.output = output

    def makeCkt(self,ckt_file):
        ckt = read_Netlist(ckt_file)  #use to read one circuits data

        self.gates = [x[0] for x in ckt.wires]
        types = [x[1] for x in ckt.wires]
        self.PIs = ckt.PIs
        self.POs = ckt.POs
     
        type_map,input_map,PI_value_map = ({} for i in range(3))
    
        for gates,ckt_type in zip(self.gates,types):
            type_map[gates] = ckt_type
            
        for gates,inputs in zip(self.gates,ckt.wires):
            input_map[gates] = inputs[2:]
    
        for k in input_map:
            if len(input_map[k]) == 2:
                input_map[k]= [[input_map[k][0],input_map[k][1]]]
            else:
                input_map[k] = [[input_map[k][0]]]
        
        for k in input_map:
            input_map[k].append(type_map[k])
            Type = type_map[k]
            getc = lambda x: 0 if x == 'and' or x == 'nand' else 1
            geti = lambda x: 0 if x == 'and' or x == 'or' else 1
            cXORi = lambda c,i: c ^ i
            cbarXORi = lambda c,i: int(not c ^ i)
            input_map[k].append(getc(Type))
            input_map[k].append( geti(Type) )
            input_map[k].append ( cXORi(getc(Type),geti(Type)) )
            input_map[k].append( cbarXORi(getc(Type),geti(Type)) )
            input_map[k].append('x')
        

        for k in input_map:
            self.gate_values[k] = { input_map[k][0][0] : 'x', input_map[k][0][1] : 'x'}
        
        self.gate_map = input_map
        
    def c(self,gate):
        return self.gate_map[gate][2]
    def cXORi(self,gate):
        return self.gate_map[gate][4]
    def cbarXORi(self,gate):
        return self.gate_map[gate][5]
    def getType(self,gate):
        return self.gate_map[gate][1]
    
    def getInputs(self,gate):
        if len(self.gate_map[gate][0]) == 2:
            return self.gate_map[gate][0]
        else:
            return self.gate_map[gate][0][0]
    
    def getInputValues(self,gate,Input):
            return self.gate_values[gate][Input]
   
    def setInputs(self,gate,value,set_all=True):
        if set_all:
            for inputs in self.getInputs(gate):
                if self.gate_values[gate][inputs] == 'x':
                    self.gate_values[gate][inputs] = value
    
    def assignOutput(self,gate):
            Inputs = self.getInputs(gate) # list of inputs
            c = self.c(gate) # c of gate
            values = []
            for Inputs in Inputs:
                values.append(self.getInputValues(gate,Inputs))
            if c in values:
                self.gate_map[gate][-1] = self.cXORi(gate)
            elif not(c in values) and not('x' in values):
                self.gate_map[gate][-1] = self.cbarXORi(gate)
            else: self.gate_map[gate][-1] = 'x'
    
    def propagatePIs(self):
        pass
    
    def setPIs(self):
        pass
    
    def D_algo(self):
        pass 

                


    
            #if self.c(gate) in self.getInputValues(gate,inputs):
                #self.gate_map[gate][-1] = "HEY!"

        
            #for inputs in self.getInputs(gate):
                #if k.c(gate) == 


        
                
if __name__ == '__main__':
    
    ckt = circuit()
    ckt.makeCkt("t4_21.ckt")
   
    for gate in ckt.gates:
        print(gate,ckt.getType(gate),ckt.getInputs(gate),ckt.c(gate))

    for k,v in ckt.gate_values.items():
        print(k,v)
        
    for gate in ckt.gates:
        ckt.setInputs(gate,0)

    for k,v in ckt.gate_values.items():
        print(k,v)
    
    for gate in ckt.gates:
        ckt.assignOutput(gate)
        
    for k,v in ckt.gate_map.items():
        print(k,v)
         