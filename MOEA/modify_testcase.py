import numpy as np

class modify_testcase:
    '''
        This class reads input data and save its data

        use 'modify' function before make test.sh file
        This function changes the sequence of test cases

        Some Rules:
        1. Allow duplication of test case -> allow_dup, Default = True
        2. Allow unused test case         -> allow_unused, Default = True
        Rule can be changed by using change rule
    '''
    def __init__(self, input_fname):
        self.input_fname = input_fname
        self.data = []
        #get data from input file
        with open(input_fname, 'r') as f:
            lines = f.readlines()
            for line in lines:
                self.data.append(line)
        self.datalen = len(self.data)

        self.num_trial = 0 # number of function 'modify' called
        self.rule = {"allow_dup": True, "allow_unused": True}

    def modify(self,sequence):
        #index error check
        for seq in sequence:
            if seq >= self.datalen:
                raise Exception('Wrong index: element of sequence should be lower than', self.datalen)
        self._rule_check(sequence)

        #make output name
        output_fname = 'ouput' + str(self.num_trial) + '.tests'
        self.num_trial += 1

        #write test case
        with open(output_fname, 'w') as f:
            for seq in sequence:
                f.write(self.data[seq])

    def _rule_check(self, sequence):
        if not self.rule["allow_dup"]:
            if len(sequence) != len(set(sequence)):
                raise Exception('Rule error: duplication of test case')

        if not self.rule["allow_unused"]:
            if len(set(sequence)) != self.datalen:
                raise Exception('Rule error: unused test case')

    def change_rule(self,rule):
        for key in rule.keys():
            if key in self.rule:
                if type(self.rule[key]) == type(rule[key]):
                    self.rule[key] = rule[key]
                    print(self.rule)
                else:
                    print('Type is different between two value\nexpected type: ',type(self.rule[key]),
                          '\ngiven type:', type(rule[key]))
            else:
                print('Not allowed rule:', key)




print('test case')
c = modify_testcase('make.tests')
#c.change_rule({"allow_dup": False})
sequence = np.random.permutation(111)
c.modify(sequence)
