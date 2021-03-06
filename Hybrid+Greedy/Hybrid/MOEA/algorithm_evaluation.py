import csv
import GLOB
import GATool as GA
import numpy as np
import random

def read_file(SIR_name, version):
    '''
    Read files in Result directory and get data
    return data by each MOEA and trial
    return reference points for the specific SIR program and version

    data: dictionary, key = MOEA value = 2D array.
          first dimension for each trial
          second dimension for data
          ex) dict['NSGA2'] = [[pt1,pt2, ...], [pt100,pt101, ...], ...]
              each pt = [evaluation metric1, metric2, metric3, ...]

    ref_pt: array.
            ex) ref_pt = [pt1, pt2, pt3, ...]
            each pt = [evaluation metric1, metric2, metric3, ...]

    :param SIR_name:  String, SIR program name
    :param version:   int, version of SIR program
    :return:
    '''
    directory = GLOB.RESULT_DIRECTORY + SIR_name + '/'
    data = dict()
    ref_pt = []

    for MOEA in GLOB.TRY_ALGORITHM:
        data_moea = [[] for i in range(GLOB.TRIALS_PER_VERSION)]
        for i in range(GLOB.TRIALS_PER_VERSION):
            fname = 'eval_' + SIR_name + '_version' + str(version) + '_' + MOEA + '_trial' + str(i) + '.csv'
            with open(directory + fname, 'r') as f:
                f.readline()
                rdr = csv.reader(f)
                for line in rdr:
                    for j in range(len(line)):
                        line[j] = float(line[j])
                    data_moea[i].append(np.array(line))
                    gene = GA.Gene_Info(None)
                    gene.set_eval(np.array(line))
                    ref_pt.append(gene)

            ref_pt = GA.get_pareto(ref_pt)[0] #update reference point
        data[MOEA] = data_moea

    for i in range(len(ref_pt)):
        ref_pt[i] = ref_pt[i].get_eval()

    return data, ref_pt

def write_result(SIR_name, version, result):
    directory = GLOB.RESULT_DIRECTORY
    for MOEA in GLOB.TRY_ALGORITHM:
        res = result[MOEA]
        mean = res.mean(axis=0)
        std = res.std(axis=0)

        fname = + SIR_name + '_version' + str(version) + '_' + MOEA + '.csv'
        with open(directory + fname, newline='') as f:
            wr = csv.writer(f)
            wr.writerow(['','EPSIOLON','HV','IGD'])
            wr.writerow(['mean'] + list(mean))
            wr.writerow(['std'] + list(std))
            wr.writerow([''])
            for i in range(len(res)):
                wr.writerow(['trial'+str(i)] + list(res[i]))



def calc_indicators(SIR_name, version):
    res = dict()
    data, ref_pt = read_file(SIR_name,version)

    for MOEA in GLOB.TRY_ALGORITHM:
        res_moea = []
        for i in range(GLOB.TRIALS_PER_VERSION):
            HV = get_HV(data[MOEA][i])
            IGD = get_IGD(data[MOEA][i], ref_pt)
            EPSILON = get_EPSILON(data[MOEA][i], ref_pt)
            res_moea.append([EPSILON, HV, IGD])
        res[MOEA] = np.array(res_moea)
    write_result(SIR_name,version,res)

def get_HV(data):
    '''
    Hyper volume of moea solution
    High HV = Diverse pareto front

    all evaluation metric is zero -> do not consider the evaluation metric

    :param data: list(pt)
    :return:     float()
    '''
    print('HV')
    HV = 0
    inv_data = []

    for d in data:
        nearest_pt = [0,0,0]
        for invd in inv_data:
            for idx in range(3):
                if d[idx] >= invd[idx] >= nearest_pt[idx]:
                    nearest_pt[idx] = invd[idx]
        HV_add = 1
        for e in d-np.array(nearest_pt):
            if e > 0.:
                HV_add *= e
        HV += HV_add
        inv_data.append(d)

    return HV

def get_IGD(data,ref):
    '''
    average distance from each reference point to its closest solution
    Small IGD = Good pareto front

    :param data: list(pt)
    :param ref:  list(pt)
    :return:     float
    '''
    smallest_dist = GLOB.LARGE
    rsize = len(ref)
    for pt in data:
        dist = 0
        for rpt in ref:
            dist += np.linalg.norm(pt-rpt)
        dist /= rsize

        # update smallest distance
        if dist < smallest_dist:
            smallest_dist = dist
    return smallest_dist

def get_EPSILON(data,ref):
    largest_dist = 0
    for pt in data:
        smallest_dist_per_pt = GLOB.LARGE
        for rpt in ref:
            dist = np.linalg.norm(pt-rpt)
            if dist < smallest_dist_per_pt:
                smallest_dist_per_pt = dist

        if smallest_dist_per_pt > largest_dist:
            largest_dist = smallest_dist_per_pt

    return largest_dist

def analysis_All():
    for SIR_name in TEST_PGM:
        for version in GLOB.NUM_VERSIONS[SIR_name]:
            calc_indicators(SIR_name,version)