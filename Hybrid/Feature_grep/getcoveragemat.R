library(dplyr)#processing dataframe 
rm(list=ls())
a=read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V0coverage_com.csv")

compression_max<-function(fileName){
  coverage = read.csv(fileName)
  coverage_com = coverage %>% select_if(function(x) sum(x)>0)
  print(i)
  i=1
  while(i<ncol(coverage_com)){
    cc=coverage_com[,i]
    for(j in (i+1):ncol(coverage_com)){
      if(j>ncol(coverage_com)){
        break
      }
      if(all(cc==coverage_com[,j])){
        coverage_com[,i]=coverage_com[,i]+cc
        coverage_com[,j]=0
      }
    }
    coverage_com = coverage_com %>% select_if(function(x) sum(x)>0)
    i=i+1
  }
  com_fileName = sub('coverage','coverage_com',fileName)
  write.csv(coverage_com,com_fileName)
}

coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V5coverage0.csv")

compression_max("C:/users/user/PycharmProjects/AISE/Coverage/V0coverage.csv")
compression_max("C:/users/user/PycharmProjects/AISE/Coverage/V1coverage.csv")
compression_max("C:/users/user/PycharmProjects/AISE/Coverage/V2coverage.csv")
compression_max("C:/users/user/PycharmProjects/AISE/Coverage/V3coverage.csv")
compression_max("C:/users/user/PycharmProjects/AISE/Coverage/V4coverage.csv")
compression_max("C:/users/user/PycharmProjects/AISE/Coverage/V5coverage0.csv")
compression_max("C:/users/user/PycharmProjects/AISE/Coverage/V5coverage1.csv")
compression_max("C:/users/user/PycharmProjects/AISE/Coverage/V5coverage2.csv")
compression_max("C:/users/user/PycharmProjects/AISE/Coverage/V5coverage3.csv")
compression_max("C:/users/user/PycharmProjects/AISE/Coverage/V5coverage4.csv")
compression_max("C:/users/user/PycharmProjects/AISE/Coverage/V6coverage0.csv")
compression_max("C:/users/user/PycharmProjects/AISE/Coverage/V6coverage1.csv")
compression_max("C:/users/user/PycharmProjects/AISE/Coverage/V6coverage2.csv")
compression_max("C:/users/user/PycharmProjects/AISE/Coverage/V6coverage3.csv")
compression_max("C:/users/user/PycharmProjects/AISE/Coverage/V6coverage4.csv")


coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V0coverage.csv")
coverage_com = coverage %>% select_if(function(x) sum(x)>0)
write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V0coverage_remove0.csv")

i=1
while(i<ncol(coverage_com)){
  cc=coverage_com[,i]
  for(j in (i+1):ncol(coverage_com)){
    if(j>ncol(coverage_com)){
      break
    }
    if(all(cc==coverage_com[,j])){
      coverage_com[,i]=coverage_com[,i]+cc
      coverage_com[,j]=0
    }
  }
  coverage_com = coverage_com %>% select_if(function(x) sum(x)>0)
  i=i+1
}

write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V0coverage_com.csv")



coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V1coverage.csv")
coverage_com = coverage %>% select_if(function(x) sum(x)>0)
write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V1coverage_remove0.csv")

i=1
while(i<ncol(coverage_com)){
  cc=coverage_com[,i]
  for(j in (i+1):ncol(coverage_com)){
    if(j>ncol(coverage_com)){
      break
    }
    if(all(cc==coverage_com[,j])){
      coverage_com[,i]=coverage_com[,i]+cc
      coverage_com[,j]=0
    }
  }
  coverage_com = coverage_com %>% select_if(function(x) sum(x)>0)
  i=i+1
}

write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V1coverage_com.csv")



coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V2coverage.csv")
coverage_com = coverage %>% select_if(function(x) sum(x)>0)
write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V2coverage_remove0.csv")


i=1
while(i<ncol(coverage_com)){
  cc=coverage_com[,i]
  for(j in (i+1):ncol(coverage_com)){
    if(j>ncol(coverage_com)){
      break
    }
    if(all(cc==coverage_com[,j])){
      coverage_com[,i]=coverage_com[,i]+cc
      coverage_com[,j]=0
    }
  }
  coverage_com = coverage_com %>% select_if(function(x) sum(x)>0)
  i=i+1
}

write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V2coverage_com.csv")




coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V3coverage.csv")
coverage_com = coverage %>% select_if(function(x) sum(x)>0)
write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V3coverage_remove0.csv")


i=1
while(i<ncol(coverage_com)){
  cc=coverage_com[,i]
  for(j in (i+1):ncol(coverage_com)){
    if(j>ncol(coverage_com)){
      break
    }
    if(all(cc==coverage_com[,j])){
      coverage_com[,i]=coverage_com[,i]+cc
      coverage_com[,j]=0
    }
  }
  coverage_com = coverage_com %>% select_if(function(x) sum(x)>0)
  i=i+1
}

write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V3coverage_com.csv")





coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V4coverage.csv")
coverage_com = coverage %>% select_if(function(x) sum(x)>0)
write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V4coverage_remove0.csv")


i=1
while(i<ncol(coverage_com)){
  cc=coverage_com[,i]
  for(j in (i+1):ncol(coverage_com)){
    if(j>ncol(coverage_com)){
      break
    }
    if(all(cc==coverage_com[,j])){
      coverage_com[,i]=coverage_com[,i]+cc
      coverage_com[,j]=0
    }
  }
  coverage_com = coverage_com %>% select_if(function(x) sum(x)>0)
  i=i+1
}

write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V4coverage_com.csv")




coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V5coverage0.csv")
coverage_com = coverage %>% select_if(function(x) sum(x)>0)
write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V5coverage_remove0.csv")

i=1
while(i<ncol(coverage_com)){
  cc=coverage_com[,i]
  for(j in (i+1):ncol(coverage_com)){
    if(j>ncol(coverage_com)){
      break
    }
    if(all(cc==coverage_com[,j])){
      coverage_com[,i]=coverage_com[,i]+cc
      coverage_com[,j]=0
    }
  }
  coverage_com = coverage_com %>% select_if(function(x) sum(x)>0)
  i=i+1
}

write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V5coverage_com0.csv")



coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V5coverage1.csv")
coverage_com = coverage %>% select_if(function(x) sum(x)>0)
write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V5coverage_remove1.csv")


i=1
while(i<ncol(coverage_com)){
  cc=coverage_com[,i]
  for(j in (i+1):ncol(coverage_com)){
    if(j>ncol(coverage_com)){
      break
    }
    if(all(cc==coverage_com[,j])){
      coverage_com[,i]=coverage_com[,i]+cc
      coverage_com[,j]=0
    }
  }
  coverage_com = coverage_com %>% select_if(function(x) sum(x)>0)
  i=i+1
}

write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V5coverage_com1.csv")




coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V5coverage2.csv")
coverage_com = coverage %>% select_if(function(x) sum(x)>0)
write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V5coverage_remove2.csv")



i=1
while(i<ncol(coverage_com)){
  cc=coverage_com[,i]
  for(j in (i+1):ncol(coverage_com)){
    if(j>ncol(coverage_com)){
      break
    }
    if(all(cc==coverage_com[,j])){
      coverage_com[,i]=coverage_com[,i]+cc
      coverage_com[,j]=0
    }
  }
  coverage_com = coverage_com %>% select_if(function(x) sum(x)>0)
  i=i+1
}

write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V5coverage_com2.csv")




coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V5coverage3.csv")
coverage_com = coverage %>% select_if(function(x) sum(x)>0)
write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V5coverage_remove3.csv")



i=1
while(i<ncol(coverage_com)){
  cc=coverage_com[,i]
  for(j in (i+1):ncol(coverage_com)){
    if(j>ncol(coverage_com)){
      break
    }
    if(all(cc==coverage_com[,j])){
      coverage_com[,i]=coverage_com[,i]+cc
      coverage_com[,j]=0
    }
  }
  coverage_com = coverage_com %>% select_if(function(x) sum(x)>0)
  i=i+1
}

write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V5coverage_com3.csv")


coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V5coverage4.csv")
coverage_com = coverage %>% select_if(function(x) sum(x)>0)
write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V5coverage_remove4.csv")


i=1
while(i<ncol(coverage_com)){
  cc=coverage_com[,i]
  for(j in (i+1):ncol(coverage_com)){
    if(j>ncol(coverage_com)){
      break
    }
    if(all(cc==coverage_com[,j])){
      coverage_com[,i]=coverage_com[,i]+cc
      coverage_com[,j]=0
    }
  }
  coverage_com = coverage_com %>% select_if(function(x) sum(x)>0)
  i=i+1
}

write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V5coverage_com4.csv")






coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V6coverage0.csv")
coverage_com = coverage %>% select_if(function(x) sum(x)>0)
write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V6coverage_remove0.csv")

i=1
while(i<ncol(coverage_com)){
  cc=coverage_com[,i]
  for(j in (i+1):ncol(coverage_com)){
    if(j>ncol(coverage_com)){
      break
    }
    if(all(cc==coverage_com[,j])){
      coverage_com[,i]=coverage_com[,i]+cc
      coverage_com[,j]=0
    }
  }
  coverage_com = coverage_com %>% select_if(function(x) sum(x)>0)
  i=i+1
}

write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V6coverage_com0.csv")



coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V6coverage1.csv")
coverage_com = coverage %>% select_if(function(x) sum(x)>0)

i=1
while(i<ncol(coverage_com)){
  cc=coverage_com[,i]
  for(j in (i+1):ncol(coverage_com)){
    if(j>ncol(coverage_com)){
      break
    }
    if(all(cc==coverage_com[,j])){
      coverage_com[,i]=coverage_com[,i]+cc
      coverage_com[,j]=0
    }
  }
  coverage_com = coverage_com %>% select_if(function(x) sum(x)>0)
  i=i+1
}

write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V6coverage_com1.csv")



coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V6coverage2.csv")
coverage_com = coverage %>% select_if(function(x) sum(x)>0)

i=1
while(i<ncol(coverage_com)){
  cc=coverage_com[,i]
  for(j in (i+1):ncol(coverage_com)){
    if(j>ncol(coverage_com)){
      break
    }
    if(all(cc==coverage_com[,j])){
      coverage_com[,i]=coverage_com[,i]+cc
      coverage_com[,j]=0
    }
  }
  coverage_com = coverage_com %>% select_if(function(x) sum(x)>0)
  i=i+1
}

write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V6coverage_com2.csv")




coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V6coverage3.csv")
coverage_com = coverage %>% select_if(function(x) sum(x)>0)

i=1
while(i<ncol(coverage_com)){
  cc=coverage_com[,i]
  for(j in (i+1):ncol(coverage_com)){
    if(j>ncol(coverage_com)){
      break
    }
    if(all(cc==coverage_com[,j])){
      coverage_com[,i]=coverage_com[,i]+cc
      coverage_com[,j]=0
    }
  }
  coverage_com = coverage_com %>% select_if(function(x) sum(x)>0)
  i=i+1
}

write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V6coverage_com3.csv")


coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V6coverage4.csv")
coverage_com = coverage %>% select_if(function(x) sum(x)>0)

i=1
while(i<ncol(coverage_com)){
  cc=coverage_com[,i]
  for(j in (i+1):ncol(coverage_com)){
    if(j>ncol(coverage_com)){
      break
    }
    if(all(cc==coverage_com[,j])){
      coverage_com[,i]=coverage_com[,i]+cc
      coverage_com[,j]=0
    }
  }
  coverage_com = coverage_com %>% select_if(function(x) sum(x)>0)
  i=i+1
}

write.csv(coverage_com,"C:/users/user/PycharmProjects/AISE/Coverage/V6coverage_com4.csv")





#############################################################################################
coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V0coverage_remove0.csv")
coverage = coverage[,-1]



lines=as.character(readLines("C:/users/user/PycharmProjects/AISE/code diff/changeline_0_1"))
diff_line_num=unlist(strsplit(lines,split=" "))


for(i in 1:length(diff_line_num)){
  line_num=diff_line_num[i]
  col_name=paste('X',line_num,sep="")
  print(col_name)
  if(!(col_name %in% colnames(coverage))){
    print('del')
    diff_line_num=diff_line_num[-i]
  }else{
    next
  }
}

num_test = nrow(coverage)
num_change_line = length(diff_line_num)
delta_coverage=data.frame(matrix(ncol=num_change_line,nrow=num_test))

colnames(delta_coverage)=diff_line_num


for(line_num in diff_line_num){
  col_name=paste('X',line_num,sep="")
  print(col_name)
    for(testcase in 1:num_test){
      if(coverage[testcase,col_name]==1){
        delta_coverage[testcase,line_num]=1
    }else{
      delta_coverage[testcase,line_num]=0
    }        
  }      
}


write.csv(delta_coverage,"C:/users/user/PycharmProjects/AISE/code diff//delta_coverage_0_1.csv")


#####################################################################################################

coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V1coverage_remove0.csv")
coverage = coverage[,-1]


lines=as.character(readLines("C:/users/user/PycharmProjects/AISE/code diff/changeline_1_2"))
diff_line_num=unlist(strsplit(lines,split=" "))

i=1
while(i <= length(diff_line_num)){
  line_num=diff_line_num[i]
  col_name=paste('X',line_num,sep="")
  if(!(col_name %in% colnames(coverage))){
    diff_line_num=diff_line_num[-i]
    print(col_name)
  }else{
    i=i+1
    next
  }
}

num_test = nrow(coverage)
num_change_line = length(diff_line_num)
delta_coverage=data.frame(matrix(ncol=num_change_line,nrow=num_test))

colnames(delta_coverage)=diff_line_num


for(line_num in diff_line_num){
  col_name=paste('X',line_num,sep="")
  for(testcase in 1:num_test){
    if(coverage[testcase,col_name]==1){
      delta_coverage[testcase,line_num]=1
    }else{
      delta_coverage[testcase,line_num]=0
    }        
  }      
}


write.csv(delta_coverage,"C:/users/user/PycharmProjects/AISE/code diff//delta_coverage_1_2.csv")



#####################################################################################################

coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V2coverage_remove0.csv")
coverage = coverage[,-1]


lines=as.character(readLines("C:/users/user/PycharmProjects/AISE/code diff/changeline_2_3"))
diff_line_num=unlist(strsplit(lines,split=" "))

i=1
while(i <= length(diff_line_num)){
  line_num=diff_line_num[i]
  col_name=paste('X',line_num,sep="")
  if(!(col_name %in% colnames(coverage))){
    diff_line_num=diff_line_num[-i]
    print(col_name)
  }else{
    i=i+1
    next
  }
}

num_test = nrow(coverage)
num_change_line = length(diff_line_num)
delta_coverage=data.frame(matrix(ncol=num_change_line,nrow=num_test))

colnames(delta_coverage)=diff_line_num


for(line_num in diff_line_num){
  col_name=paste('X',line_num,sep="")
  for(testcase in 1:num_test){
    if(coverage[testcase,col_name]==1){
      delta_coverage[testcase,line_num]=1
    }else{
      delta_coverage[testcase,line_num]=0
    }        
  }      
}


write.csv(delta_coverage,"C:/users/user/PycharmProjects/AISE/code diff//delta_coverage_2_3.csv")



#####################################################################################################

coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V3coverage_remove0.csv")
coverage = coverage[,-1]


lines=as.character(readLines("C:/users/user/PycharmProjects/AISE/code diff/changeline_3_4"))
diff_line_num=unlist(strsplit(lines,split=" "))

i=1
while(i <= length(diff_line_num)){
  line_num=diff_line_num[i]
  col_name=paste('X',line_num,sep="")
  if(!(col_name %in% colnames(coverage))){
    diff_line_num=diff_line_num[-i]
    print(col_name)
  }else{
    i=i+1
    next
  }
}

num_test = nrow(coverage)
num_change_line = length(diff_line_num)
delta_coverage=data.frame(matrix(ncol=num_change_line,nrow=num_test))

colnames(delta_coverage)=diff_line_num


for(line_num in diff_line_num){
  col_name=paste('X',line_num,sep="")
  for(testcase in 1:num_test){
    if(coverage[testcase,col_name]==1){
      delta_coverage[testcase,line_num]=1
    }else{
      delta_coverage[testcase,line_num]=0
    }        
  }      
}


write.csv(delta_coverage,"C:/users/user/PycharmProjects/AISE/code diff//delta_coverage_3_4.csv")



#####################################################################################################

coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V4coverage_remove0.csv")
coverage = coverage[,-1]


lines=as.character(readLines("C:/users/user/PycharmProjects/AISE/code diff/changeline_4_5"))
diff_line_num=unlist(strsplit(lines,split=" "))

i=1
while(i <= length(diff_line_num)){
  line_num=diff_line_num[i]
  col_name=paste('X',line_num,sep="")
  if(!(col_name %in% colnames(coverage))){
    diff_line_num=diff_line_num[-i]
    print(col_name)
  }else{
    i=i+1
    next
  }
}

num_test = nrow(coverage)
num_change_line = length(diff_line_num)
delta_coverage=data.frame(matrix(ncol=num_change_line,nrow=num_test))

colnames(delta_coverage)=diff_line_num


for(line_num in diff_line_num){
  col_name=paste('X',line_num,sep="")
  for(testcase in 1:num_test){
    if(coverage[testcase,col_name]==1){
      delta_coverage[testcase,line_num]=1
    }else{
      delta_coverage[testcase,line_num]=0
    }        
  }      
}


write.csv(delta_coverage,"C:/users/user/PycharmProjects/AISE/code diff//delta_coverage_4_5.csv")



#####################################################################################################

coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V5coverage_remove0.csv")
coverage = coverage[,-1]


lines=as.character(readLines("C:/users/user/PycharmProjects/AISE/code diff/changeline_5_6"))
diff_line_num=unlist(strsplit(lines,split=" "))

i=1
while(i <= length(diff_line_num)){
  line_num=diff_line_num[i]
  col_name=paste('X',line_num,sep="")
  if(!(col_name %in% colnames(coverage))){
    diff_line_num=diff_line_num[-i]
    print(col_name)
  }else{
    i=i+1
    next
  }
}

num_test = nrow(coverage)
num_change_line = length(diff_line_num)
delta_coverage=data.frame(matrix(ncol=num_change_line,nrow=num_test))

colnames(delta_coverage)=diff_line_num


for(line_num in diff_line_num){
  col_name=paste('X',line_num,sep="")
  for(testcase in 1:num_test){
    if(coverage[testcase,col_name]==1){
      delta_coverage[testcase,line_num]=1
    }else{
      delta_coverage[testcase,line_num]=0
    }        
  }      
}


write.csv(delta_coverage,"C:/users/user/PycharmProjects/AISE/code diff//delta_coverage_5_6.csv")

#####################################################################################################

coverage = read.csv("C:/users/user/PycharmProjects/AISE/Coverage/V6coverage_remove0.csv")
coverage = coverage[,-1]


lines=as.character(readLines("C:/users/user/PycharmProjects/AISE/code diff/changeline_6_7"))
diff_line_num=unlist(strsplit(lines,split=" "))

i=1
while(i <= length(diff_line_num)){
  line_num=diff_line_num[i]
  col_name=paste('X',line_num,sep="")
  if(!(col_name %in% colnames(coverage))){
    diff_line_num=diff_line_num[-i]
    print(col_name)
  }else{
    i=i+1
    next
  }
}

num_test = nrow(coverage)
num_change_line = length(diff_line_num)
delta_coverage=data.frame(matrix(ncol=num_change_line,nrow=num_test))

colnames(delta_coverage)=diff_line_num


for(line_num in diff_line_num){
  col_name=paste('X',line_num,sep="")
  for(testcase in 1:num_test){
    if(coverage[testcase,col_name]==1){
      delta_coverage[testcase,line_num]=1
    }else{
      delta_coverage[testcase,line_num]=0
    }        
  }      
}


write.csv(delta_coverage,"C:/users/user/PycharmProjects/AISE/code diff//delta_coverage_6_7.csv")



