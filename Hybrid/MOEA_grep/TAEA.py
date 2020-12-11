import numpy as np
import modify_testcase as modifier
import version_evaluation as evaluation
import random
import GLOB
import GATool as GA

def run_TAEA(SIR_name, version, test_size):
    evaluator = evaluation.VEval(SIR_name, version, test_size)
    dim = test_size

    population = GA.initial_genes(dim, GLOB.POP,version)
    population_history = [population]
    CA, DA = [], [] #covergence archive, diversity archive
    GA.evaluate(population,evaluator)
    if GLOB.DEBUG:
        print('0', 0)

    for i in range(GLOB.MAX_IT):
        CA, DA = collect_non_dominated(population,CA,DA)
        #print(len(CA), len(DA))
        population = new_crossover(CA,DA,GLOB.CROSSOVER_RATE,1/test_size,dim,version)
        GA.evaluate(population,evaluator)
        if GLOB.DEBUG:
            print(i,len(CA+DA), 'covergence archive size', len(CA), 'divergence archive size', len(DA))

    return CA+DA



def collect_non_dominated(pop,CA,DA):
    def distance(eval1, eval2):
        return np.linalg.norm(eval1-eval2)
    new_CA = CA[:]
    new_DA = DA[:]

    #step1: update CA and DA
    for i in range(len(pop)):
        p = pop[i]

        #check if non dominated
        p.update_flag({"non-dominated":True,"dominate-other":False})
        for archive in new_CA + new_DA:
            if GA._is_dominate(archive,p):
                p.update_flag({"non-dominated":False})
                break
        if not p.get_flag("non-dominated"): #skip if not non-dominated
            continue

        #check if it dominated other
        for archive in new_CA:
            if GA._is_dominate(p,archive):
                new_CA.remove(archive)
                p.update_flag({"dominate-other":True})
        for archive in new_DA:
            if GA._is_dominate(p,archive):
                new_DA.remove(archive)
                p.update_flag({"dominate-other":True})

        if p.get_flag("dominate-other"): #dominate other, add at CA
            new_CA.append(p)
        else:                           #not dominate other, add at DA
            new_DA.append(p)

    #step2: limit the size of CA and DA
    if len(new_CA + new_DA) > GLOB.MAX_ARCHIVE_TAEA:
        if len(new_CA) > GLOB.MAX_ARCHIVE_TAEA:
            new_DA = []
            return
        for pop_da in new_DA:
            pop_da.update_flag({"len":GLOB.LARGE})
            for pop_ca in new_CA:
                dist = distance(pop_da.get_eval(),pop_ca.get_eval())
                if dist < pop_da.get_flag("len"):
                    pop_da.update_flag({"len":dist})

        #remove some population in DA
        new_DA = sorted(new_DA,key= lambda pop: pop.get_flag("len"))
        new_DA = new_DA[-GLOB.MAX_ARCHIVE_TAEA+len(new_CA):]

    return new_CA, new_DA



def new_crossover(CA,DA,cr,mr,dim,version):
    ratio = GLOB.CA_DA_RATIO
    new_pop = []
    if len(CA+DA) < 2:
        new_pop += GA.initial_genes(dim, GLOB.POP,version)
        return new_pop
    elif len(CA) < 2 or len(DA) < 2:
        new_pop += GA.crossover(CA+DA,mr=mr)
        return new_pop

    for i in range(GLOB.POP):
        child = None

        # consider crossover rate
        if random.random() < cr:
            p1,p2 = None,None

            # randomly choose parents between CA and DA
            rand_num = random.random()
            if rand_num < ratio * ratio:
                p1, p2 = random.sample(CA, 2)
            elif rand_num < 2 * ratio - ratio * ratio:
                if random.random() < 0.5:
                    p1 = random.sample(CA, 1)[0]
                    p2 = random.sample(DA, 1)[0]
                else:
                    p1 = random.sample(DA, 1)[0]
                    p2 = random.sample(CA, 1)[0]
            else:
                p1, p2 = random.sample(DA, 2)

            child = GA.PMX(p1,p2)
        else:
            seq = random.sample(CA+DA, 1)[0].get_seq().copy()
            child = GA.Gene_Info(seq)

        # mutation
        if random.random() < mr:
            seq = child.get_seq()
            idx1, idx2 = random.sample(list(seq), 2)
            seq[idx2], seq[idx1] = seq[idx1], seq[idx2]

        #check overlap
        overlapped = False
        for parent in CA+DA:
            if (child.get_seq() == parent.get_seq()).all():
                overlapped = True
                break
        if overlapped: # if overlap, do not add child at new_pop
            continue

        new_pop.append(child)

    return new_pop

#run_TAEA('sed',1,360)