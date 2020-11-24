import numpy as np

MAX_IT = 30

class Gene_Info:
    def __init__(self,sequence):
        self.sequence = sequence
        self.eval = None

    def set_eval(self,eval):
        self.eval = eval

    def get_data(self):
        return self.sequence,self.eval

    def is_evaluated(self):
        return self.eval is None

def run_NSGA2():
    population = initial_genes()
    population_history = [population]
    for i in range(MAX_IT):
        new_pop = population
        evaluate(new_pop)
        pareto = get_pareto(new_pop)
        new_pop = select(pareto)
        population = new_pop
        population_history.append(population)

    first_pareto = get_first_pareto(population) #final result


def initial_genes():
    '''

    :return: list(Gene_Info)
    '''
    pass

def crossover(pop):
    '''

    :param pop:
    :return: list(Gene_Info)
    '''
    new_pop = pop[:]

def evaluate(pop):
    '''
    complete this function after feature detection team finished their work

    :param pop:
    :return:
    '''
    pass

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
    pass

def get_first_pareto(pop):
    '''
    get only first pareto

    :param pop:
    :return:
    '''

def select(pareto):
    '''
    select certain number of genes

    :param pareto:
    :return:
    '''
    pass
