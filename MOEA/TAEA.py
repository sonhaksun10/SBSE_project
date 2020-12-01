import numpy as np
import modify_testcase as modifier
import random
import GLOB
import GATool as GA

def run_TAEA(input_fname):
    modify = modifier.modify_testcase(input_fname)
    dim = modify.get_datasize()

    population = GA.initial_genes(dim, GLOB.POP)
    population_history = [population]
    CA, DA = [], [] #covergence archive, diversity archive
    GA.evaluate(population,modify)

    for i in range(GLOB.MAX_IT):
        collect_non_dominated(population,CA,DA)
        new_pop = GA.crossover(CA+DA)
        GA.evaluate(new_pop,modify)



def collect_non_dominated(pop,CA,DA):
    def distance(eval1, eval2):
        return np.linalg.norm(eval1-eval2)

    #step1: update CA and DA
    for i in range(len(pop)):
        p = pop[i]

        #check if non dominated
        p.update_flag({"non-dominated":True,"dominate-other":False})
        for archive in CA+DA:
            if GA._is_dominate(archive,p):
                p.update_flag({"non-dominated":False})
                break
        if not p.get_flag("non-dominated"): #skip if not non-dominated
            break

        #check if it dominated other
        for archive in CA:
            if GA._is_dominate(p,archive):
                CA.remove(archive)
                p.update_flag({"dominate-other":True})
        for archive in DA:
            if GA._is_dominate(p,archive):
                DA.remove(archive)
                p.update_flag({"dominate-other":True})

        if p.get_flag("dominate-other"): #dominate other, add at CA
            CA.append(p)
        else:                           #not dominate other, add at DA
            DA.append(p)

    #step2: limit the size of CA and DA
    if len(CA+DA) > GLOB.MAX_ARCHIVE:
        if len(CA) > GLOB.MAX_ARCHIVE:
            DA = []
            return
        for pop_da in DA:
            pop_da.update_flag({"len":GLOB.LARGE})
            for pop_ca in CA:
                dist = distance(pop_da.get_eval(),pop_ca.get_eval())
                if dist < pop_da.get_flag("len"):
                    pop_da.update_flag({"len":dist})

        #remove some population in DA
        new_DA = sorted(DA,key= lambda pop: pop.get_flag("len"))
        DA = new_DA[-GLOB.MAX_ARCHIVE+len(CA):]



def new_crossover(CA,DA):
    ratio = GLOB.CA_DA_RATIO
    new_pop = []

    for i in range(GLOB.POP):
        p1,p2 = None,None
        if len(DA) != 0:
            rand_num = random.random()
            if rand_num < ratio*ratio:
                p1,p2 = random.sample(CA,2)
            elif rand_num < 2*ratio-ratio*ratio:
                p1 = random.sample(CA,1)[0]
                p2 = random.sample(DA,1)[0]
            else:
                p1,p2 = random.sample(DA,2)
        else:
            p1,p2 = random.sample(CA,2)

        child = GA.PMX(p1,p2)
        new_pop.append(child)

    return new_pop

