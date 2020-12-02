import pandas as pd
import os
import re

cwd = os.getcwd()
file_path = os.path.join(cwd,"fault_history(sed_v7).txt")
df = pd.DataFrame()
f = open(file_path)

col=-1
row=-1
regex_tc=re.compile("^unitest")
regex_f=re.compile("^v")
line_num = 1


for line in f.readlines():
    if line_num == 1:
        TC_NUM = int(line)
        line_num += 1
        continue
    elif line_num == 2:
        F_NUM = int(line)
        temp_df = [[0 for col in range(F_NUM)] for row in range(TC_NUM)]
        line_num += 1
        continue
    else:
        if re.match(regex_tc,line):
            col=col+1
            row=-1
        elif re.match(regex_f, line):
            row=row+1
        else:
            try :
                temp_df[col][row]=int(line)
            except IndexError:
                print(col,row)

df=pd.DataFrame(temp_df)
print(df)
df.to_csv("fault_history(sed_v7).csv")