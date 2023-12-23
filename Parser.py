
from Scanner import *
import matplotlib.pyplot as plt 
from ExpNode import *


class SyntaxParser():
    def __init__(self,string,print=False):
        self.token_iter = None
        self.CurrentToken = Token("ERRTOKEN", "", 0.0, None)  # 使用给出的Token类初始化
        self.show_process = False
        self.print = print
        self.Error = False
        self.Parser(string)
        self.isvalid()
    def fetch_token(self) -> Token:
        try:
            self.CurrentToken = next(self.token_iter)
            # print(self.CurrentToken)
            return self.CurrentToken
        except StopIteration:
            return None

    def match_token(self, token_type, show=None) -> Token:
        if show:
            self.CurrentToken.display()  # 使用提供的Token类的display方法
        if self.CurrentToken.TokenType == token_type:
            self.fetch_token()
            return True
        else:
            print("Expected ", token_type, "received ", self.CurrentToken.TokenType)
            print("Error!")
            self.error = True
            return False

    def printprocess(self, op, string) -> None:
        if not self.show_process:
            return
        if op == 0:
            print("Enter %s" % string)
        else:
            print("Exit %s" % string)

## Expression -> Term -> Factor
## PLUS OR MINUS
    def Expression(self) -> ExpNode:
        self.printprocess(0, "Expression")
        left = self.Term()
        root = None
        while self.CurrentToken.TokenType==TokenType.PLUS or self.CurrentToken.TokenType==TokenType.MINUS:
            root = ExpNode(self.CurrentToken)
            self.match_token(self.CurrentToken.TokenType)
            right = self.Term()
            root.add_child(left)
            root.add_child(right)
            left = root
        self.printprocess(1, "Expression")
        return left
    
## MUL OR DIV
    def Term(self) -> ExpNode:
        self.printprocess(0, "Term")
        left = self.Factor()
        # root = None
        while self.CurrentToken.TokenType==TokenType.MUL or self.CurrentToken.TokenType==TokenType.DIV:
            root = ExpNode(self.CurrentToken)
            self.match_token(self.CurrentToken.TokenType)
            right = self.Factor()
            root.add_child(left)
            root.add_child(right)
            left = root
        self.printprocess(1, "Term")
        return left
## 
    def Factor(self) -> ExpNode:
        self.printprocess(0, "Factor")
        if self.CurrentToken.TokenType==TokenType.PLUS or self.CurrentToken.TokenType==TokenType.MINUS:
            root = ExpNode(self.CurrentToken)
            self.match_token(self.CurrentToken.TokenType)
            child = self.Factor()	
            root.add_child(child)
            self.printprocess(1, "Factor")
            return root
        
        ##如果不是+或者- 那么就是乘方运算
        else:
            self.printprocess(1, "Factor")
            return self.Component()		
## 乘方运算
    def Component(self) -> ExpNode:
        self.printprocess(0, "Component")
        left = self.Atom()
        if self.CurrentToken.TokenType==TokenType.POWER:
            root = ExpNode(self.CurrentToken)
            self.match_token(self.CurrentToken.TokenType)
            right = self.Component()

            root.add_child(left)
            root.add_child(right)
            self.printprocess(1, "Component")
            return root
        else:
            self.printprocess(1, "Component")
            return left
        
    def Atom(self) -> ExpNode:
        self.printprocess(0, "Atom")
        ##如果是保留字或者终结符
        if self.CurrentToken.TokenType==TokenType.CONST_ID or self.CurrentToken.TokenType==TokenType.T:
            root = ExpNode(self.CurrentToken)
            self.match_token(self.CurrentToken.TokenType)
            self.printprocess(1, "Atom")
            return root
        
        ##如果是函数
        elif self.CurrentToken.TokenType==TokenType.FUNC:
            root = ExpNode(self.CurrentToken)
            self.match_token(self.CurrentToken.TokenType)
            self.match_token(TokenType.L_BRACKET)
            son = self.Expression()
            self.match_token(TokenType.R_BRACKET)
            root.add_child(son)
            self.printprocess(1, "Atom")
            return root
        
        ##如果是括号匹配
        elif self.CurrentToken.TokenType==TokenType.L_BRACKET:
            self.match_token(TokenType.L_BRACKET)
            root = self.Expression()
            self.match_token(TokenType.R_BRACKET)
            self.printprocess(1, "Atom")
            return root
        else:
            print("Atom Error!")
            self.error = True

    def OriginStatement(self) -> ExpNode:
        self.printprocess(0, "OriginStatement")
        root = ExpNode(self.CurrentToken)
        self.match_token(TokenType.ORIGIN)
        root.add_child(ExpNode(self.CurrentToken))
        self.match_token(TokenType.IS)
        self.match_token(TokenType.L_BRACKET)
        origin_x = self.Expression().get_value()
        self.match_token(TokenType.COMMA)
        origin_y = self.Expression().get_value()
        self.match_token(TokenType.R_BRACKET)
        Otuple = [origin_x,origin_y]
        root.add_child(ExpNode(Token(TokenType.CONST_ID, str(Otuple), Otuple)))
        self.printprocess(1, "OriginStatement")
        return root
    
    def	ScaleStatement(self) ->ExpNode:
        self.printprocess(0, "ScaleStatement")
        root = ExpNode(self.CurrentToken)
        self.match_token(TokenType.SCALE)
        root.add_child(ExpNode(self.CurrentToken))
        self.match_token(TokenType.IS)
        self.match_token(TokenType.L_BRACKET)
        scale_x = self.Expression().get_value()
        self.match_token(TokenType.COMMA)
        scale_y = self.Expression().get_value()
        # print(scale_x)
        # print(scale_y)
        Stuple = [scale_x,scale_y]
        self.match_token(TokenType.R_BRACKET)
        root.add_child(ExpNode(Token(TokenType.CONST_ID, str(Stuple), Stuple)))
        self.printprocess(1, "ScaleStatement")
        return root
    
    def	RotStatement(self) -> ExpNode:
        self.printprocess(0, "RotStatement")
        root = ExpNode(self.CurrentToken)
        self.match_token(TokenType.ROT)
        root.add_child(ExpNode(self.CurrentToken))
        self.match_token(TokenType.IS)
        # root.add_child(ExpNode(self.CurrentToken))
        node = self.Expression()
        self.rot_angle = node.get_value()
        root.add_child(node)
        self.printprocess(1, "RotStatement")
        return root

    def	ForStatement(self) ->ExpNode:
        self.printprocess(0, "ForStatement")
        root = ExpNode(self.CurrentToken)
        self.match_token(TokenType.FOR)
        self.match_token(TokenType.T)
        # root.add_child(self.CurrentToken)
        self.match_token(TokenType.FROM)
        start = self.Expression().get_value()
        self.match_token(TokenType.TO)
        end = self.Expression().get_value()
        self.match_token(TokenType.STEP)
        step = self.Expression().get_value()
        Ttuple = [start,end,step]
        root.add_child(ExpNode(Token(TokenType.CONST_ID, str(Ttuple), Ttuple)))
        self.match_token(TokenType.DRAW)
        self.match_token(TokenType.L_BRACKET)
        ##注意这里的getvalue
        
        point_x = self.Expression()
        self.match_token(TokenType.COMMA)
        point_y = self.Expression()
        self.match_token(TokenType.R_BRACKET)
        Ptuple = [point_x,point_y]
        root.add_child(ExpNode(Token(TokenType.CONST_ID, str(Ptuple), Ptuple)))
        self.printprocess(1, "ForStatement")
        return root

    def ThicknessStatement(self) ->ExpNode:
        self.printprocess(0, "ThicknessStatement")
        root = ExpNode(self.CurrentToken)
        self.match_token(TokenType.THICK);
        root.add_child(ExpNode(self.CurrentToken))
        self.match_token(TokenType.IS)
        Thickness=self.Expression().get_value();
        root.add_child(ExpNode(Token(TokenType.CONST_ID, str(Thickness), float(Thickness))))
        self.printprocess(1, "ThicknessStatement")
        return root

    def ColorStatement(self) ->ExpNode:
        self.printprocess(0, "ColorStatement")
        root = ExpNode(self.CurrentToken)
        self.match_token(TokenType.COLOR)
        
        root.add_child(ExpNode(self.CurrentToken))
        self.match_token(TokenType.IS)
        self.match_token(TokenType.L_BRACKET)
        R = float(self.Expression().get_value())
        self.match_token(TokenType.COMMA)
        G = float(self.Expression().get_value())
        self.match_token(TokenType.COMMA)
        B = float(self.Expression().get_value())
        self.match_token(TokenType.R_BRACKET)
        R=R/255.0
        G=G/255.0
        B=B/255.0
        colorset = [R,G,B]
        # for i in colorset:
        #     print(i)
        
        root.add_child(ExpNode(Token(TokenType.CONST_ID, str(colorset), colorset)))
        self.printprocess(1, "ColorStatement")
        return root
    

    # Statement -> OriginStatement | ScaleStatement | RotStatement | ForStatement
    def Statement(self) -> ExpNode:
        self.printprocess(0, "Statement")
        
        if self.CurrentToken.TokenType==TokenType.ORIGIN:
            root = self.OriginStatement()
        elif self.CurrentToken.TokenType==TokenType.SCALE:
            root = self.ScaleStatement()
        elif self.CurrentToken.TokenType==TokenType.ROT:
            root = self.RotStatement()
        elif self.CurrentToken.TokenType==TokenType.FOR:
            root = self.ForStatement()
        elif self.CurrentToken.TokenType==TokenType.COLOR:
            root = self.ColorStatement()
        elif self.CurrentToken.TokenType==TokenType.THICK:
            root = self.ThicknessStatement()     
        else:
            print(self.CurrentToken.TokenType)
            print("Statement Error!")
            self.error = True
            return None
        self.printprocess(0, "Statement")
        return root


    
    def Program(self) -> list:
        self.printprocess(0, "Program")
        root = None
        OutPut = []
        while self.CurrentToken.TokenType != TokenType.NONTOKEN:
            # if self.CurrentToken.TokenType == TokenType.SEMICO:
            
            
            root = self.Statement()
            matched = self.match_token(TokenType.SEMICO)
            if self.print:
                root.print_tree()
                print(" ")

            OutPut.append(root)
            root = None;

            if not matched:
                print("Program Error")
                self.error = True
                break
            # for i in OutPut:
            #     print(i)
        self.printprocess(1, "Program")
        return OutPut

    def Parser(self, string, show=False) ->list:
        # 调用词法分析器 得到记号表
        L = Lexer(string)
        tokenList = L.tokenize(string)
        self.token_iter = iter(tokenList)
        self.fetch_token()
        return self.Program()

    def isvalid(self):
        if self.Error == False and self.print:
            print("-----------Synatax Accept------------")
        



def test():
    str1 = "ORIGIN is (-30, 0); SCALE is (  20, 25); for t from 0 to 2*pi step 0.01 draw (sin(t), cos(t));  SCALE is (  30, 20); for t from -1 to 1 step 0.01 draw (2, t); FOR t from 0 to 1 step 0.01 draw (2+t, t);for t from -1 to 1 step 0.01 draw (2, t); FOR t from 0 to 1 step 0.01 draw (2+t, -t);for t from 0 to 2*pi step 0.01 draw (1+3*sin(t), 3*cos(t)); "
    str1 = "rot is 0;origin is (50,400);scale is (2, 1);for T from 0 to 300 step 1 draw (t,0);for T from 0 to 300 step 1 draw (0,-t);for T from 0 to 300 step 1 draw (t,-t);scale is (2,0.1);for T from 0 to 55 step 1 draw (t,-(t*t));scale is (10,5);for T from 0 to 60 step 1 draw (t, -sqrt(t));scale is (20,0.1);for T from 0 to 8 step 0.1 draw (t, -exp(t));scale is (2, 20);"
    ##str1 = "ORigin is (-30, 0); SCALE is (  20, 25); for t from 0 to 2*pi step 0.01 draw (sin(t), cos(t));  SCALE is (  30, 20); for t from -1 to 1 step 0.01 draw (2, t); FOR t from 0 to 1 step 0.01 draw (2+t, t);for t from -1 to 1 step 0.01 draw (2, t); FOR t from 0 to 1 step 0.01 draw (2+t, -t);for t from 0 to 2*pi step 0.01 draw (1+3*sin(t), 3*cos(t)); "
    str1 = "rot is 0;color is (2,2,2);for t from 0 to 2*pi step pi/50 draw (cos(t),sin(t));"
    str1 = "color is (2,2,2);thick is 3.0;ORigin is (-30, 0); SCALE is (  20, 25); for t from 0 to 2*pi step 0.01 draw (sin(t), cos(t));  SCALE is (  30, 20); for t from -1 to 1 step 0.01 draw (2, t); FOR t from 0 to 1 step 0.01 draw (2+t, t);for t from -1 to 1 step 0.01 draw (2, t); FOR t from 0 to 1 step 0.01 draw (2+t, -t);for t from 0 to 2*pi step 0.01 draw (1+3*sin(t), 3*cos(t)); "
    S=SyntaxParser(str1)
    # S.Parser(str1)


# test()
