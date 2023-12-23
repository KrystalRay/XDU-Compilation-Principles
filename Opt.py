from Parser import SyntaxParser
from Scanner import Token,TokenType

class Optimizer:
    def __init__(self, string):
        self.crot = None
        self.corigin =  None
        self.csacle =   None
        self.ccolor =   None
        self.cthick =   None
        S = SyntaxParser(string)
        self.input = S.Parser(string)
        print("Before Optimizer:")
        self.print_IR()
        self.Optimizer()
        print("After Optimizer:")
        self.print_IR()
    def Optimizer(self)->list:
        for node in self.input:
            op = node.get_token()
            if op.TokenType == TokenType.ROT:
                if self.crot:
                    self.input.remove(self.crot)
                self.crot = node
            elif op.TokenType==TokenType.SCALE:
                if self.csacle:
                    self.input.remove(self.csacle)
                self.csacle = node
            elif op.TokenType==TokenType.ORIGIN:
                if self.corigin:
                    self.input.remove(self.corigin)
                self.corigin = node
            elif op.TokenType==TokenType.COLOR:
                if self.ccolor:
                    self.input.remove(self.ccolor)
                self.ccolor = node
            elif op.TokenType==TokenType.THICK:
                if self.cthick:
                    self.input.remove(self.cthick)
                self.cthick = node
            elif op.TokenType==TokenType.FOR:
                self.set_None()
            else:
                print("Optimizer Error")
        return self.input
    def set_None(self):
        self.crot = None
        self.corigin =  None
        self.csacle =   None
        self.ccolor =    None
        self.cthick =    None
        
    def print_IR(self) ->None:
        for node in self.input:
            node.print_tree()
            print(" ")
        print("---------------------------")
# str = "ORigin is (-30, 0); SCALE is (  312, 25); SCALE is (  52, 25); SCALE is (  15, 25); SCALE is (  20, 25); for t from 0 to 2*pi step 0.01 draw (sin(t), cos(t));  SCALE is (  30, 20); for t from -1 to 1 step 0.01 draw (2, t); FOR t from 0 to 1 step 0.01 draw (2+t, t);for t from -1 to 1 step 0.01 draw (2, t); FOR t from 0 to 1 step 0.01 draw (2+t, -t);for t from 0 to 2*pi step 0.01 draw (1+3*sin(t), 3*cos(t)); "

# O = opt(str)