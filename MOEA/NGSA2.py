import numpy as np
import modify_testcase as modifier
import random

POP = 100
MAX_IT = 30
FIT_FUNC_GENERATED = False

class Gene_Info:
    def __init__(self,sequence):
        self.sequence = sequence
        self.eval = None

    def set_eval(self,eval):
        self.eval = eval

    def get_eval(self):
        return self.eval

    def get_seq(self):
        return self.sequence

    def is_evaluated(self):
        return not (self.eval is None)

def run_NSGA2(input_fname):
    modify = modifier.modify_testcase(input_fname)
    dim = modify.get_datasize()

    population = initial_genes(dim)
    population_history = [population]
    for i in range(MAX_IT):
        new_pop = crossover(population)
        evaluate(new_pop,modify)
        pareto = get_pareto(new_pop)
        new_pop = select(pareto)
        population = new_pop
        population_history.append(population)

    first_pareto = get_first_pareto(population) #final result


def initial_genes(dim):
    '''

    :return: list(Gene_Info)
    '''

    pop = []
    if type(dim) == tuple:
        pass
    else:
        for i in range(POP):
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
    p = 0.2
    gene_size = len(pop[0].get_seq())
    for i in range(POP):
        gene1, gene2 = random.sample(pop,2)
        seq1, seq2 = gene1.get_seq(), gene2.get_seq()
        child_seq = []
        query, id = seq1, 'seq1'
        idx = 0
        while len(child_seq) < gene_size:
            while query[idx] in child_seq:
                idx = (idx+1)%gene_size
            child_seq.append(query[idx])
            if random.random() < p:
                if id == 'seq1':
                    query, id = seq2, 'seq2'
                else:
                    query, id = seq1, 'seq1'

        child = Gene_Info(child_seq)
        child_pop.append(child)

    new_pop += child_pop

    return new_pop

def evaluate(pop,modify):
    '''
    complete this function after feature detection team finished their work

    :param pop:
    :return:        None
    '''

    for gene in pop:
        if gene.is_evaluated():
            continue

        if FIT_FUNC_GENERATED:
            pass
        else:         #remove this part after fitness evaluation is done
            gene.set_eval(np.random.rand(3))


def get_pareto(pop):
    '''
    important!
    get pareto front with new data

    return type: [first pareto, second pareto, ... ,last pareto]
    ex) first pareto = [gene3, gene15, gene19, gene22, ...]
        second pareto = [gene5, gene10, gene20, ...]

    :param pop:
    :return:    list(list(Gene_Info))
    '''
    pareto = [[]]
    cp_pop = pop[:]

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
    for e1,e2 in zip(gene1.get_eval(), gene2.get_eval()):
        if e1 <= e2:
            return False
    return True

def get_first_pareto(pop):
    '''
    get only first pareto

    :param pop:
    :return:
    '''
    return get_pareto(pop)[0]

def select(pareto):
    '''
    select certain number of genes

    :param pareto:
    :return:
    '''
    new_pop = []
    remain_pop = POP//2
    for layer in pareto:
        if len(layer) <= remain_pop:
            new_pop += layer
            remain_pop -= len(layer)
        elif remain_pop > 0:
            new_pop += crowding_dist(layer, remain_pop)
            break

    return new_pop

def crowding_dist(layer,num_select):
    distance = [0] * len(layer)

    num_obj = len(layer[0].get_eval())
    for i in range(num_obj):
        cp_layer = layer[:]
        sorted_gene = sorted(cp_layer, key= lambda gene: gene.get_eval()[i])
        max_val = max(cp_layer, key=lambda gene: gene.get_eval()[i]).get_eval()[i]
        min_val = min(cp_layer, key=lambda gene: gene.get_eval()[i]).get_eval()[i]

        idx = layer.index(sorted_gene[0])
        distance[idx] += 999999999999
        idx = layer.index(sorted_gene[-1])
        distance[idx] += 999999999999

        for j in range(1,len(layer)-1):
            idx = layer.index(sorted_gene[j])
            distance[idx] = distance[idx] + (sorted_gene[j+1].get_eval()[i] - sorted_gene[j-1].get_eval()[i])/(max_val - min_val + 1e-6)

    cutline = sorted(distance)[-num_select]
    res = []
    for i in range(len(distance)):
        if distance[i] >= cutline:
            res.append(layer[i])

    return res



run_NSGA2('make.tests')