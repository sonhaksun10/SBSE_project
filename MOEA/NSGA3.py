import numpy as np
import modify_testcase as modifier
import random
import GLOB
import GATool as GA


def run_NSGA3(input_fname):
    modify = modifier.modify_testcase(input_fname)
    dim = modify.get_datasize()
    reference = get_ref()

    population = GA.initial_genes(dim,GLOB.POP)
    population_history = [population]
    for i in range(GLOB.MAX_IT):
        new_pop = GA.crossover(population)
        GA.evaluate(new_pop,modify)
        pareto = GA.get_pareto(new_pop)
        new_pop = select(pareto)
        population = new_pop
        population_history.append(population)

    first_pareto = get_first_pareto(population) #final result

def get_ref():
    reference = []
    for l in GLOB.reference:
        gene = GA.Gene_Info(None)
        gene.set_eval = np.array(l)
        reference.append(gene)
    return reference

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
    remain_pop = GLOB.POP//2
    for layer in pareto:
        if len(layer) <= remain_pop:
            new_pop += layer
            remain_pop -= len(layer)
        elif remain_pop > 0:
            new_pop += select_in_layer(layer, remain_pop)
            break

    return new_pop

def select_in_layer(layer,num_select):
    return layer



run_NSGA2('make.tests')
