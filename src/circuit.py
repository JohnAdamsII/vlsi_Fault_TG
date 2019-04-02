from read_Netlist import read_Netlist

class circuit:

    gate_map = {}
    gate_values = {}
    fault_set = set()
    collapsed_fault_set = set()

    def __init__(self,PIs=[],POs=[],gates=[]):
        self.PIs = PIs
        self.POs = POs
        self.gates = gates

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
        
        for k in input_map:
            self.gate_values[k] = { input_map[k][0][0] : 'x', input_map[k][0][1] : 'x', 'output' : 'x'}
        
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
    
    def getInputValue(self,gate,Input):
            return self.gate_values[gate][Input]
    
    def getFanouts(self,Input):
        fan_outs = []
        for k,v in self.gate_values.items():
                if Input in v:
                    fan_outs.append(k)
        return fan_outs

    def setInput(self,gate,Input,value):
        fan_outs = self.getFanouts(Input)
        for fanouts in fan_outs:
            self.gate_values[fanouts][Input] = value
        self.assignOutput(gate)

    def assignOutput(self,gate):
            Inputs = self.getInputs(gate) # list of inputs
            c = self.c(gate) # c of gate
            values = []
            for Inputs in Inputs:
                values.append(self.getInputValue(gate,Inputs))
            if c in values:
                self.gate_values[gate]['output'] = self.cXORi(gate)
                self.propagate(gate,self.cXORi(gate))
            elif not(c in values) and not('x' in values):
                self.gate_values[gate]['output'] = self.cbarXORi(gate)
                self.propagate(gate,self.cbarXORi(gate))
            
    def propagate(self,gate,value):
        fan_outs = self.getFanouts(gate)
        for inputs in fan_outs:
            self.gate_values[inputs][gate] = value
            self.gate_values[inputs]['output'] = value
    
    def setPIs(self,PI_values):
        for index,PI in enumerate(self.PIs):
            for k,v in self.gate_values.items():
                if PI in v:
                    self.gate_values[k][PI] = PI_values[index]
                    self.assignOutput(k)
    
    def getFaultList(self):
        all_gates = self.gates + self.PIs
        for gates in all_gates:
            self.fault_set.add(str(gates)+"-s-a-1")
            self.fault_set.add(str(gates)+"-s-a-0")
        return self.fault_set
       
    def collapseFaults(self):
        pass

    def D_algo(self):
        pass 
              
if __name__ == '__main__':
    
    ckt = circuit()
    ckt.makeCkt("t4_21.ckt")

    ckt.setPIs([0,1,0,1,1])

    [print(k,v) for k,v in ckt.gate_values.items()]
   
    faults = ckt.getFaultList()
    [print(x) for x in faults]

    for k,v in ckt.gate_map.items():
        print(k,v)
        
         