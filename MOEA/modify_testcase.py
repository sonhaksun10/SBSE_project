import numpy as np


def modify_testcase(input_fname, output_fname, sequence, rule=None):
    '''
    use this function before make test.sh file
    This function changes the sequence of test cases

    Some Rules:
    1. Allow duplication of test case -> allow_dup, Default = True
    2. Allow unused test case         -> allow_unused, Default = True

    :param input_fname:     String:     input file name
    :param output_fname:    String:     output file name
    :param sequence:        np.array:   sequence of test case
    :return:                None
    '''
    if rule is None:
        rule = {"allow_dup": True, "allow_unused": True}

    print('sequence:', list(sequence))
    print()

    # read test cases
    testcases = []
    with open(input_fname, 'r') as f:
        lines = f.readlines()
        for line in lines:
            testcases.append(line)

    # error check/ rule check
    testcase_size = len(testcases)
    for seq in sequence:
        if seq >= testcase_size:
            raise Exception('Wrong index: element of sequence should be lower than', testcase_size)
    _rule_check(sequence, testcase_size, rule)

    # write test cases as sequence
    with open(output_fname, 'w') as f:
        for seq in sequence:
            f.write(testcases[seq])


def _rule_check(sequence, tsize, rule):
    if not rule["allow_dup"]:
        if len(sequence) != len(set(sequence)):
            raise Exception('Rule error: duplication of test case')

    if not rule["allow_unused"]:
        if len(set(sequence)) != tsize:
            raise Exception('Rule error: unused test case')


print('test case')
rule = {"allow_dup": True, "allow_unused": True}
modify_testcase('make.tests', 'output.tests', np.random.permutation(110), rule)
