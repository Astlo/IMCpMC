""" Simulation of pMC with modules"""
from random import random
from .modules import mysub
from .parse import myparse
import app.MCpMC.pmcmodules
import time

def typennotexp(expr):
    """return true if type is int or float"""
    return isinstance(expr, (int, float))


def sim(length, pmc,valu=None):
    """simulate pMC once for at most length step
        return the accumulated reward"""
    pmc.reinit()
    end = False
    step = 0
    cumu_reward = 0
    prob = 1
    while step < length and not end:
        step += 1
        numb_mod_deadlocked = 0
        for trans_mod in pmc.get_possible_transitions():
            if len(trans_mod) > 1:
                raise Exception("several action possible")
            if trans_mod:
                #print("################################################################################################")
                #print(trans_mod)
                if valu is None:
                    name, _, outcom, hasExp = trans_mod[0]
                    norma = len(outcom)
                    threshold = random()
                    j = 0
                    while j < len(outcom) and threshold > 0:
                        if hasExp:
                            threshold -= 1/norma
                        else:
                            threshold -= outcom[j][0]
                        j += 1
                    j -= 1
                    realprob = outcom[j][0]
                    if hasExp:
                        prob *= mysub(realprob, pmc.get_valuation())*norma
                    else:
                        prob *= mysub(realprob, pmc.get_valuation())/realprob
                        #print("mysub " , mysub(realprob, pmc.get_valuation()), " realprob ", realprob)
                    #print("prob ", mysub(realprob, pmc.get_valuation()), "realprob " , realprob, "get ", pmc.get_valuation())
                    pmc.maj(outcom[j][1])
                    cumu_reward += pmc.get_reward(name)
                else:
                    name, _, outcom, hasExp = trans_mod[0]
                    threshold = random()
                    j = 0
                    #print(threshold)
                    while j < len(outcom) and threshold > 0:
                        print("debut")
                        threshold -= mysub(mysub(outcom[j][0],valu),pmc.get_valuation())
                        j += 1

                    j -= 1
                    realprob = outcom[j][0]
                    print("sortie")
                    prob *= mysub(realprob, pmc.get_valuation())/mysub(mysub(outcom[j][0],valu),pmc.get_valuation())
                    #print("mysub ", mysub(realprob, pmc.get_valuation())/mysub(mysub(outcom[j][0],valu),pmc.get_valuation()))
                    #print(mysub(realprob, pmc.get_valuation()))
                    #print(mysub(mysub(outcom[j][0],valu),pmc.get_valuation()))
                    pmc.maj(outcom[j][1])
                    cumu_reward += pmc.get_reward(name)
            else:
                numb_mod_deadlocked += 1
            end = (numb_mod_deadlocked == len(pmc.modules))
    #print("prob ", prob*cumu_reward)
    #print("prob*cumu_reward ", prob*cumu_reward, " ", prob, " ", cumu_reward)
    return prob*cumu_reward



def simu(text, num_simu, length,valu=None):
    """length = length of exec, num_simu = number of simu, pmc = pmc to simulate"""
    time1 = time.time()
    pmc = myparse(text)
    pmc.preprocessing()
    time2 = time.time()
    #print('parsing took %0.3f ms' % ((time2-time1)*1000.0))

    accu_reward = 0
    accu_var = 0
    for _ in range(0, num_simu):
        #print("____________________________________________________________________________________________________")
        random_var_y = sim(length, pmc,valu)
        accu_reward += random_var_y
        accu_var += random_var_y*random_var_y

    estespy = accu_reward/num_simu
    try:
        estvar = (accu_var/(num_simu-1)-num_simu/(num_simu-1)*estespy**2)**(1/2)
    except ZeroDivisionError as e:
        raise Exception("Length of run must to superior or egal at 2") from e
    return [estespy, estvar, pmc]
