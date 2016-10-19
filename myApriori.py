from collections import Counter, defaultdict
from candidateGen import *
import pdb

def getTransaction(inputfile):
    transaction_set = []
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

    return freqset

if __name__ == "__main__":
    transaction = getTransaction('retail.dat')
    print Apriori(transaction, 0.1)