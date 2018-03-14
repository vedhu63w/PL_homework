from re 		import sub

from MyError 			import MyError
from Primitive_Func		import lispeval, cons
from SExp_class			import SExp


def gettype(str_1):
	if str_1 == "(":
		return 1;
	elif str_1 == ")":
		return 2;
	elif str_1 == ".":
		return 3;
	elif ((str_1[0] == "-" or str_1[0] == "+") and str_1[1:].isdigit()) or str_1.isdigit():
		return 4;
	elif str_1[0].isalpha():
		return 5;
	elif str_1 == " ":
		return 6;
	else: 
		return -1;


# Input a string
# outputs first token id, string after token, type of token
def ckNextToken(SExp_str):
	if not SExp_str: 
		raise MyError("Unexpected end of SExpression")
	# if the first item is parenthesis or dot or space
	if SExp_str[0] == "." or SExp_str[0] == "(" or SExp_str[0] == ")" or SExp_str[0] == " ":
		return SExp_str[1:], SExp_str[0], gettype(SExp_str[0])
	else:
		min_indx = 100000
		if SExp_str.find('.')!=-1:
			min_indx = min(min_indx, SExp_str.find('.'))
		if SExp_str.find('(')!=-1:
			min_indx = min(min_indx, SExp_str.find('('))
		if SExp_str.find(')')!=-1:
			min_indx = min(min_indx, SExp_str.find(')'))
		if SExp_str.find(' ')!=-1:
			min_indx = min(min_indx, SExp_str.find(' '))
		# print SExp_str
		return SExp_str[min_indx:], SExp_str[:min_indx], gettype(SExp_str[:min_indx])



def print_tree(Fin_SExp):
	if Fin_SExp.type==3:
		return "(" + print_tree(Fin_SExp.left) + "." \
						+ print_tree(Fin_SExp.right) + ")"
	elif Fin_SExp.type==2:
		return Fin_SExp.sym_atm.name
	elif Fin_SExp.type==1:
		return "%d" % Fin_SExp.int_val


# ltype 1: ( 2: ) 3: . 4: int 5: symatm 6: space
def input_lisp(SExp_str):
	SExp_str, tkn, l_type = ckNextToken(SExp_str)
	if l_type == 1:
		# adding for special () dont know how to handle otherwise
		temp_SExp_str, tkn, l_type = ckNextToken(SExp_str)
		if l_type == 2:
			return SExp(exp_type=2, sym_atm="NIL"), temp_SExp_str
		
		S1, SExp_str = input_lisp(SExp_str)
		SExp_str, tkn, l_type = ckNextToken(SExp_str)
		# Space automatically implies a list
		if l_type == 6 or l_type == 2:
			# list
			S2, SExp_str = input2(SExp_str, tkn, l_type)
			return cons(S1, S2), SExp_str
		elif l_type == 3:
			S2, SExp_str = input_lisp(SExp_str)
			SExp_str, tkn, l_type = ckNextToken(SExp_str)
			if l_type == 2:
				return cons(S1, S2), SExp_str
			else:
				raise MyError("error expected \")\" at %s" % tkn+SExp_str)
		else:
			raise MyError("error expected \".\" or \")\" or \" \" at %s" % tkn+SExp_str)
			
	# TODO: accepts 4., 4, ), etc
	if l_type == 4:
		# if its just a number it better end with $
		return SExp(exp_type=1, int_val=tkn), SExp_str
	# TODO: accepts 4., 4, ), etc
	if l_type == 5:
		# if its just a identifier it better end with $
		return SExp(exp_type=2, sym_atm=tkn), SExp_str
	if l_type == 2 or l_type == 3 or l_type == 6 or l_type == -1: 
		raise MyError("error expected Symbolic atom, integer or \"(\" at %s" % tkn+SExp_str)


def input2(SExp_str, tkn, l_type): 
	if l_type == 1:
		S1, SExp_str = input_lisp("(" + SExp_str)
		SExp_str, tkn, l_type = ckNextToken(SExp_str)
		S2, SExp_str = input2(SExp_str, tkn, l_type)
		return cons(S1, S2), SExp_str
	if l_type == 2: 					
		return SExp(exp_type=2, sym_atm="NIL"), SExp_str
 	elif l_type == 4:
 		tkn_old = tkn
		SExp_str, tkn, l_type = ckNextToken(SExp_str)
		S2, SExp_str = input2(SExp_str, tkn, l_type)
		return cons(SExp(exp_type=1, int_val=tkn_old), S2), SExp_str
 	elif l_type == 5:
 		tkn_old = tkn
		SExp_str, tkn, l_type = ckNextToken(SExp_str)
		S2, SExp_str = input2(SExp_str, tkn, l_type)
		return cons(SExp(exp_type=2, sym_atm=tkn_old), S2), SExp_str
	elif l_type == 6:
		SExp_str, tkn, l_type = ckNextToken(SExp_str)
		return input2(SExp_str, tkn, l_type)
	else:
		raise MyError("error did not expect \".\" at %s" % tkn+SExp_str)


def remove_space(SExp_str):
	# remove multiple space to single space
	flt_SExp_str = sub('\s+', ' ', SExp_str).strip()
	# removing space around .
	flt_SExp_str = sub('\s+\.', '.', flt_SExp_str).strip()
	flt_SExp_str = sub('\.\s+', '.', flt_SExp_str).strip()
	# removing space before closing paranthesis
	flt_SExp_str = sub('\s+\)', ')', flt_SExp_str).strip()
	# removing space after opening paranthesis
	flt_SExp_str = sub('\(\s+', '(', flt_SExp_str).strip()
	# strip removes trailing and preciding spaces as well
	return flt_SExp_str


def initiate_atoms():
	SExp(exp_type=2, sym_atm="T")
	SExp(exp_type=2, sym_atm="NIL")
	SExp(exp_type=2, sym_atm="CONS")
	SExp(exp_type=2, sym_atm="CAR")
	SExp(exp_type=2, sym_atm="CDR")
	SExp(exp_type=2, sym_atm="COND")


def main():
	# raw_input(SExp_str)
	# SExp_str = "  (  2   3   4  )  "
	# SExp_str = "((2.4) (3.5))"
	# SExp_str = "((ASD3   .   324) (2   .   L2))"
	# SExp_str = "((2.4)  .  (3.5))"
	# SExp_str = "(2.(3.4))"
	# SExp_str = "( 3 (3.5)) "
	# Full_SExp_str = "(AB.(BC.AB))$( 3 (3.5))$$"
	# SExp_str = "(s)"
	# SExp_str = "((()))"
	# SExp_str = "(ASF2.2)"

	# just making sure nothing is after $$
	# Full_SExp_str = Full_SExp_str[:Full_SExp_str.find("$$")]
	# list_SExp_str = Full_SExp_str.split("$")
	# EXPECTS $ AS LAST CHARACTER IN A LINE
	
	flag=True
	alist = SExp(exp_type=2, sym_atm="NIL")
	dlist = SExp(exp_type=2, sym_atm="NIL")
	while flag:
		SExp_str = ""
		line = raw_input()
		SExp_str = SExp_str + line.split('$')[0]		
		while(line.find("$")==-1):
			line = raw_input()
			SExp_str = SExp_str + line.split('$')[0]
		
		if line.find("$$")!=-1:
			flag = False
		# elif dollar_str != "$":
		# 	print "Expected SExp in line and then $ in new line- alternating between SExpression and $"
		SExp_str = remove_space(SExp_str)
		try: 
			Fin_SExp, rem_SExp_str = input_lisp(SExp_str)
			if rem_SExp_str: 
				raise MyError("error expected input to be finished but got %s" % rem_SExp_str)
			print "Dot Notation: %s " % print_tree(Fin_SExp)
			Eval_SExp, state, dlist = lispeval(Fin_SExp, alist, dlist)
			if state:
				print "State Changed and dlist looks: %s" % print_tree(dlist)
			else:
				print "Evaluation: %s" % print_tree(Eval_SExp)
			# import pdb
			# pdb.set_trace()
		except MyError as e: 
			print "Error in %s: %s" % (SExp_str, e.err_msg)

	# print Fin_SExp.left.int_val
	# print Fin_SExp.left.left.sym_atm.name		
	# SExp_str = "( 3.   4    )    "


if __name__ == "__main__":
	main()