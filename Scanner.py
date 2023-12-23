import math

class TokenType:
    '所有记号类型的定义'
    COMMENT1 = "//"
    COMMENT2 = "--"
    ORIGIN = "ORIGIN"
    SCALE = "SCALE"
    ROT = "ROT"
    IS = "IS"
    FOR = "FOR"
    FROM = "FROM"
    TO = "TO"
    STEP = "STEP"
    DRAW = "DRAW"
    THICK = "THICK"
    COLOR = "COLOR"

    T = "T"

    FUNC = "FUNCTION"
    CONST_ID = "CONST_ID"

    SEMICO = ';'
    L_BRACKET = '('
    R_BRACKET = ')'
    COMMA = ','

    PLUS = '+'  
    MINUS = '-'
    MUL = '*'
    DIV = '/'
    POWER = '**'

    NONTOKEN = "NON"
    ERRTOKEN = "ERR"

class Token:
    '所有记号'
    def __init__(self, TokenType="ERRTOKEN", lexeme="", value=0.0, FuncPtr=None,line_num=1.0):
        self.TokenType = TokenType
        self.lexeme = lexeme
        self.value = value
        self.FuncPtr = FuncPtr
        self.line_num=  line_num

    def display(self):
        print(str(self.TokenType).rjust(20), self.lexeme.rjust(20), str(self.value).rjust(20), str(self.FuncPtr).rjust(20),str(self.line_num).rjust(20))
    # 打印Token的信息，包含Token类型 当前词素 当前tokenvalue和函数指针
    def __str__(self):
        return str(self.TokenType)
    
    def getline_num(self):
        return self.line_num
        
    def set_linenum(self,num):
        self.line_num = num
        
TokenTypeDict = {
    "PI": Token(TokenType.CONST_ID, "PI", math.pi), 
    "E": Token(TokenType.CONST_ID, "E", math.e),      
    "T": Token(TokenType.T, "T"),

    "ORIGIN": Token(TokenType.ORIGIN, "ORIGIN"), 
    "SCALE": Token(TokenType.SCALE, "SCALE"), 
    "ROT": Token(TokenType.ROT, "ROT"), 
    "IS": Token(TokenType.IS, "IS"), 
    "FOR": Token(TokenType.FOR, "FOR"), 
    "FROM": Token(TokenType.FROM, "FROM"), 
    "TO": Token(TokenType.TO, "TO"), 
    "STEP": Token(TokenType.STEP, "STEP"), 
    "DRAW": Token(TokenType.DRAW, "DRAW"),
    "COLOR":Token(TokenType.COLOR, "COLOR"),
    "THICK":Token(TokenType.THICK, "THICK"),

    "SIN": Token(TokenType.FUNC, "SIN", 0.0,  math.sin),    
    "COS": Token(TokenType.FUNC, "COS", 0.0,  math.cos), 
    "TAN": Token(TokenType.FUNC, "TAN", 0.0,  math.tan), 
    "LN": Token(TokenType.FUNC, "LN", 0.0,  math.log), 
    "EXP": Token(TokenType.FUNC, "EXP", 0.0,  math.exp), 
    "SQRT": Token(TokenType.FUNC, "SQRT", 0.0,  math.sqrt)
}
# 符号表



class Lexer():
    def __init__(self,string,print=None):
        self.tokens = []       # 存储token列表 
        self.line_num = 1      # 跟踪行号
        self.i = 0
        self.Error = False
        self.ErrorSet = []
        self.print = print
        self.tokenize(string)
        self.ErrorHandle()
        self.isvalid()
    def extractAlphaToken(self, string):
        tmp_str = string[self.i]
        while self.i + 1 < len(string):
            char = string[self.i + 1]
            if char.isalnum():
                tmp_str += char
                self.i += 1
            else:
                # self.i += 1
                break
        return TokenTypeDict.get(tmp_str, Token(TokenType.ERRTOKEN, tmp_str))

    def extractNumberToken(self, string):
        tmp_num = string[self.i]
        while self.i + 1 < len(string):
            char = string[self.i + 1]
            if char.isdigit():
                tmp_num += char
                self.i += 1
            elif char == '.':
                tmp_num += char
                self.i += 1
                while self.i + 1 < len(string):
                    next_char = string[self.i + 1]
                    if next_char.isdigit():
                        tmp_num += next_char
                        self.i += 1
                    else:
                        break
                break
            else:
                break
        return Token(TokenType.CONST_ID, tmp_num, float(tmp_num))

    def extractSymbolToken(self, char, string):
        if char == ';':
            return Token(TokenType.SEMICO, ';')
        elif char == '(':
            return Token(TokenType.L_BRACKET, '(')
        elif char == ')':
            return Token(TokenType.R_BRACKET, ')')
        elif char == ',':
            return Token(TokenType.COMMA, ',')
        elif char == '+':
            return Token(TokenType.PLUS, '+')
        elif char == '-':
            if string[self.i+1] == '-':
                while string[self.i+1]!='\n':
                    self.i += 1
                self.line_num+=1
                # return Token(TokenType.COMMENT2, '--')
            else:
                return Token(TokenType.MINUS, '-')
        elif char == '*':
            if string[self.i+1] == '*':
                self.i+=1
                return Token(TokenType.POWER, '**')
            else: 
                return Token(TokenType.MUL, '*')
        elif char == '/':
            if string[self.i+1] == '/':
                while string[self.i+1]!='\n':
                    self.i += 1
                self.line_num+=1
                # return Token(TokenType.COMMENT1, '//')
            else:
                return  Token(TokenType.DIV, '/')
        else:
            return Token(TokenType.ERRTOKEN, char)
#表驱动型编码
    def tokenize(self, string):
        tokens = []
        self.i = 0
        string = string.upper()
        while self.i < len(string):
            char = string[self.i]

            if char == '\n':
                self.line_num += 1
                self.i += 1
                continue
            elif char in (' ', '\t', '\r'):
                self.i += 1
                continue
            elif char.isalpha():
                token = self.extractAlphaToken(string)
            elif char.isdigit():
                token = self.extractNumberToken(string)
            else:
                if self.i==len(string)-1:
                    token = self.extractSymbolToken(char,' ')
                else:
                    token = self.extractSymbolToken(char,string)
                    # if token.TokenType == TokenType.COMMENT1 or token.TokenType == TokenType.COMMENT2 or token.TokenType == TokenType.POWER:
                    #     self.i+=1
            if token:
                tokens.append(token)
                if token.TokenType == TokenType.ERRTOKEN:
                    self.Error = True
                    self.ErrorSet.append(token)
                    token.set_linenum(self.line_num)

            self.i += 1
        tokens.append(Token(TokenType.NONTOKEN))
        if self.print:
            self.TokensDisply(tokens)
        return tokens

    def TokensDisply(self,tokens):
        print("Tokentype".rjust(20), "InputStack".rjust(20), "TValue".rjust(20), "FuncPtr".rjust(20))
        for token in tokens:
                token.display()
        
    def ErrorHandle(self):
        if self.Error:
            print("-----------Lexical Error------------")
            print("Tokentype".rjust(20), "InputStack".rjust(20), "TValue".rjust(20), "FuncPtr".rjust(20),"Line_Num".rjust(20))
            for err in self.ErrorSet:
                err.display()
    def isvalid(self):
        if self.Error == False and self.print :
            print("-----------Lexical Accept------------")

# 要进行词法分析的字符串
input_string = "--cd LLVM_Pass \n \a hello world.\n SCALE IS (100,100) \n ORIGIN is (320,160)//this is a comment 8**8"
str1 = "rot is 0;color is (2,2,2);THick is 3;"
# 实例化 Lexer 对象
# lexer = Lexer(str1,True)
# print("FOR T FROM 0 TO 2*PI STEP PI/50 DRAW (cos(T), sin(T));")
# 调用 tokenize 方法进行词法分析
# result_tokens = lexer.tokenize(str1)

