import random

def PMX(parent1, parent2):
    size = min(len(parent1), len(parent2))
    p1, p2 = ind1[:], ind2[:]
    child1,child2 = ind1[:],ind2[:]

    print(parent1,p1)
    cut1 = random.randint(0, size - 1)
    cut2 = random.randint(cut1 + 1, size)

    # Apply crossover between cx points
    for i in range(cut1, cut2):
        # Keep track of the selected values
        temp1 = child1[i]
        temp2 = child2[i]
        # Swap the matched value
        child1[i], child1[p1[temp2]] = temp2, temp1
        child2[i], child2[p2[temp1]] = temp1, temp2
        # Position bookkeeping
        p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
        p2[temp1], p2[temp2] = p2[temp2], p2[temp1]

    return child1,child2

ind1, ind2 = [0,1,2,3,4,5], [4,2,0,5,1,3]
res1,res2=PMX(ind1,ind2)
print(ind1,ind2,res1,res2)