import pandas as pd
from os import listdir
from os.path import isfile, join
import re
import numpy as np

FOLDERPATH = "C:/users/user/PycharmProjects/AISE/Coverage/V4"
df = pd.DataFrame()
files = [f for f in listdir(FOLDERPATH) if isfile(join(FOLDERPATH, f))]
codeLine= 11000
testNum= 363
s=(testNum,codeLine)
coverageMatrix = np.zeros(s,dtype=int)
testIndex = -1
codeLineIndex = -1

regex_getN=re.compile("^\s*\d*:\s*\d*")


for file in files:
    testIndex += 1
    FILEPATH = FOLDERPATH + "/" + file
    f = open(FILEPATH)
    for line in f.readlines():
        if re.match(regex_getN,line):
            stateNum = re.match(regex_getN, line).group()
            stateNumed = int(stateNum.split(sep=":")[1])
            coverageMatrix[testIndex,stateNumed-1]=1
coverageDf=pd.DataFrame(coverageMatrix)
coverageDf.to_csv(FOLDERPATH+"coverage.csv",index=False)


#
# import pandas as pd
# from os import listdir
# from os.path import isfile, join
# import re
# import numpy as np
#
# FOLDERPATH = "C:/users/user/PycharmProjects/AISE/Coverage/V5"
# df = pd.DataFrame()
# files = [f for f in listdir(FOLDERPATH) if isfile(join(FOLDERPATH, f))]
#
# codeLine= 8000
# testNum= 370
# fileNum= 5
# s=(testNum,codeLine,fileNum)
# coverageMatrix = np.zeros(s,dtype=int)
# testIndex = -1
# codeLineIndex = -1
# fileNum=-1
#
# regex_getN=re.compile("^\w*.c.gcov:\s*\d*:\s*\d*")
#
#
# def getFileIndex(fileName):
#     return({'sed.c.gcov':0, 'regexec.c.gcov':1, 'regex_internal.c.gcov':2, 'regcomp.c.gcov':3,'getline.c.gcov':4}.get(fileName,"default"))
#
#
# for file in files:
#     testIndex += 1
#     FILEPATH = FOLDERPATH + "/" + file
#     f = open(FILEPATH)
#     for line in f.readlines():
#         if re.match(regex_getN,line):
#             stateline = re.match(regex_getN, line).group()
#             fileName = stateline.split(sep=":")[0]
#             stateNumed = int(stateline.split(sep=":")[2])
#             fileIndex=getFileIndex(fileName)
#             coverageMatrix[testIndex,stateNumed-1,fileIndex]=1
#
#
# for i in range(5):
#     coverageDf=pd.DataFrame(coverageMatrix[:,:,i])
#     coverageDf.to_csv(FOLDERPATH+str(i)+"coverage.csv",index=False)
#     i=i+1