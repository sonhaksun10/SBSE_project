import numpy as np
import GLOB
import random
import copy
import pandas as pd

class Gene_Info:
    def __init__(self,sequence):
        self.sequence = sequence    #type: #np.ndarray
        self.eval = None            #type: #np.ndarray
        self.flag = dict()

    def set_eval(self,eval):
        self.eval = eval

    def get_eval(self):
        return self.eval

    def get_seq(self):
        return self.sequence

    def is_evaluated(self):
        return not (self.eval is None)

    def update_flag(self, flag):
        for key in flag.keys():
            self.flag[key] = flag[key]

    def get_flag(self, key):
        if key not in self.flag:
            return None
        return self.flag[key]

def initial_genes(dim,pop_size,version):
    '''
    :return: list(Gene_Info)
    '''
    state = 'test_ordering_state_(for_v'+str(version)+').csv'
    delta = 'test_ordering_delta_(for_v'+str(version)+').csv'
    fault = 'test_ordering_fault_(for_v'+str(version)+').csv'
    pop1=[]
    pop2=[]
    pop3=[]
    with open(state, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            pop1.append(int(line))

    with open(delta, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            pop2.append(int(line))

    with open(fault, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            pop3.append(int(line))
    pop = []
    pop.append(Gene_Info(np.asarray(pop1)))
    pop.append(Gene_Info(np.asarray(pop2)))
    pop.append(Gene_Info(np.asarray(pop3)))
    for i in range(pop_size-3):
        gene = Gene_Info(np.random.permutation(dim))
        pop.append(gene)
    return pop


def crossover(pop,cr = GLOB.CROSSOVER_RATE, mr = GLOB.MUTATION_RATE):
    '''

    :param pop: list(Gene_info)
    :return: list(Gene_Info)
    '''
    new_pop = pop[:]
    child_pop = []
    gene_size = len(new_pop[0].get_seq())
    for i in range(GLOB.POP):
        if random.random() < cr:
            gene1, gene2 = random.sample(pop,2)
            child = PMX(gene1,gene2)

            child_pop.append(child)
        else:
            seq = random.sample(pop,1)[0].get_seq().copy()
            child_pop.append(Gene_Info(seq))

    for child in child_pop:
        if random.random() < mr:
            seq = child.get_seq()
            idx1,idx2 = random.sample(list(seq),2)
            seq[idx2], seq[idx1] = seq[idx1], seq[idx2]

    #filter out genes that have the same sequence
    for child in child_pop:
        for parent in pop:
            if (child.get_seq() == parent.get_seq()).all():
                child_pop.remove(child)
                break

    new_pop += child_pop

    return new_pop

'''
def PMX(gene1,gene2,gene_size):
    seq1, seq2 = gene1.get_seq(), gene2.get_seq()
    child_seq = []
    query, id = seq1, 'seq1'
    idx = 0
    p = 0.2
    while len(child_seq) < gene_size:
        while query[idx] in child_seq:
            idx = (idx + 1) % gene_size
        child_seq.append(query[idx])
        if random.random() < p:
            if id == 'seq1':
                query, id = seq2, 'seq2'
            else:
                query, id = seq1, 'seq1'

    child = Gene_Info(child_seq)
    return child
'''

def PMX(parent1, parent2):
    seq1, seq2 = parent1.get_seq(), parent2.get_seq()
    size = min(len(seq1), len(seq2))
    p1, p2 = [0]*size, [0]*size
    child1,child2 = copy.deepcopy(seq1), copy.deepcopy(seq2)
    cut1 = random.randint(0, size - 1)
    cut2 = random.randint(cut1 + 1, size)

    for i in range(size):
        p1[seq1[i]] = i
        p2[seq2[i]] = i

    # Apply crossover between cx points
    for i in range(cut1, cut2):
        # Keep track of the selected values
        temp1 = child1[i]
        temp2 = child2[i]
        # Swap the matched value
        child1[i], child1[p1[temp2]] = temp2, temp1
        child2[i], child2[p2[temp1]] = temp1, temp2
        # Position bookkeeping
        p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
        p2[temp1], p2[temp2] = p2[temp2], p2[temp1]

    child = Gene_Info(child1)
    return child


def evaluate(pop,evaluator):
    '''
    complete this function after feature detection team finished their work

    :param pop:     list(Gene_Info)
    :return:        None
    '''

    for gene in pop:
        if gene.is_evaluated():
            continue

        if GLOB.FIT_FUNC_GENERATED:
            eval = evaluator.eval(gene.get_seq())
            gene.set_eval(eval)
        else:         #remove this part after fitness evaluation is done
            gene.set_eval(np.random.rand(3))


def get_pareto(pop):
    '''
    important!
    get pareto front with new data - non-dominated sort

    return type: [first pareto, second pareto, ... ,last pareto]
    ex) first pareto = [gene3, gene15, gene19, gene22, ...]
        second pareto = [gene5, gene10, gene20, ...]

    :param pop:
    :return:    list(list(Gene_Info))
    '''
    pareto = [[]]

    S = [[] for i in range(len(pop))]
    n = [0 for i in range(len(pop))]
    rank = [0 for i in range(len(pop))]

    for i in range(len(pop)):
        p = pop[i]
        for j in range(len(pop)):
            q = pop[j]
            if _is_dominate(p,q):
                S[i].append(j)
            elif _is_dominate(q,p):
                n[i] += 1
        if n[i] == 0:
            rank[i] = 0
            pareto[0].append(p)

    x = 0
    while (pareto[x] != []):
        Q = []
        for p in pareto[x]:
            i = pop.index(p)
            for j in S[i]:
                n[j] -= 1
                if (n[j] == 0):
                    rank[j] = x + 1
                    if pop[j] not in Q:
                        Q.append(pop[j])
        x += 1
        pareto.append(Q)

    pareto.pop()
    return pareto


def _is_dominate(gene1,gene2):
    '''
    check gene1 dominates gene2
    :param gene1:
    :param gene2:
    :return:
    '''
    if gene1 == gene2:
        return False

    for e1,e2 in zip(gene1.get_eval(), gene2.get_eval()):
        if e1 < e2:
            return False
    if (gene1.get_eval() == gene2.get_eval()).all():
        return False
    return True