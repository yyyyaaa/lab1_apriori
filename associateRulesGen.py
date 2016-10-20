import os
import collections
from candidateGen import *

def getfreqset(inputfile):
    if not os.path.isfile(inputfile):
        print 'File not found'
        return {}

    freqsets = {}

    try:
        with open(inputfile, "rt") as file:
            for line in file:
                freqset = {}
                freqset_string = line.split()

                # Convert string to int
                keyfreqlist = [int(item) for item in freqset_string[1:]]

                if len(keyfreqlist) == 1:
                    freqsets[keyfreqlist[0]] = float(freqset_string[0])
                else:
                    freqsets[tuple(keyfreqlist)] = float(freqset_string[0])

        return freqsets

    except:
        print 'There something wrong when reading file'
        return {}

def genRules(freqsets, k_item=1, minconfidence=0.5):
    if k_item < 1:
        return {}

    k_itemsets = {}

    for key, value in freqsets.iteritems():
        if type(key) != int:
            # Find all itemset
            if k_item == 1:
                k_itemsets[key] = value
            # Find k_itemset
            elif len(key) == k_item:
                k_itemsets[key] = value

    # key: (items), values: [consequence]
    rule_list = collections.defaultdict(list)
    # {items: {consequent: confidence}}
    confidence_score_hash = collections.defaultdict(dict)

    """ First generate all rules with one item in the consequent and output those
    whose conf >= minconf"""
    for itemset, itemsupport in k_itemsets.iteritems():
        consequence_list = []
        for index in range(len(itemset)):
            # items -> consequence
            consequence = itemset[index]
            items = itemset[:index] + itemset[index+1:]
            if len(items) == 1:
                items = items[0]

            # Find confidence
            confidence = float(freqsets[itemset]) / freqsets[items]
            if confidence >= minconfidence:
                rule_list[items].append([consequence])
                confidence_score_hash[items][consequence] = round(confidence, 2)
                consequence_list.append([consequence])

        if consequence_list:
            APGenRules(freqsets, itemset, consequence_list, rule_list, confidence_score_hash, minconfidence)

    return rule_list, confidence_score_hash


def APGenRules(freqsets, itemset, consequence_list, rule_list, confidence_score_hash, minconfidence):
    if len(itemset) > len(consequence_list[0]) + 1:
        # Generate new consequence list
        new_consequence_list = candidateGen(consequence_list)

        # Cannot generate break here
        if not new_consequence_list:
            return

        remove_consequence = []

        # Make associaiton rule based on confidence score
        for consequence in new_consequence_list:
             # items -> consequence
            items = [item for item in itemset
                         if item not in consequence]

            if len(items) == 1:
                items = items[0]
            else:
                items = tuple(items)

            # Calculate confindence
            confidence = float(freqsets[itemset]) / freqsets[items]

            if confidence >= minconfidence:
                # Add new association rule to rule list
                rule_list[items].append(consequence)
                confidence_score_hash[items][tuple(consequence)] = round(confidence, 2)
            else:
                remove_consequence.append(consequence)

        # Remove consequence with association rule smaller than confidence here
        for consequence in remove_consequence:
            new_consequence_list.remove(consequence)

        # Recursively find new association rule
        APGenRules(freqsets, itemset, new_consequence_list, rule_list, confidence_score_hash, minconfidence)

def writeAssociateRule(rule_list, freqsets, confidence_harsh, outputfile):
    try:
        with open(outputfile, "wt") as file:
            for items, consequences in rule_list.iteritems():
                buffer1 = []
                # items -> consequences
                if type(items) == int:
                    buffer1.append(items)
                else:
                    for item in items:
                        buffer1.append(item)
                for consequence in consequences:
                    buffer2 = []
                    for item in consequence:
                        buffer2.append(item)

                    # Calculate confidence
                    if len(consequence) == 1:
                        consequence = consequence[0]
                    else:
                        consequence = tuple(consequence)

                    confidence = confidence_harsh[items][consequence]

                    #Write confidence
                    file.write(str(confidence) + ' ')

                    # Write items
                    for item in buffer1:
                        file.write(str(item) + ' ')
                    file.write('-> ')

                    # Write consequences
                    for item in buffer2:
                        file.write(str(item) + ' ')
                    file.write('\n')

    except:
        print 'Something wrong when writing file'
        return

def userInput():
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    minconf = sys.argv[3]
    k_item = sys.argv[4]

    freqset = getfreqset(inputfile)
    rule, score_harsh = genRules(freqset, int(k_item), float(minconf))
    writeAssociateRule(rule, freqset, score_harsh, outputfile)


if __name__ == "__main__":
    userInput()