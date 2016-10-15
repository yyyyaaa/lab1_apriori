from collections import Counter, defaultdict
from candidateGen import *
import pdb

def getTransaction(inputfile):
    transaction_set = []
    try:
        with open(inputfile, 'rt') as file:
            for line in file:
                transaction = line.split()
                transaction_set.append(transaction)
        return transaction_set

    except:
        print "Something wrong when reading file"
        return []

def Apriori(transaction_set, minsupport):
    init_set = defaultdict(int)
    transaction_count = 0

    # create init itemsets
    for transaction in transaction_set:
        for item in transaction:
            init_set[item] = init_set[item] + 1
            transaction_count += 1

    #find first frequent set
    first_set = {item: frequency for (item, frequency) in init_set.iteritems()
               if float(init_set[item]) / transaction_count >= minsupport}
    freqset = []
    freqset.append(first_set)
    candidate_dict = Counter()


    while len(freqset[-1]) != 0:
        current_candidate = candidateGen([list(x) for x in freqset[-1].keys()])
        pdb.set_trace()
        for transaction in transaction_set:

            for candidate_item in current_candidate:
                if candidate_item in transaction:
                    candidate_dict[tuple(candidate_item)] += 1

        new_freqset = { item: freq for item, freq in candidate_dict.iteritems()
                        if float(freq)/transaction_len >= minsupport }

        freqset.append(new_freqset)

    return freqset

if __name__ == "__main__":
    transaction = getTransaction('retail.dat')
    print len(Apriori(transaction, 0.0001))
