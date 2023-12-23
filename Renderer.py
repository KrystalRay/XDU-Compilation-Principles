from ExpNode import *
from Parser import SyntaxParser
from Scanner import Lexer
from Opt import Optimizer
import matplotlib.pyplot as plt 
import math

class Renderer:
	def __init__(self, string):
		self.orx = 0.0
		self.ory = 0.0
		self.scx = 1.0
		self.scy = 1.0#默认比例为1比1
		self.ang = 0.0
		self.color = (0.0,0.0,0.0) #默认为黑色
		self.thickness = 1.0
		S = SyntaxParser(string)
		input = S.Parser(string)
		
		self.semantics(input)
		self.showPic()

	# 语义分析
	def semantics(self, input):
		for statement in input:
			op = statement.get_token()
			if op.TokenType == TokenType.ROT:
				self.ang = statement.right.get_value()
			elif op.TokenType==TokenType.SCALE:
				self.scx, self.scy = statement.right.get_value()
				#print("scalex:",self.scx)
				#print("scaley:",self.scy)
			elif op.TokenType==TokenType.ORIGIN:
				self.orx, self.ory = statement.right.get_value()
				#print(self.orx) 
				#print(self.ory) 
			elif op.TokenType==TokenType.FOR:
				T_start, T_end , T_step = statement.left.get_value()
				#print("T_start, T_end , T_step:",T_start, T_end , T_step)
				Point_x, Point_y = statement.right.get_value()
				#print("Point_x, Point_y:",Point_x, Point_y)
				self.render(T_start, T_end, T_step, Point_x, Point_y)
			elif op.TokenType==TokenType.COLOR:
				color = statement.right.get_value()
				# for i in color:
				# 	i = i//255
				self.color = color
				# print("color:",self.color)
			elif op.TokenType==TokenType.THICK:
				self.thickness = statement.right.get_value()
				#print("thickness:",self.thickness)
			else:
				print("analyse Error")
	#渲染器
	def render(self, T_start, T_end, T_step, Point_x, Point_y):
		T_value = T_start
		Points = dict(X=[], Y=[]) 
		while T_value<=T_end:
			ExpNode.T_value = T_value
			
			x= Point_x.get_value()
			y= Point_y.get_value()
			# print("(%f, %f)" % (x, y))
			# 比例变换
			x, y = x*self.scx, y*self.scy
			# 旋转变换
			x, y = x*math.cos(self.ang) + y*math.sin(self.ang), y*math.cos(self.ang) - x*math.sin(self.ang)
			# 平移变换
			x, y = x+self.orx, y+self.ory
			Points['X'].append(x)
			Points['Y'].append(y)
			T_value += T_step
		plt.plot(Points['X'], Points['Y'],linestyle = '-',linewidth = self.thickness, color = self.color)
		
	
	def showPic(self):
		plt.xlim(xmax=1000, xmin=-1000)
		plt.ylim(ymax=1000, ymin=-1000)
		plt.show()
		

# # R = Renderer("rot is 6.0;")
str = "ORigin is (-30, 0); SCALE is (  20, 25); for t from 0 to 2*pi step 0.01 draw (sin(t), cos(t));"

# R = Renderer(str)