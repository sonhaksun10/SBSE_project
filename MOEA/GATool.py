import numpy as np
import GLOB
import random

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

def initial_genes(dim,pop_size):
    '''

    :return: list(Gene_Info)
    '''

    pop = []
    if type(dim) == tuple:
        pass
    else:
        for i in range(pop_size):
            gene = Gene_Info(np.random.permutation(dim))
            pop.append(gene)
    return pop

def crossover(pop):
    '''

    :param pop:
    :return: list(Gene_Info)
    '''
    new_pop = pop[:]
    child_pop = []
    gene_size = len(pop[0].get_seq())
    for i in range(GLOB.POP):
        gene1, gene2 = random.sample(pop,2)
        child = PMX(gene1,gene2,gene_size)

        child_pop.append(child)

    new_pop += child_pop

    return new_pop

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

def evaluate(pop,modify):
    '''
    complete this function after feature detection team finished their work

    :param pop:
    :return:        None
    '''

    for gene in pop:
        if gene.is_evaluated():
            continue

        if GLOB.FIT_FUNC_GENERATED:
            pass
        else:         #remove this part after fitness evaluation is done
            gene.set_eval(np.random.rand(3))

