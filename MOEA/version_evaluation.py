'''
Evaluate 3 kinds of APFDc: APSCc, APDCc, APFDc
'''
import glob
import csv

class VEval:
    def __init__(self,SIR_name, version, test_size):
        self.version = version
        self.test_size = test_size

        self.comp_coverage = []
        self.delta_cov = []
        self.fault_history = []
        self.time_cost = []

        if SIR_name == 'sed':
            self.read_data(SIR_name)


    def read_data(self,SIR_name):
        DIR_name = "../Feature/" + SIR_name + "/"
        version = self.version

        cov = "V" + str(version-1) + "coverage_com.csv"
        delta = "delta_coverage_" + str(version-1) + "_" + str(version) + ".csv"
        fhistory = "fault_history(" + SIR_name + "_v" + str(version) + ").csv"
        timecost = "testcasetTime(v" + str(version-1) + ").txt"

        with open(DIR_name + cov, 'r') as f:
            rdr = csv.reader(f)
            for line in rdr:
                new_line = str2int(line[1:])
                self.comp_coverage.append(new_line)
            self.comp_coverage.pop(0)

        with open(DIR_name + delta, 'r') as f:
            rdr = csv.reader(f)
            for line in rdr:
                if len(line) == 1:
                    self.delta_cov.append([])
                else:
                    new_line = str2int(line[1:])
                    self.delta_cov.append(new_line)
            self.delta_cov.pop(0)

        with open(DIR_name + fhistory, 'r') as f:
            rdr = csv.reader(f)
            for line in rdr:
                new_line = str2int(line[1:])
                self.fault_history.append(new_line)
            self.fault_history.pop(0)

        with open(DIR_name + timecost, 'r') as f:
            for line in f.readlines():
                self.time_cost.append(int(line.split()[1]))

    def eval(self, seq):
        e1 = APFDc(seq,self.comp_coverage,self.time_cost)
        e2 = APFDc(seq,self.delta_cov,self.time_cost)
        e3 = APFDc(seq,self.fault_history,self.time_cost)

        return np.array([e1,e2,e3])

def APFDc(seq, fault_mat, cost):
    num_fault = len(fault_mat[0])
    true_num_fault = 0

    up = 0
    down = 0

    for i in range(num_fault):
        num_fault_add = 0
        up_add = 0
        fault_detected = False
        for j in seq:
            if not fault_detected:
                if fault_mat[j][i] > 0:
                    num_fault_add = fault_mat[j][i]
                    up_add += 0.5*cost[j]
            else:
                up_add += cost[j]

        if not fault_detected:
            num_fault_add = 1

        up += up_add
        true_num_fault += num_fault_add

    down = sum(cost) * true_num_fault
    res = up/down

    return res

def str2int(arr):
    new_arr = []
    for cell in arr:
        try:
            new_arr.append(int(cell))
        except ValueError:
            new_arr.append(cell)
    return new_arr




val = VEval('sed',0,360)