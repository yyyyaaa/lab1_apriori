import sys
import os
import itertools
import pdb

def candidateGen(inputfile):
    # Set of new candidate
    candidate_set = []

    # Get frequent itemsets from inputfile
    freqset = getFreqSet(inputfile)
    if freqset == []:
        return []

    # Join step
    for i in range(len(freqset) - 1):
        for j in range(i+1, len(freqset)):
            if cmp(freqset[i][:-1], freqset[j][:-1]) == 0 and freqset[i][-1] != freqset[j][-1]:
                newset = freqset[i] + [freqset[j][-1]]
                candidate_set.append(newset)

                # Prune step
                item_combination = [list(x) for x in itertools.combinations(newset,len(newset) - 1)]
                for item in item_combination:
                    if item not in freqset:
                        candidate_set.remove(newset)
                        break
    return candidate_set

def getFreqSet(inputfile):
    freqset = []
    try:
        with open(inputfile, "rt") as file:
            for line in file:
                transaction = line.split()
                freqset.append(transaction)

        file.close()
        return freqset

    except:
        print "Something wrong when reading file"
        return []


def writeCandidate():
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]

    # Check input file
    if not os.path.isfile(inputfile):
        print "Input file not found"
        return

    # Generate candidate
    candidate_set = candidateGen(inputfile)

    # Write output
    try:
        with open(outputfile, "wt") as file:
            for candidate in candidate_set:
                for item in candidate:
                    file.write(item + ' ')
                file.write('\n')
        file.close()
    except:
        print "Cannot write file"
        return

writeCandidate()
