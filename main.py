from tkinter import Tk, Text, Menu, filedialog, PanedWindow, Scrollbar,Button
import os
import sys

# Redirecting sys.stdout to a function that updates the Text widget
class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, message):
        self.text_space.insert("end", message)
        self.text_space.see("end")  # Auto-scroll to the end of the output
        self.text_space.update()  # Update the text widget

from Scanner import Lexer
from Parser import SyntaxParser
from Renderer import Renderer
from Opt import Optimizer
def callLexer():
    str = textBox.get('1.0', "end")
    Lexer(str,print=True)

def callParser():
    str = textBox.get('1.0', "end")
    SyntaxParser(str,print=True)

def callOptimizer():
    str = textBox.get('1.0', "end")
    Optimizer(str)
    
def callRenderer():
    str = textBox.get('1.0', "end")
    Renderer(str)

def openFile():
    filePath = filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser(r"文件路径")))
    txtFile = open(filePath)
    content = txtFile.read()
    textBox.delete(0.0, "end")
    textBox.insert("insert", content)

def clearTerminal():
    terminal_output.delete(0.0, "end")

def main():
    global terminal_output  # terminal_output a global variable
    tk = Tk()
    tk.title("KrystalRay's Interpreter")
    tk.geometry("800x600")

    paned_window = PanedWindow(tk, orient='vertical')
    paned_window.pack(fill='both', expand=True)

    global textBox
    textBox = Text(tk, height=15)
    paned_window.add(textBox)

    # 分一部分窗口给终端
    terminal_frame = PanedWindow(paned_window, orient='vertical')
    terminal_frame.pack(fill='both', expand=True)
    paned_window.add(terminal_frame)

    # 为终端建立一个输入空间
    terminal_output = Text(terminal_frame, wrap='word')
    terminal_frame.add(terminal_output)

    scrollbar = Scrollbar(terminal_frame, command=terminal_output.yview)
    scrollbar.pack(side='right', fill='y')
    terminal_output.config(yscrollcommand=scrollbar.set)

    sys.stdout = StdoutRedirector(terminal_output)

    menuBar = Menu(tk)
    menuBar.add_command(label="文件", command=openFile)

    menuOpt = Menu(menuBar, tearoff=0)
    menuOpt.add_command(label="词法分析", command=callLexer)
    menuOpt.add_command(label="语法分析", command=callParser)
    menuOpt.add_command(label="死代码消除", command=callOptimizer)
    menuOpt.add_command(label="语法制导翻译绘图", command=callRenderer)
    menuOpt.add_separator()
    menuBar.add_cascade(label="选择", menu=menuOpt)
    tk.config(menu=menuBar)

    clear_button = Button(terminal_frame, text="清空终端", command=clearTerminal)
    terminal_frame.add(clear_button)

    tk.mainloop()

if __name__ == '__main__':
    main()
