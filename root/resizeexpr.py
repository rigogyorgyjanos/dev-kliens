import wndMgr

class Expr(object):
	def __init__(self, name=None, op=None, left=None, right=None):
		self.name = name
		self.op = op
		self.left = left
		self.right = right

	def __int__(self):
		return int(self.EvaluateLeaf(self.GetScreenSize()))

	def __float__(self):
		return float(self.EvaluateLeaf(self.GetScreenSize()))

	def GetScreenSize(self):
		return {
			"SCREEN_WIDTH": wndMgr.GetScreenWidth(),
			"SCREEN_HEIGHT": wndMgr.GetScreenHeight(),
		}

	def GetNewNumber(self, x, ctx):
		if isinstance(x, Expr):
			return x.EvaluateLeaf(ctx)
		return x

	# ----- leaf evaluation -----
	def EvaluateLeaf(self, ctx):
		if self.name:
			return ctx[self.name]

		if self.op == 'int':
			return int(self.GetNewNumber(self.left, ctx))

		if self.op == 'float':
			return float(self.GetNewNumber(self.left, ctx))

		l = self.GetNewNumber(self.left, ctx)
		r = self.GetNewNumber(self.right, ctx)

		if self.op == '+':
			return l + r
		if self.op == '-':
			return l - r
		if self.op == '*':
			return l * r
		if self.op == '/':
			return l / r

		raise ValueError("Unknown op %s" % self.op)

	# ----- operators -----
	def __add__(self, other):
		return Expr(op='+', left=self, right=other)

	def __sub__(self, other):
		return Expr(op='-', left=self, right=other)

	def __mul__(self, other):
		return Expr(op='*', left=self, right=other)

	def __div__(self, other):
		return Expr(op='/', left=self, right=other)

	def __radd__(self, other):
		return Expr(op='+', left=other, right=self)

	def __rsub__(self, other):
		return Expr(op='-', left=other, right=self)

	def __rmul__(self, other):
		return Expr(op='*', left=other, right=self)

	def __rdiv__(self, other):
		return Expr(op='/', left=other, right=self)