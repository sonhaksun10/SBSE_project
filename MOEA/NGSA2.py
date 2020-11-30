import numpy as np
import modify_testcase as modifier
import random
import GLOB
import GATool as GA


def run_NSGA2(input_fname):
    modify = modifier.modify_testcase(input_fname)
    dim = modify.get_datasize()

    population = GA.initial_genes(dim,GLOB.POP)
    population_history = [population]
    for i in range(GLOB.MAX_IT):
        new_pop = GA.crossover(population)
        GA.evaluate(new_pop,modify)
        pareto = get_pareto(new_pop)
        new_pop = select(pareto)
        population = new_pop
        population_history.append(population)

    first_pareto = get_first_pareto(population) #final result



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
    remain_pop = GLOB.POP//2
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
        distance[idx] += GLOB.LARGE
        idx = layer.index(sorted_gene[-1])
        distance[idx] += GLOB.LARGE

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