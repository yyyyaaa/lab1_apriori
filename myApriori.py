from collections import Counter, defaultdict
import os
from candidateGen import *
import pdb

def getTransaction(inputfile):
    transaction_set = []

    # Check if file exist
    if not os.path.isfile(inputfile):
        print "File not found"
        return []

    try:
        with open(inputfile, 'rt') as file:
            for line in file:
                transaction = line.split()

                # Convert string to int
                item_set = []
                for item in transaction:
                    item_set.append(int(item))
                transaction_set.append(item_set)
        return transaction_set

    except:
        print "Something wrong when reading file"
        return []

def Apriori(transaction_set, minsupport):
    init_set = Counter()
    transaction_len = len(transaction_set)

    # create init itemsets
    for transaction in transaction_set:
        for item in transaction:
            init_set[(item)] += 1

    # Find first frequent set
    first_set = {item: frequency for (item, frequency) in init_set.iteritems()
               if float(init_set[item]) / transaction_len >= minsupport}
    freqset = []
    freqset.append(first_set)

    # Convert list to list of list for matching right parameter
    first_freq = [[item] for item in freqset[-1]]
    current_candidate = candidateGen(first_freq)

    while 1:
        #current_candidate = candidateGen(freqset[-1].keys())#candidateGen([[x] for x in freqset[-1].keys()])
        #pdb.set_trace()
        candidate_dict = Counter()

        for transaction in transaction_set:
            for candidate_item in current_candidate:
                # Find item in transaction
                matches = [item for item in candidate_item if item in transaction]
                if len(matches) == len(candidate_item):
                    candidate_dict[tuple(candidate_item)] += 1

        new_freqset = {item: freq for item, freq in candidate_dict.iteritems()
                        if float(freq)/transaction_len >= minsupport}

        # Remove candidate_dict because new_freqset will iterate through the old items
        del candidate_dict

        # Still have something to generate else break the loop
        if new_freqset:
            freqset.append(new_freqset)

            # Find new candidate
            current_candidate = candidateGen([list(item_set) for item_set in freqset[-1].keys()])
            if current_candidate == []:
                break
        else:
            break

    return freqset, transaction_len

def writeFreqSet(freqsets, transaction_len, outputfile):
    try:
        with open(outputfile, "wt") as file:
            for freqset in freqsets:
                for itemset, value in freqset.iteritems():
                    support = float(value) / transaction_len
                    support = round(support, 2)
                    file.write(str(support) + ' ')

                    if type(itemset) == int:
                        file.write(str(itemset) + ' ')
                    else:
                        for item in itemset:
                            file.write(str(item) + ' ')
                    file.write('\n')

    except:
        print "Something wrong when reading file"
        return


def userInput():
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    minsup = sys.argv[3]

    # Get transaction
    transaction = getTransaction(inputfile)
    if not transaction:
        return

    # Find frequency set with minsup
    freqset, transaction_len = Apriori(transaction, float(minsup))

    # Write result to file
    writeFreqSet(freqset, transaction_len, outputfile)

if __name__ == "__main__":
    userInput()