from multiprocessing import Process
import os
import NSGA2
import TAEA
import SPEA2
import GLOB
import csv

def write_file(MOEA,SIR_name,version,result):
    directory = GLOB.RESULT_DIRECTORY + SIR_name + '/'

    for i in range(len(result)):
        res = result[i]
        fname = 'seq_' + SIR_name + '_version' + str(version) + '_' + MOEA + '_trial' + str(i) + '.csv'
        with open(directory + fname, 'w', newline='') as f:
            wr = csv.writer(f)
            for gene in res:
                wr.writerow(list(gene.get_seq()))

        fname = 'eval_' + SIR_name + '_version' + str(version) + '_' + MOEA +  '_trial' + str(i) + '.csv'
        with open(directory + fname, 'w', newline='') as f:
            wr = csv.writer(f)
            wr.writerow(['coverage','delta-coverage','fault-history'])
            for gene in res:
                wr.writerow(list(gene.get_eval()))


def run_MOEA(MOEA,SIR_name,version):
    result = []
    num_testcases = GLOB.NUM_TESTCASES[SIR_name]
    for i in range(GLOB.TRIALS_PER_VERSION):
        print('child process:', SIR_name, 'version', version, '_', MOEA, ': trial', i)
        if MOEA == 'NSGA2':
            res = NSGA2.run_NSGA2(SIR_name,version,num_testcases)
            result.append(res)
        elif MOEA == 'SPEA2':
            res = SPEA2.run_SPEA2(SIR_name,version,num_testcases)
            result.append(res)
        elif MOEA == 'TAEA':
            res = TAEA.run_TAEA(SIR_name,version,num_testcases)
            result.append(res)

    write_file(MOEA, SIR_name, version, result)
    print('child process:', SIR_name, 'version', version, '_', MOEA, '-> finished')


if __name__ == '__main__':
    process = []
    if GLOB.MULTI_PROCESS:
        for SIR_name in GLOB.TEST_PGM:
            for i in range(1, GLOB.NUM_VERSIONS[SIR_name] + 1):
                for MOEA in GLOB.TRY_ALGORITHM:
                    process.append(Process(target=run_MOEA, args=(MOEA, SIR_name, i)))
                    print("process ready:", SIR_name, 'version', i, '_', MOEA)

        cpu_size = os.cpu_count()
        running_cores = max(1,cpu_size-5)


        for i in range(len(process)//running_cores):
            for j in range(running_cores):
                p = process[running_cores*i+j]
                p.start()
            for j in range(running_cores):
                p = process[running_cores*i+j]
                p.join()

        for i in range(len(process) % running_cores):
            p = process[-i-1]
            p.start()
        for i in range(len(process) % running_cores):
            p = process[-i - 1]
            p.join()

        print('finish calculation')
    else:
         run_MOEA('TAEA', 'grep', 2)
