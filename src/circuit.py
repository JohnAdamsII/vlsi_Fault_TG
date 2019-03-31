from operator import xor

class circuit:
    def __init__(self,name="",Type=None,PIs=[],POs=[],gates=[],output="x"):
        self.name = name
        self.Type = Type
        self.PIs = PIs
        self.POs = POs
        self.gates = gates
        self.output = output
    #Read only attributes set automatically based on Type, controlling value, inversion value, and c XOR i
    @property
    def c(self):
        if self.Type.casefold() == "AND".casefold() or self.Type.casefold() == "NAND".casefold():
            return 0
        elif self.Type.casefold() == "OR".casefold() or self.Type.casefold() == "NOR".casefold():
            return 1
        else: return None
    @property
    def i(self):
        if self.Type.casefold() == "NAND".casefold() or self.Type.casefold() == "NOR".casefold():
            return 1
        elif self.Type.casefold() == "AND".casefold() or self.Type.casefold() == "OR".casefold():
            return 0
        else: return None
    @property
    def cXORi(self):
        return None if self.c == None else xor(self.c,self.i)

    def getType(self):
        pass
        
                
if __name__ == '__main__':
    #pass

    ckt = circuit("1gat","AnD")
    print(ckt.name,ckt.Type,ckt.c,ckt.i,ckt.cXORi)
        