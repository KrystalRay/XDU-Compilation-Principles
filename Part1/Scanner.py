from enum import Enum 
import math


class TokenType(Enum):
    '所有符号类型的基类'

    ORIGIN = "ORIGIN"
    SCALE = "SCALE"
    ROT = "ROT"
    IS = "IS"
    FOR = "FOR"
    FROM = "FROM"
    TO = "TO"
    STEP = "STEP"
    DRAW = "DRAW"

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

class Token():
    def __init__(self, Token_Type, lexeme, value=0.0, FuncPtr = None):
        self.Token_Type = Token_Type;
        self.lexeme = lexeme;
        self.value = value;
        self.FuncPtr = FuncPtr;
    def display(self):
        print(str(self.Token_Type).rjust(20),self.lexeme.rjust(20),str(self.value).rjust(20),str(self.FuncPtr).rjust(20))
    #打印Token的信息，包含Token类型 当前词素 当前tokenvalue和函数指针

TokenTypeDict = dict(
    PI = Token(TokenType.CONST_ID, "PI", math.pi), 
    E = Token(TokenType.CONST_ID, "E", math.e),      
    T = Token(TokenType.T, "T"),

    ORIGIN = Token(TokenType.ORIGIN, "ORIGIN"), 
    SCALE = Token(TokenType.SCALE, "SCALE"), 
    ROT = Token(TokenType.ROT, "ROT"), 
    IS = Token(TokenType.IS, "IS"), 
    FOR = Token(TokenType.FOR, "FOR"), 
    FROM = Token(TokenType.FROM, "FROM"), 
    TO = Token(TokenType.TO, "TO"), 
    STEP = Token(TokenType.STEP, "STEP"), 
    DRAW = Token(TokenType.DRAW, "DRAW"),

    SIN = Token(TokenType.FUNC, "SIN", 0.0,  math.sin),    
    COS = Token(TokenType.FUNC, "COS", 0.0,  math.cos), 
    TAN = Token(TokenType.FUNC, "TAN", 0.0,  math.tan), 
    LN = Token(TokenType.FUNC, "LN", 0.0,  math.log), 
    EXP = Token(TokenType.FUNC, "EXP", 0.0,  math.exp), 
    SQRT = Token(TokenType.FUNC, "SQRT", 0.0,  math.sqrt)
    );
#符号表



class Lexer:
    def __init__(self):
        self.tokens = []       # 存储token列表 
        self.line_num = 1      # 跟踪行号

    def extractAlphaToken(self, string, i):
        tmp_str = string[i]
        while i + 1 < len(string):
            char = string[i + 1]
            if char.isalnum():
                tmp_str += char
                i += 1
            else:
                break
        return TokenTypeDict.get(tmp_str, Token(TokenType.ERRTOKEN, tmp_str))

    def extractNumberToken(self, string, i):
        tmp_num = string[i]
        while i + 1 < len(string):
            char = string[i + 1]
            if char.isdigit():
                tmp_num += char
                i += 1
            elif char == '.':
                tmp_num += char
                i += 1
                while i + 1 < len(string):
                    next_char = string[i + 1]
                    if next_char.isdigit():
                        tmp_num += next_char
                        i += 1
                    else:
                        break
                break
            else:
                break
        return Token(TokenType.CONST_ID, tmp_num, float(tmp_num))

    def extractSymbolToken(self, char):
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
            return Token(TokenType.MINUS, '-')
        elif char == '*':
            return Token(TokenType.POWER, '**')
        elif char == '/':
            return Token(TokenType.DIV, '/')
        else:
            return Token(TokenType.ERRTOKEN, char)

    def tokenize(self, string, show=False):
        tokens = []
        i = 0

        while i < len(string):
            char = string[i]

            if char == '\n':
                self.line_num += 1
                i += 1
                continue
            elif char in (' ', '\t', '\r'):
                i += 1
                continue
            elif char.isalpha():
                token = self.extractAlphaToken(string, i)
            elif char.isdigit():
                token = self.extractNumberToken(string, i)
            else:
                token = self.extractSymbolToken(char)

            if token:
                tokens.append(token)

            i += 1

        if show:
            self.showTokens(tokens)
        return tokens

    def showTokens(self,tokens):
        print("Tokentype".rjust(20), "InputStack".rjust(20), "TValue".rjust(20), "FuncPtr".rjust(20))
        for token in tokens:
                token.display()
        


# 实例化 Lexer 对象
lexer = Lexer()

# 要进行词法分析的字符串
input_string = "--cd LLVM_Pass \n \a hello world.\n SCALE IS (100,100) \n ORIGIN is (320,160)"

# 调用 tokenize 方法进行词法分析
result_tokens = lexer.tokenize(input_string, True)

