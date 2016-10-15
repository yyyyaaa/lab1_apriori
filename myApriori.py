import collections

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
    init_set = collections.defaultdict(lambda: 0)

    # create init itemsets
    for transaction in transaction_set:
        for item in transaction:
            init_set[item] = init_set[item] + 1


    #find first frequent set
    transaction_len = len(transaction_set)
    first_set = {item: frequency for (item, frequency) in init_set.iteritems()
               if float(init_set[item]) / transaction_len >= minsupport}
    freqset = []
    freqset.append(first_set)

    while len(freqset[-1]) != 0:
        pass

    return init_set

def candidateGen(freqset):
    # Set of new candidate
    candidate_set = []

    # Join step
    keylist = freqset.keys()
    for i in range(len(keylist) - 1):
        for j in range(i + 1, len(freqset)):
            item1 = freqset[i]
            item2 = freqset[j]
            if cmp(item1[:-1], item2[:-2]) == 0 and item1[-1] != item2[-1]:
                newset = item1

#transaction = getTransaction('retail.dat')
#print len(Apriori(transaction, 0.0001))


set = {i:i + 1 for i in range(1, 11)}
setb = {a: b for a, b in set.iteritems()
        if set[a] >= 8}
setc = []
setc.append(set)
setc.append({})
if not setc[-1]:
    print 'fsdfsd'
print setc

key = set.keys()
print key
