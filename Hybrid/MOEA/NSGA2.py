import numpy as np
import modify_testcase as modifier
import version_evaluation as evaluation
import random
import GLOB
import GATool as GA
import pandas as pd


def run_NSGA2(SIR_name, version, test_size):
    evaluator = evaluation.VEval(SIR_name, version, test_size)
    dim = test_size
    population = GA.initial_genes(dim,GLOB.POP,version)
    if GLOB.DEBUG:
        print('0', len(population))
    population_history = [population]
    for i in range(GLOB.MAX_IT): 
        new_pop = GA.crossover(population, mr=1/dim)
        GA.evaluate(new_pop,evaluator)
        pareto = GA.get_pareto(new_pop)
        new_pop = select(pareto)
        population = new_pop
        population_history.append(population)
        if GLOB.DEBUG:
            print(i, len(population))

    first_pareto = get_first_pareto(population) #final result
    return first_pareto

def get_first_pareto(pop):
    '''
    get only first pareto

    :param pop:
    :return:
    '''
    return GA.get_pareto(pop)[0]

def select(pareto):
    '''
    select certain number of genes

    :param pareto:
    :return:
    '''
    new_pop = []
    remain_pop = GLOB.POP
    if GLOB.DEBUG:
        for i in range(len(pareto)):
            print('layer',i,':',len(pareto[i]))
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
        max_val = sorted_gene[-1].get_eval()[i]
        min_val = sorted_gene[0].get_eval()[i]

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

#run_NSGA2('sed',2,360)