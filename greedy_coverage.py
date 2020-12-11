import argparse
import random
import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt
import csv


class TestCase:
    def __init__(self,num):
        self.testnum=num
        self.cov = []
        self.exectime = 0

    def get_testnum(self):
        return self.testnum

    def set_faultcov(self,faultcov):
        self.faultcov=faultcov

    def get_cov(self):
        return self.cov

    def set_cov(self,statecov):
        self.cov=cov

    def get_exectime(self):
        return self.exectime


def run_greedy(testcase_list,type):
    before_ordering=testcase_list # all the test cases
    after_ordering=[]             # it is like [[first highest possible coverage per time unit], [second~],[]] which is list of list
    while len(before_ordering) > 0:
        order_list=[]
        best_ratio=(0,1) #initialize best_ratio
        cov_list=[0]*len(testcase_list[0].get_cov(type))  #initialize cov_list, at first it is [0,0,0,0,...] if it is covered by some selected cases, 0 ->1 changed
        best_testcase,best_ratio=first_testcase(before_ordering,type) #find first_tescase which covers the most.
        order_list.append(best_testcase)  #add first_case order_list
        before_ordering.remove(best_testcase)  #remove first_case from before_ordering
        cov_list=best_testcase.get_cov(type) #update cov_list
        while not (best_testcase is None):
            (best_testcase,best_ratio,cov_list)=next_testcase(before_ordering,best_ratio,cov_list)
            order_list.append(best_testcase)
            before_ordering.remove(best_testcase)
        after_ordering.append(order_list)     #highest possible coverage is made
    testnum_list=[]
    for test_set in after_ordering:   #make list of order of test case
        for test in test_set:
            testnum_list.append(test.get_testnum())
    return testnum_list

def first_testcase(testcase_list,type):
    best_ratio=0.0
    best_testcase=testcase_list[0]
    for test_case in testcase_list:
        if (test_case.get_cov(type).count(1) / test_case.get_exectime()) > (best_ratio[0]/best_ratio[1]):
            best_ratio=(test_case.get_cov(type).count(1) , test_case.get_exectime())
            best_testcase=test_case
    return (best_testcase,best_ratio)

def next_testcase(testcase_list,best_ratio,cov_list,type):
    best_ratio=best_ratio
    best_testcase=None
    cov_list=cov_list
    for test_case in testcase_list:
        if ((best_ratio[0]+num_cov(cov_list,test_case.get_cov(type))) / (best_ratio[1]+test_case.get_exectime())) > (best_ratio[0]/best_ratio[1]):
            best_ratio=((best_ratio[0]+num_cov(cov_list,test_case.get_cov(type))), (best_ratio[1]+test_case.get_exectime()))
            best_testcase=test_case
    for nth in cov_list:
        if cov_list[nth]==0 and best_testcase.get_cov(type)[nth]==1:
            cov_list[nth]==1
    return (best_testcase,best_ratio,cov_list)

def num_cov(cov_list,testcase_cov):
    subtract_list = [testcase_cov[i] - cov_list[i] for i in range(len(cov_list))] 
    return subtract_list.count(1)


def make_testCase(testcase, type):
    sequence=run_greedy(testcase,type)
    print(sequence)
    #make output name
    output_fname = 'ouput_greedy_' + type + '.tests'

    #write test case
    with open(output_fname, 'w') as f:
        for seq in sequence:
            f.write(seq)
    return output_fname


parser = argparse.ArgumentParser(description="")
parser.add_argument('file', type=str, metavar="PATH", help="Path coverage file")
parser.add_argument('file2', type=str, metavar="PATH", help="Path execution time file")
args = parser.parse_args()
covfile = args.file
execfile = args.file2
cov_list=[]
exec_time=[]
with open(covfile, 'r') as f:
  lines = f.readlines()
  lines = lines[1:]
  for line in lines:
    line = line.strip()
    line = line.split(",")
    slice=line[1:len(line)]
    slice = [ int(x) for x in slice ]
    cov_list.append(slice)

with open(execfile, 'r') as f:
    for line in f.readlines():
        exec_time.append(int(line.split()[1]))

testcase=[]
for i in range(len(cov_list)):
    temp=TestCase(i)
    temp.set_cov(cov_list[i])
    temp.set_exectime(exec_time[i])
    testcase.append(temp)

make_testCase(testcase,type)
