import MCpMC.modules

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

class PmcModules:
    """ pMC with modules """

    def __init__(self):
        self.param = []
        self.varGlobalInit = {}
        self.current_value_global = {}
        self.modules = []
        self.reward = []
        pass
    def add_parameter(self, param):
        """ add a parameter """
        self.param += [param]
    def add_global_variable(self, state, min_value, max_value, ini=None):
        """ add a global variable with initial value"""
        if ini is None:
            init = min_value
        else:
            init = ini
        self.varGlobalInit[state] = init
        self.current_value_global[state] = init
    def add_module(self, mod):
        """ add a module """
        self.modules += [mod]
    def reinit(self):
        """ reinit all module and global variables to their initial values"""
        self.current_value_global = {**self.varGlobalInit}
        for mod in self.modules:
            mod.reinit()
    def get_possible_transitions(self):
        """ return the doable transitions """
        res = [m.get_possible_transitions(self.current_value_global) for m in self.modules]

        name = [[tr[0] for tr in t if tr[0] != ""] for t in res]
        def good_name(action):
            """ indicate whether the name is ok for all modules"""
            for i in range(0, len(res)):
                if (action in self.modules[i].alph) and (action not in name[i]):
                    return False
            return True
        name = [list(filter(good_name, na)) for i, na in enumerate(name)]
        res2 = [list(filter(lambda t: (t[0] in name[i]) or t[0] == "", a))
                for i, a in enumerate(res)]
        #print("res ", res2)
        return res2

    def preprocessing(self):
        """ preprocess for each state """
        [m.preprocessing(self.current_value_global) for m in self.modules]


    def get_module(self, name):
        """ return the module corresponding to name"""
        for mod in self.modules:
            if mod.name == name:
                return mod
        raise Exception("moule "+name+" not found")
    def set_init_value(self, variable, value):
        """ set a new initial value for a global variable """
        if variable in self.current_value_global:
            self.current_value_global[variable] = value
        else:
            for mod in self.modules:
                mod.set_init_value(variable, value)
    def add_reward(self, name, cond, reward):
        """ add a reward """
        self.reward += [[name, cond, reward]]
    def get_reward(self, act):
        """ return the reward of a given action """
        #print(self.reward)
        cumu_reward = 0
        substitution = self.get_valuation()
        for rew_action, cond, reward in self.reward:
            #print(rew_action, cond, mysub(cond, substitution))
            if (rew_action == act or act == '') and mysub(cond, substitution):
                cumu_reward += mysub(reward, substitution)
                #print("cumu_reward " , cumu_reward)
        return cumu_reward
    def maj(self, update):
        """ update the globale variable and all modules according to up"""
        valuation = self.get_valuation()
        #print("glo ", self.current_value_global)
        for mod in self.modules:
            mod.maj(update, self.current_value_global)
        temp = {}
        for k in self.current_value_global:
            if k in update:
                temp[k] = mysub(update[k], valuation)
            else:
                temp[k] = self.current_value_global[k]
        self.current_value_global = temp
        #print("new ", self.current_value_global)
    def get_valuation(self):
        """ return the current value of all variable (globale+sates in modules)"""
        return {**dict(i for mod in self.modules
                       for i in mod.current_value_state.items()), **self.current_value_global}
