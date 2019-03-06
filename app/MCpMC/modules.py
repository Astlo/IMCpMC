""" Define pMC with modules """
import sympy
def copy_dict(dic):
    """ copy a dictionary """
    return {**dic}

def exp_to_fun(exp):
    try:
        free_var = exp.free_symbols
        b=True
    except:
        b=False
    if b:
        f=sympy.lambdify(free_var,exp,modules={'And':all, 'Or':any})
        def g(dic):
            eval=list(map(lambda x: dic[x],free_var))
            return (f(*eval))
        return g
    else:
        return lambda *x: exp


def mysub(exp, dic):
    """ sympy subs but filtering local dictionary with only variables in exp"""
    try:
        free_var = exp.free_symbols
    except:
        free_var = []

    reduced_dic = {x:dic[x] for x in free_var if x in dic}
    #print("reduced_dic" , reduced_dic)
    if reduced_dic:
        return exp.subs(reduced_dic)
    return exp


class Module:
    """ module of a pMC with modules """
    def __init__(self, name):
        self.name = name
        self.initial_value_state = {}
        self.trans = []
        self.current_value_state = {}
        self.alph = {}
    def add_state(self, state, min_value, max_value, ini=None):
        """ add a state """
        if ini is None:
            init = min_value
        else:
            init = ini
        self.initial_value_state[state] = init
        self.current_value_state[state] = init
    def add_transition(self, name, cond, outcom):
        """ add a transition """
        self.alph[name] = True
        self.trans += [[name, cond, outcom,exp_to_fun(cond)]]
    def reinit(self):
        """ reinitialize all state to their initial value """
        self.current_value_state = copy_dict(self.initial_value_state)
    def eval(self, exp, global_substitution):
        """ evaluate an expression with the current value of the states
            given the current values of the global variables"""
        return mysub(exp, {**self.current_value_state, **global_substitution})

    def preprocessing(self, global_substitution):
        transitions = self.trans
        self.trans = []
        for  name, cond, outcom, funcond in transitions:
            hasExp = False
            for transition in outcom:
                """return false if there is no symbol or no expression in transitions"""
                if not isinstance(transition[0], (int, float, sympy.numbers.Float)):
                    hasExp = True
                    break
            self.trans += [[name, cond, outcom, funcond, hasExp]]

    def get_possible_transitions(self, global_substitution):
        """ return the transition doable given the current value of the global variable """
        return [[name, cond, outcom, hasExp]
                for  name, cond, outcom, funcond, hasExp in self.trans
                if funcond({**global_substitution, **self.current_value_state})]
    def copy(self, name):
        """ return a copy of the module """
        mod = Module(name)
        mod.initial_value_state = copy_dict(self.initial_value_state)
        mod.current_value_state = copy_dict(self.current_value_state)
        mod.alph = copy_dict(self.alph)
        mod.trans = []
        for namet, cond, outcom in self.trans:
            mod.add_transition(namet, cond, list(outcom))
        return mod
    def replace(self, name1, name2):
        """ replace name1 with name2 in the module """
        if name1 in self.initial_value_state:
            self.initial_value_state[name2] = self.initial_value_state[name1]
            del self.initial_value_state[name1]
            self.current_value_state[name2] = self.current_value_state[name1]
            del self.current_value_state[name1]
        substitution = {name1 : name2}
        new_trans = []
        for i in range(0, len(self.trans)):
            name, cond, outcom, funcond = self.trans[i]
            if name == name1:
                new_name = name2
                self.alph[name2] = True
                del self.alph[name1]
            else:
                new_name = name
            new_outcom = []
            for var, update in outcom:
                new_outcom += [[mysub(var, substitution),
                                {mysub(state, substitution):mysub(state_up, substitution)
                                 for state, state_up in update.items()}]]
            new_trans += [[new_name, mysub(cond, substitution), new_outcom, funcond]]
        self.trans = new_trans
    def set_init_value(self, state, value):
        """ declare a new initial value for a state """
        if state in self.initial_value_state:
            self.initial_value_state[state] = value
            self.initial_value_state[state] = value
    def maj(self, update, global_valu):
        """ update the current states values according to up """
        temp = copy_dict(self.current_value_state)
        #print("current_value_state " , self.current_value_state)
        for k in self.current_value_state:
            #print("k",k)
            if k in update:
                self.current_value_state[k] = mysub(update[k], {**temp, **global_valu})
                #print("new ", self.current_value_state[k])
            else:
                self.current_value_state[k] = self.current_value_state[k]
        return temp
