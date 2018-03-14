from MyError import MyError

dict_sym_atm = dict()


class SymbolicAtom:
	def __init__(self, name):
		if name[0].isupper(): 
			for curr_char in name[1:]:
				if curr_char.isupper() or curr_char.isdigit():
					continue
				else:
					raise MyError("Identifier not in correct format %s" % name) 
 		self.name = name;
	
	def __repr__(self):
		print "Symbolic atome %s" % self.name


# TODO: check the format of sym_atm
class SExp():
	# exp_type = 1: int 2: Symbolic atom 3: binary tree
	def __init__(self, exp_type, SE1=None, SE2=None, int_val=0, sym_atm=""):
		self.type = exp_type;
		if exp_type == 3:		
			self.left = SE1;
			self.right = SE2;
		elif exp_type == 1:
			self.int_val = int(int_val) ;
		elif exp_type == 2:
			self.sym_atm = dict_sym_atm.setdefault( sym_atm, SymbolicAtom(sym_atm));


	def __repr__(self):
		if self.type == 1:
			return ("An Integer with %d" % self.int_val)
		elif self.type == 2:
			return ("An Symbolic Atom %s" % self.sym_atm.name)
		elif self.type == 3:
			return ("Binary Tree")
		else:
			return "Should not happen"

