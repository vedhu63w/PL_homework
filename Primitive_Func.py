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
# TODO for trees
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
		# print ("TODO on trees")
		return SExp(exp_type=2, sym_atm="NIL")

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
	leval, _, _ = lispeval(car(car(be)), alist, dlist)
	if iseqbool(leval, SExp(exp_type=2, sym_atm="T")):
		leval, _, _ = lispeval(car(cdr(car(be))), alist, dlist)
		return leval
	else:
		return evcon(cdr(be), alist, dlist)


def addtodlist(dlist, functparbody):
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
		raise MyError("Number of argument does not match for %s", fn)
	return new_alist


def get_val(fn_name, dlist):
	curr_ptr = dlist
	while(not iseqbool(curr_ptr, SExp(exp_type=2, sym_atm="NIL")) and not iseqbool(car(car(curr_ptr)), fn_name) ):
		curr_ptr = curr_ptr.right
	if (iseqbool(curr_ptr, SExp(exp_type=2, sym_atm="NIL"))):
		raise MyError("%s is not a function definition\n" % fn_name)
	return cdr(car(curr_ptr))


def lispapply(fn_name, x, alist, dlist):
	# fn_name should be an atom as its checked in lispeval
	if iseqbool(fn_name, SExp(exp_type=2, sym_atm="CAR")):
		return car(car(x))
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="CDR")):
		return cdr(car(x))
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="EQ")):
		return eq(car(x), car(cdr(x)))
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="ATOM")):
		return atom(car(x))
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="CONS")):
		return cons(car(x), car(cdr(x)))
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="NULL")):
		return eq(car(x), SExp(exp_type=2, sym_atm="NIL"))
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="INT")):
		return SExp(exp_type=2, sym_atm="T") if car(x).type == 1 \
			else SExp(exp_type=2, sym_atm="NIL")
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="PLUS")):
		if car(x).type == 1 and car(cdr(x)).type == 1:
			return SExp(exp_type=1, int_val=car(x).int_val+car(cdr(x)).int_val)
		else: raise MyError("Not correct format")
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="MINUS")):
		if car(x).type == 1 and car(cdr(x)).type == 1:
			return SExp(exp_type=1, int_val=car(x).int_val-car(cdr(x)).int_val)
		else: raise MyError("Not correct format")
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="TIMES")):
		if car(x).type == 1 and car(cdr(x)).type == 1:
			return SExp(exp_type=1, int_val=car(x).int_val*car(cdr(x)).int_val)
		else: raise MyError("Not correct format")
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="QUOTIENT")):
		if car(x).type == 1 and car(cdr(x)).type == 1:
			return SExp(exp_type=1, int_val=car(x).int_val/car(cdr(x)).int_val)
		else: raise MyError("Not correct format")
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="REMAINDER")):
		if car(x).type == 1 and car(cdr(x)).type == 1:
			return SExp(exp_type=1, int_val=car(x).int_val%car(cdr(x)).int_val)
		else: raise MyError("Not correct format")
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="LESS")):
		if car(x).type == 1 and car(cdr(x)).type == 1:
			return retLisp(car(x).int_val < car(cdr(x)).int_val)
		else: raise MyError("Not correct format")
	elif iseqbool(fn_name, SExp(exp_type=2, sym_atm="GREATER")):
		if car(x).type == 1 and car(cdr(x)).type == 1:
			return retLisp(car(x).int_val > car(cdr(x)).int_val)
		else: raise MyError("Not correct format")
	# TODO: ADD other primitive functions
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
		elif iseqbool(car(LSExp), SExp(exp_type=2, sym_atm="QUOTE")):
			return car(cdr(LSExp)), 0, dlist
		else:
			return lispapply(car(LSExp), evlist(cdr(LSExp), alist, dlist), alist, dlist), 0, dlist
	else:
		raise MyError("SExp should be atom or car of SExp should be atom")