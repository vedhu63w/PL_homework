from SExp_class 		import dict_sym_atm, SExp
from MyError			import MyError

def cons(SExp_1, SExp_2):
	return SExp(exp_type=3, SE1=SExp_1, SE2=SExp_2)


def car(LSExp):
	if LSExp.type != 3:
		raise MyError("CAR of Atom is not permitted %s" % LSExp) 
	else:
		return LSExp.left


def cdr(LSExp):
	if LSExp.type != 3:
		raise MyError("CDR of Atom is not permitted %s" % LSExp) 
	else:
		return LSExp.right


def atom(LSExp):
	return SExp(exp_type=2, sym_atm="T") if LSExp.type != 3 \
				else SExp(exp_type=2, sym_atm="NIL")


def retLisp(boolval):
	return SExp(exp_type=2, sym_atm="T") if boolval \
			else SExp(exp_type=2, sym_atm="NIL")

# Currently just compares the atoms
def eq(SExp1, SExp2):	
	if SExp1.type == 1:
		if SExp2.type == 1:
			return retLisp(SExp1.int_val == SExp2.int_val)
		else:
			return SExp(exp_type=2, sym_atm="NIL")
	elif SExp1.type == 2:
		if SExp2.type == 2:
			return retLisp(SExp1.sym_atm == SExp2.sym_atm)
		else:
			return SExp(exp_type=2, sym_atm="NIL")
	else:
		return SExp(exp_type=2, sym_atm="NIL")


def EQLISP(SExp1, SExp2):	
	if SExp1.type == 1:
		if SExp2.type == 1:
			return retLisp(SExp1.int_val == SExp2.int_val)
		else:
			return SExp(exp_type=2, sym_atm="NIL")
	elif SExp1.type == 2:
		if SExp2.type == 2:
			return retLisp(SExp1.sym_atm == SExp2.sym_atm)
		else:
			return SExp(exp_type=2, sym_atm="NIL")
	else:
		raise MyError("Arguments for equal should be atomic and same type")


# This is for python T for True and NIL for False
def iseqbool(SExp1, SExp2):
	return True if eq(SExp1, SExp2).sym_atm == dict_sym_atm["T"] \
				else False	

# TODO: Raises error if atom not in list. Maybe want to change it later
def get_valAlist(LSExp, alist):
	list_pair = alist
	while(not iseqbool(list_pair, SExp(exp_type=2, sym_atm="NIL"))):
		if iseqbool(car(car(list_pair)), LSExp):
			return cdr(car(list_pair))
		list_pair = cdr(list_pair)
	raise MyError("Unbounded error %s" % LSExp.sym_atm.name)


def evcon(be, alist, dlist):
	if iseqbool(be, SExp(exp_type=2, sym_atm="NIL")):
		raise MyError("No condition correct")
	car_ev_be = evlist(car(be), alist, dlist)
	# leval, _, _ = lispeval(car(car(be)), alist, dlist)
	if not chk_numarg(car_ev_be, 2): raise MyError("Number of arguments for COND is not 2")
	if iseqbool(car(car_ev_be), SExp(exp_type=2, sym_atm="T")):
		# leval, _, _ = lispeval(car(cdr(be)), alist, dlist)
		# return leval
		return car(cdr(car_ev_be))
	else:
		return evcon(cdr(be), alist, dlist)


def addtodlist(dlist, functparbody):
	if not chk_numarg(functparbody, 3): raise MyError("Number of arguments for DEFUN should be 3")
	if iseqbool(atom(car(cdr(functparbody))), SExp(exp_type=2, sym_atm="T")): 
		raise MyError("Parameters for functions should not be a atom")
	dlist = cons(functparbody, dlist) 
	return dlist


def addtoAlist(plist, x, alist, fn):
	curr_ptr_p = plist
	curr_ptr_x = x
	new_alist = alist
	while (not iseqbool(curr_ptr_p, SExp(exp_type=2, sym_atm="NIL"))):
		new_alist = cons(cons(car(curr_ptr_p), car(curr_ptr_x)), new_alist)
		curr_ptr_x = cdr(curr_ptr_x)
		curr_ptr_p = cdr(curr_ptr_p)
	if not iseqbool(curr_ptr_x, SExp(exp_type=2, sym_atm="NIL")):
		raise MyError("Number of argument does not match for function %s"% fn)
	return new_alist


def get_val(fn_name, dlist):
	curr_ptr = dlist
	while(not iseqbool(curr_ptr, SExp(exp_type=2, sym_atm="NIL")) and not iseqbool(car(car(curr_ptr)), fn_name) ):
		curr_ptr = curr_ptr.right
	if (iseqbool(curr_ptr, SExp(exp_type=2, sym_atm="NIL"))):
		raise MyError("%s is not a function definition\n" % fn_name)
	return cdr(car(curr_ptr))


def chk_numarg(x, expected):
	curr_x = x
	while (not iseqbool(curr_x, SExp(exp_type=2, sym_atm="NIL")) ):
		curr_x = cdr(curr_x)
		expected-=1;
	return True if expected==0 else False


def lispapply(fn_name, x, alist, dlist):
	# fn_name should be an atom as its checked in lispeval
	if iseqbool(fn_name, SExp(exp_type=2, sym_atm="CAR")):
		if not chk_numarg(x, 1): 
			raise MyError("Number of argument for CAR not correct") 
		return car(car(x))
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="CDR")):
		if not chk_numarg(x, 1): 
			raise MyError("Number of argument for CDR not correct")
		return cdr(car(x))
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="EQ")):
		if not chk_numarg(x, 2): 
			raise MyError("Number of argument for EQ not correct")
		return EQLISP(car(x), car(cdr(x)))
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="ATOM")):
		if not chk_numarg(x, 1): 
			raise MyError("Number of argument for ATOM not correct")
		return atom(car(x))
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="CONS")):
		if not chk_numarg(x, 2): 
			raise MyError("Number of argument for CONS not correct")
		return cons(car(x), car(cdr(x)))
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="NULL")):
		if not chk_numarg(x, 1): 
			raise MyError("Number of argument for NULL not correct")
		return eq(car(x), SExp(exp_type=2, sym_atm="NIL"))
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="INT")):
		if not chk_numarg(x, 1): 
			raise MyError("Number of argument for INT not correct")
		return SExp(exp_type=2, sym_atm="T") if car(x).type == 1 \
			else SExp(exp_type=2, sym_atm="NIL")
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="PLUS")):
		if not chk_numarg(x, 2): 
			raise MyError("Number of argument for PLUS not correct")
		if car(x).type == 1 and car(cdr(x)).type == 1:
			return SExp(exp_type=1, int_val=car(x).int_val+car(cdr(x)).int_val)
		else: raise MyError("Not correct format for PLUS")
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="MINUS")):
		if not chk_numarg(x, 2): 
			raise MyError("Number of argument for MINUS not correct")
		if car(x).type == 1 and car(cdr(x)).type == 1:
			return SExp(exp_type=1, int_val=car(x).int_val-car(cdr(x)).int_val)
		else: raise MyError("Not correct format for MINUS")
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="TIMES")):
		if not chk_numarg(x, 2): 
			raise MyError("Number of argument for TIMES not correct")
		if car(x).type == 1 and car(cdr(x)).type == 1:
			return SExp(exp_type=1, int_val=car(x).int_val*car(cdr(x)).int_val)
		else: raise MyError("Not correct format for TIMES")
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="QUOTIENT")):
		if not chk_numarg(x, 2): 
			raise MyError("Number of argument for QUOTIENT not correct")
		if car(x).type == 1 and car(cdr(x)).type == 1:
			try:
				return SExp(exp_type=1, int_val=car(x).int_val/car(cdr(x)).int_val)
			except ZeroDivisionError:
				raise MyError("Zero cannot be in denomintor for QUOTIENT")
		else: raise MyError("Not correct format for QUOTIENT")
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="REMAINDER")):
		if not chk_numarg(x, 2): 
			raise MyError("Number of argument for REMAINDER not correct")
		if car(x).type == 1 and car(cdr(x)).type == 1:
			try:
				return SExp(exp_type=1, int_val=car(x).int_val%car(cdr(x)).int_val)
			except ZeroDivisionError:
				raise MyError("Zero cannot be in denomintor for REAMINDER")
		else: raise MyError("Not correct format for REMAINDER")
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="LESS")):
		if not chk_numarg(x, 2): 
			raise MyError("Number of argument for LESS not correct")
		if car(x).type == 1 and car(cdr(x)).type == 1:
			return retLisp(car(x).int_val < car(cdr(x)).int_val)
		else: raise MyError("Not correct format for LESS")
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="GREATER")):
		if not chk_numarg(x, 2): 
			raise MyError("Number of argument for GREATER not correct")
		if car(x).type == 1 and car(cdr(x)).type == 1:
			return retLisp(car(x).int_val > car(cdr(x)).int_val)
		else: raise MyError("Not correct format for GREATER")
	else:
		par_bdy = get_val(fn_name, dlist)
		leval, _, _ = lispeval(car(cdr(par_bdy)), addtoAlist(car(par_bdy), x, alist, fn_name), dlist) 
		return leval


def evlist(LSExp, alist, dlist):
	curr_ptr = LSExp
	while(not iseqbool(curr_ptr, SExp(exp_type=2, sym_atm="NIL"))):
		car_eval, _, _ = lispeval(car(LSExp), alist, dlist)
		return cons(car_eval, evlist(cdr(LSExp), alist, dlist))
	return SExp(exp_type=2, sym_atm="NIL")


def lispeval(LSExp, alist, dlist):
	if iseqbool(atom(LSExp), SExp(exp_type=2, sym_atm="T")):
		if LSExp.type == 1:
			return LSExp, 0, dlist
		elif iseqbool(LSExp, SExp(exp_type=2, sym_atm="T")) or iseqbool(LSExp, SExp(exp_type=2, sym_atm="NIL")):
			return LSExp, 0, dlist
		else:
			return get_valAlist(LSExp, alist), 0, dlist
	elif iseqbool(atom(car(LSExp)), SExp(exp_type=2, sym_atm="T")):
		if iseqbool(car(LSExp), SExp(exp_type=2, sym_atm="COND")):
			return evcon(cdr(LSExp), alist, dlist), 0, dlist
		elif iseqbool(car(LSExp), SExp(exp_type=2, sym_atm="DEFUN")):
			return None, 1, addtodlist(dlist, cdr(LSExp))
		# TODO: Quote parameter checking
		elif iseqbool(car(LSExp), SExp(exp_type=2, sym_atm="QUOTE")):
			return car(cdr(LSExp)), 0, dlist
		else:
			return lispapply(car(LSExp), evlist(cdr(LSExp), alist, dlist), alist, dlist), 0, dlist
	else:
		raise MyError("SExp should be atom or car of SExp should be atom")