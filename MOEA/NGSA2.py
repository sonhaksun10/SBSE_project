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
        new_pop = select(new_pop, pareto)
        population = new_pop
        population_history.append(population)


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
    pass

def get_pareto(pop):
    pass

def select(pop,pareto):
    pass