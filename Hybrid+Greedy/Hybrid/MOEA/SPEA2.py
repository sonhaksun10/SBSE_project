import numpy as np
import modify_testcase as modifier
import version_evaluation as evaluation
import random
import GLOB
import GATool as GA
import math


def run_SPEA2(SIR_name, version, test_size):
    evaluator = evaluation.VEval(SIR_name, version, test_size)
    dim = test_size
    population = GA.initial_genes(dim,GLOB.POP,version)
    archive = []
    population_history = [population]
    archive_history = [archive]
    if GLOB.DEBUG:
        print('0', len(population))
    for i in range(GLOB.MAX_IT):
        #update
        union = population+archive
        GA.evaluate(union,evaluator)
        get_fitness(union)
        archive = select(union)
        population = GA.crossover(archive)[GLOB.POP+1:]
        if GLOB.DEBUG:
            print(i, len(population))
        #save history
        population_history.append(population)
        archive_history.append(archive)

    first_pareto = get_first_pareto(archive) #final result
    return first_pareto

def get_first_pareto(pop):
    '''
    get only first pareto

    :param pop:
    :return:
    '''
    return GA.get_pareto(pop)[0]

def get_fitness(pop):
    #get score for each gene
    for p in pop:
        score = 0
        for q in pop:
            if GA._is_dominate(q,p):
                score += 1
        p.update_flag({'score':score})

    #get raw fitness for each gene
    for p in pop:
        raw = 0
        for q in pop:
            if GA._is_dominate(q,p):
                q_score = q.get_flag("score")
                raw += q_score
        p.update_flag({"raw":raw})

    #get density and fitness for each gene
    N = math.ceil(math.sqrt(GLOB.POP+GLOB.MAX_ARCHIVE_SPEA2))
    for p in pop:
        dens = 0
        for q in pop: #get distance from others
            dist = np.linalg.norm(p.get_eval() - q.get_eval())
            q.update_flag({'dist':dist})
        sorted_pop = sorted(pop, key=lambda gene:gene.get_flag('dist'))
        dens = sorted_pop[N+1].get_flag('dist')
        fitness = dens + p.get_flag('raw')
        p.update_flag({'dense':dens, 'fitness':fitness})


def select(pop):
    '''
    select certain number of genes

    :param pareto:
    :return:
    '''
    new_pop = []
    for p in pop:
        if p.get_flag('fitness') < 1:
            new_pop.append(p)

    if len(new_pop) > GLOB.MAX_ARCHIVE_SPEA2:
        if GLOB.DEBUG:
            print('truncate population, current size', len(new_pop), 'target size', GLOB.MAX_ARCHIVE_SPEA2)
        num_remove = len(new_pop) - GLOB.MAX_ARCHIVE_SPEA2

        # calculate distance to other nodes
        for p in new_pop:
            dist_table = []
            for i, q in enumerate(new_pop):
                dist = np.linalg.norm(p.get_eval() - q.get_eval())
                dist_table.append((dist, i))
            dist_table = sorted(dist_table)

            dist_indicator = 0
            for i in range(1,11):
                dist_indicator += dist_table[i][0] / (10 ** (i - 1))
            p.update_flag({'dist_table': dist_table, 'dist_indicator': dist_indicator})

        '''
        for _ in range(num_remove):
            #truncate, find p with the closest to neighbor
            removed = False
            for p in new_pop:
                truncate = True
                dt1 = p.get_flag('dist_table')
                for q in new_pop:
                    if p == q:
                        continue
                    dt2 = q.get_flag('dist_table')

                    for d1,d2 in zip(dt1,dt2):
                        if d1[0] > d2[0]:
                            truncate = False
                            break
                        elif d1[0] < d2[0]:
                            break

                    if not truncate:
                        break

                if truncate:
                    new_pop.remove(p)
                    removed = True
                    break

            if not removed:
                if GLOB.DEBUG:
                    for p in new_pop:
                        print(p.get_flag('dist_table'))
                raise Exception('one element in archive is not removed')
        '''

        new_pop = sorted(new_pop, key= lambda gene: gene.get_flag('dist_indicator'))[-GLOB.MAX_ARCHIVE_SPEA2:]


    elif len(new_pop) < GLOB.MAX_ARCHIVE_SPEA2:
        if GLOB.DEBUG:
            print('current size', len(new_pop), 'target size', GLOB.MAX_ARCHIVE_SPEA2)
        new_pop = sorted(pop, key= lambda gene: gene.get_flag('fitness'))[:GLOB.MAX_ARCHIVE_SPEA2]

    return new_pop




#run_SPEA2('sed',1,360)