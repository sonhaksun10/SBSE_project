import csv
import GLOB
import GATool as GA
import numpy as np
import random
import version_evaluation as veval

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
    directoty_hybrid = GLOB.RESULT_DIRECTORY + SIR_name + '_hybrid/'
    data = dict()
    ref_pt = []

    for MOEA in GLOB.TRY_ALGORITHM:
        data_moea = [[] for i in range(GLOB.TRIALS_PER_VERSION)]
        data_hybrid = [[] for i in range(GLOB.TRIALS_PER_VERSION)]
        for i in range(GLOB.TRIALS_PER_VERSION):
            #only MOEA
            fname = 'eval_' + SIR_name + '_version' + str(version + 1) + '_' + MOEA + '_trial' + str(i) + '.csv'
            with open(directory + fname, 'r') as f:
                f.readline()
                rdr = csv.reader(f)
                for line in rdr:
                    for j in range(len(line)):
                        line[j] = float(line[j])
                    gene = GA.Gene_Info(None)
                    gene.set_eval(np.array(line))
                    data_moea[i].append(gene)
                    ref_pt.append(gene)

            #hybrid
            fname = 'eval_' + SIR_name + '_version' + str(version + 1) + '_' + MOEA + '_trial' + str(i) + '.csv'
            with open(directoty_hybrid + fname, 'r') as f:
                f.readline()
                rdr = csv.reader(f)
                for line in rdr:
                    for j in range(len(line)):
                        line[j] = float(line[j])
                    gene = GA.Gene_Info(None)
                    gene.set_eval(np.array(line))
                    data_hybrid[i].append(gene)
                    ref_pt.append(gene)

            ref_pt = GA.get_pareto(ref_pt)[0] #update reference point

        for i in range(len(data_moea)):
            data_moea[i] = GA.get_pareto(data_moea[i])[0]
            for j in range(len(data_moea[i])):
                data_moea[i][j] = data_moea[i][j].get_eval()
        for i in range(len(data_hybrid)):
            data_hybrid[i] = GA.get_pareto(data_hybrid[i])[0]
            for j in range(len(data_hybrid[i])):
                data_hybrid[i][j] = data_hybrid[i][j].get_eval()
        data[MOEA] = data_moea
        data[MOEA + '_hybrid'] = data_hybrid

    for greedy in GLOB.TRY_GALGORITHM:
        data_moea = [[]]
        i = 0
        fname = 'eval_' + SIR_name + '_version' + str(version + 1) + '_' + greedy + '_trial' + str(i) + '.csv'
        with open(directory + fname, 'r') as f:
            f.readline()
            rdr = csv.reader(f)
            for line in rdr:
                for j in range(len(line)):
                    line[j] = float(line[j])
                gene = GA.Gene_Info(None)
                gene.set_eval(np.array(line))
                data_moea[i].append(gene)
                ref_pt.append(gene)

        ref_pt = GA.get_pareto(ref_pt)[0] #update reference point

        for i in range(len(data_moea)):
            data_moea[i] = GA.get_pareto(data_moea[i])[0]
            for j in range(len(data_moea[i])):
                data_moea[i][j] = data_moea[i][j].get_eval()
        data[greedy] = data_moea

    for i in range(len(ref_pt)):
        ref_pt[i] = ref_pt[i].get_eval()

    return data, ref_pt

def write_result(SIR_name, version, result):
    directory = GLOB.RESULT_DIRECTORY
    for MOEA in result.keys():
        res = result[MOEA]
        mean = res.mean(axis=0)
        std = res.std(axis=0)

        fname = SIR_name + '_version' + str(version + 1) + '_' + MOEA + '.csv'
        with open(directory + 'Indicator/' + fname, 'w', newline='') as f:
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
        res_hybrid = []
        hybrid = MOEA + '_hybrid'
        for i in range(GLOB.TRIALS_PER_VERSION):
            #only moea
            HV = get_HV(data[MOEA][i])
            IGD = get_IGD(data[MOEA][i], ref_pt)
            EPSILON = get_EPSILON(data[MOEA][i], ref_pt)
            res_moea.append([EPSILON, HV, IGD])

            #hybrid
            HV = get_HV(data[hybrid][i])
            IGD = get_IGD(data[hybrid][i], ref_pt)
            EPSILON = get_EPSILON(data[hybrid][i], ref_pt)
            res_hybrid.append([EPSILON, HV, IGD])

        res[MOEA] = np.array(res_moea)
        res[hybrid] = np.array(res_hybrid)

    for greedy in GLOB.TRY_GALGORITHM:
        res_greedy = []
        for i in range(1):
            HV = 0
            IGD = get_IGD(data[greedy][i], ref_pt)
            EPSILON = get_EPSILON(data[greedy][i], ref_pt)
            res_greedy.append([EPSILON, HV, IGD])
        res[greedy] = np.array(res_greedy)
    write_result(SIR_name,version,res)

def get_HV(data):
    '''
    Hyper volume of moea solution
    High HV = Diverse pareto front

    all evaluation metric is zero -> do not consider the evaluation metric

    :param data: list(pt)
    :return:     float()
    '''
    HV = 0
    inv_data = []

    for d in data:
        nearest_pt = [0,0,0]
        for invd in inv_data:
            for idx in range(3):
                if d[idx] >= invd[idx] >= nearest_pt[idx]:
                    nearest_pt[idx] = invd[idx]
        HV_add = 1
        diff = d-np.array(nearest_pt)
        for i in range(len(diff)):
            if d[i] > 0.:
                HV_add *= diff[i]
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
    for SIR_name in GLOB.TEST_PGM:
        for version in range(GLOB.NUM_VERSIONS[SIR_name]):
            print('working on:', SIR_name, 'version', version + 1)
            calc_indicators(SIR_name,version)

def get_APFDc():
    #moea and greedy
    for SIR_name in GLOB.TEST_PGM:
        directory = GLOB.RESULT_DIRECTORY + SIR_name + '/'
        for version in range(GLOB.NUM_VERSIONS[SIR_name]):
            evaluator = veval.VEval(SIR_name, version+1, GLOB.NUM_TESTCASES[SIR_name], MOEA = False)
            for MOEA in GLOB.TRY_ALGORITHM + GLOB.TRY_GALGORITHM:
                sequences = []
                APFDc = []
                for i in range(GLOB.TRIALS_PER_VERSION):
                    fname = 'seq_' + SIR_name + '_version' + str(version + 1) + '_' + MOEA + '_trial' + str(i) + '.csv'
                    with open(directory+fname,'r') as f:
                        rdr = csv.reader(f)
                        for line in rdr:
                            for j in range(len(line)):
                                line[j] = int(line[j])
                            sequences.append(line)
                    if MOEA in GLOB.TRY_GALGORITHM:
                        break


                for seq in sequences:
                    APFDc.append(evaluator.eval(seq))

                mean = sum(APFDc)/len(APFDc)
                std = np.array(APFDc).std()
                maximum = max(APFDc)

                fname = 'APFDc_' + SIR_name + '_version' + str(version + 1) + '_' + MOEA + '.csv'
                with open(GLOB.RESULT_DIRECTORY + 'Indicator/' + fname,'w',newline='') as f:
                    wr = csv.writer(f)
                    wr.writerow(['mean','std','max'])
                    wr.writerow([mean,std,maximum])
                    wr.writerow(APFDc)
                print('finish to write', fname)

    #hybrid
    for SIR_name in GLOB.TEST_PGM:
        directory = GLOB.RESULT_DIRECTORY + SIR_name + '_hybrid/'
        for version in range(GLOB.NUM_VERSIONS[SIR_name]):
            evaluator = veval.VEval(SIR_name, version + 1, GLOB.NUM_TESTCASES[SIR_name], MOEA=False)
            for MOEA in GLOB.TRY_ALGORITHM:
                sequences = []
                APFDc = []
                for i in range(GLOB.TRIALS_PER_VERSION):
                    fname = 'seq_' + SIR_name + '_version' + str(version + 1) + '_' + MOEA + '_trial' + str(i) + '.csv'
                    with open(directory + fname, 'r') as f:
                        rdr = csv.reader(f)
                        for line in rdr:
                            for j in range(len(line)):
                                line[j] = int(line[j])
                            sequences.append(line)
                    if MOEA in GLOB.TRY_GALGORITHM:
                        break

                for seq in sequences:
                    APFDc.append(evaluator.eval(seq))

                mean = sum(APFDc) / len(APFDc)
                std = np.array(APFDc).std()
                maximum = max(APFDc)

                fname = 'APFDc_' + SIR_name + '_version' + str(version + 1) + '_' + MOEA + '_hybrid.csv'
                with open(GLOB.RESULT_DIRECTORY + 'Indicator/' + fname, 'w', newline='') as f:
                    wr = csv.writer(f)
                    wr.writerow(['mean', 'std', 'max'])
                    wr.writerow([mean, std, maximum])
                    wr.writerow(APFDc)
                print('finish to write', fname)

def comparision():
    algorithms = GLOB.TRY_GALGORITHM
    for MOEA in GLOB.TRY_ALGORITHM:
        algorithms.append(MOEA)
        algorithms.append(MOEA+'_hybrid')
    num_alg = len(algorithms)
    effect_size_mesaure = dict()
    indicator = ['EPISILON', 'HV', 'IGD', 'APFDc_mean', 'APFDc_max']
    for ind in indicator:
        effect_size_mesaure[ind] = np.zeros([num_alg,num_alg])

    indicator_dir = GLOB.RESULT_DIRECTORY + 'Indicator/'

    #get all effect size measure
    for i in range(num_alg -1):
        for j in range(i+1,num_alg):
            A_wins, B_wins = np.array([0] * len(indicator)), np.array([0] * len(indicator))
            #compare
            for SIR_name in GLOB.TEST_PGM:
                for version in range(GLOB.NUM_VERSIONS[SIR_name]):
                    A_mean, B_mean = None, None
                    #get mean of A
                    fname = SIR_name + '_version' + str(version+1) + '_' + algorithms[i] + '.csv'
                    with open(indicator_dir+fname,'r') as f:
                        rdr = csv.reader(f)
                        cnt = 0
                        for line in rdr:
                            if cnt == 1:
                                for k in range(1, len(line)):
                                    line[k] = float(line[k])
                                A_mean = line[1:]
                                break
                            cnt += 1
                    fname = 'APFDc_' + SIR_name + '_version' + str(version + 1) + '_' + algorithms[i] + '.csv'
                    with open(indicator_dir + fname, 'r') as f:
                        rdr = csv.reader(f)
                        cnt = 0
                        for line in rdr:
                            if cnt == 1:
                                A_mean += [float(line[0]), float(line[2])]
                                break
                            cnt += 1
                    A_mean = np.array(A_mean)

                    # get mean of B
                    fname = SIR_name + '_version' + str(version + 1) + '_' + algorithms[j] + '.csv'
                    with open(indicator_dir + fname, 'r') as f:
                        rdr = csv.reader(f)
                        cnt = 0
                        for line in rdr:
                            if cnt == 1:
                                for k in range(1,len(line)):
                                    line[k] = float(line[k])
                                B_mean = line[1:]
                                break
                            cnt += 1
                    fname = 'APFDc_' + SIR_name + '_version' + str(version + 1) + '_' + algorithms[j] + '.csv'
                    with open(indicator_dir + fname, 'r') as f:
                        rdr = csv.reader(f)
                        cnt = 0
                        for line in rdr:
                            if cnt == 1:
                                B_mean += [float(line[0]), float(line[2])]
                                break
                            cnt += 1
                    B_mean = np.array(B_mean)

                    A_wins = A_wins + (A_mean > B_mean)
                    B_wins = B_wins + (B_mean > A_mean)

            total = A_wins + B_wins
            for k in range(len(A_wins)):
                if total[k] != 0.:
                    effect_size_mesaure[indicator[k]][i][j] = A_wins[k] / total[k]
                    effect_size_mesaure[indicator[k]][j][i] = B_wins[k] / total[k]
                else:
                    effect_size_mesaure[indicator[k]][i][j] = 0.5
                    effect_size_mesaure[indicator[k]][j][i] = 0.5

    #write the effect size measure
    with open(GLOB.RESULT_DIRECTORY + 'effect_size_measure.csv','w') as f:
        wr = csv.writer(f)
        for ind in indicator:
            wr.writerow([ind] + algorithms)
            for i in range(len(algorithms)):
                wr.writerow([algorithms[i]] + list(effect_size_mesaure[ind][i]))
            wr.writerow([''])

#analysis_All()
#get_APFDc()
comparision()