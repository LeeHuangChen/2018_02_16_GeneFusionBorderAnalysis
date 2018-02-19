from collections import Counter

def readFamilyProteinName(name):
    family = name.split("_")[0][1:]
    return int(family)


def readFusedProteinName(name):
    arr = name.split("_")
    #         0  1  2  3  4  5 6 7 8       9   10    11
    # format: ID_53_F1_16_F2_0_G_4_SplitPt_249_GenID_0
    id = int(arr[1])
    f1 = int(arr[3])
    f2 = int(arr[5])
    gen = int(arr[7])
    splitP = int(arr[9])

    return id, f1, f2, splitP


# compares the split points of each border definition and returns
# avgDist, wrongNumBordersOnSplitProt,  multBorderOnFamilyProtein
def compareSplitPoints(borderDict):
    # analysis variables
    multBorderOnFamilyProtein = 0
    wrongNumBordersOnSplitProt = 0
    numFusedProteins = 0
    sumDist = 0

    # go through every protein
    for protName in borderDict.keys():
        arr = protName.split("_")

        # if this is a family protein
        if len(arr) == 2:
            # if there are too many border definitions
            if len(borderDict[protName]) > 1:
                multBorderOnFamilyProtein += 1
        # if this is a fused protein
        elif len(arr) > 2:
            numFusedProteins += 1
            # if there are wrong numbers of border on a fused protein
            if len(borderDict[protName]) != 2:
                wrongNumBordersOnSplitProt += 1

            id, f1, f2, splitP = readFusedProteinName(protName)

            # add how far each border is to the split point
            for border in borderDict[protName]:
                s = border[1]
                e = border[2]

                minDist = min(abs(s-splitP), abs(e-splitP))

                sumDist += minDist

    avgDist = sumDist/float(numFusedProteins)

    return avgDist, wrongNumBordersOnSplitProt,  multBorderOnFamilyProtein


def identifyFamilyProteinMappings(borderDict):
    # organize all the family mappings
    familyMappingDict = {}
    # identify the family proteins
    for protName in borderDict.keys():
        arr = protName.split("_")

        # if this is a family protein
        if len(arr) == 2:
            orgFamily = readFamilyProteinName(protName)

            borders = borderDict[protName]

            testFamily = -1

            # there is only one border (the expected case)
            if len(borders) == 1:
                testFamily = int(borders[0][0])
            # if there are multiple borders, take the largest border
            elif len(borders) >1:
                maxLen = 0
                maxIndx = 0
                for i, border in enumerate(borders):
                    length = int(border[2])-int(border[1])
                    if length > maxLen:
                        maxLen = length
                        maxIndx = i
                testFamily = borders[maxIndx][0]

            # add the mapping to the family mapping dict
            if orgFamily in familyMappingDict.keys():
                familyMappingDict[orgFamily].append(testFamily)
            else:
                familyMappingDict[orgFamily] = [testFamily]

    # summarize the family mappings
    familyMappingSummaryDict = {}
    for orgFamily in familyMappingDict:
        families = familyMappingDict[orgFamily]
        familyMode, numOccur = Counter(families).most_common()[0]
        confidence = float(numOccur)/len(families)
        familyMappingSummaryDict[orgFamily] = [familyMode, confidence]

    return familyMappingSummaryDict


def findClosestBorder(targetBorder, borders):
    mindist = 100000000000
    minIndex = -1
    for i, border in enumerate(borders):
        dist = abs(border[1]-targetBorder[1])+abs(border[2]-targetBorder[2])
        if dist<mindist:
            mindist = dist
            minIndex = i

    return borders[minIndex]


def checkFusedProteins(borderDict, familySummaryDict, protLenDict):
    correctMappings = []
    incorrectMappings = []

    # identify the family proteins
    for protName in borderDict.keys():
        arr = protName.split("_")

        # if this is a fused protein
        if len(arr) > 2:
            id, f1, f2, splitP = readFusedProteinName(protName)

            borders = borderDict[protName]
            targetBorder1 = [f1, 0, splitP]
            targetBorder2 = [f2, splitP, protLenDict[protName]]
            closeBorder1 = findClosestBorder(targetBorder1, borders)
            closeBorder2 = findClosestBorder(targetBorder2, borders)
            moduleLabel1 = closeBorder1[0]
            moduleLabel2 = closeBorder2[0]

            module1, confidence1 = familySummaryDict[f1]
            module2, confidence2 = familySummaryDict[f2]

            if moduleLabel1 == module1:
                correctMappings.append(confidence1)
            else:
                incorrectMappings.append(confidence1)

            if moduleLabel2 == module2:
                correctMappings.append(confidence2)
            else:
                incorrectMappings.append(confidence2)

    return correctMappings, incorrectMappings


def checkBorderDefinitions(borderDict, protLenDict):
    familySummaryDict = identifyFamilyProteinMappings(borderDict)
    correctMappings, incorrectMappings = checkFusedProteins(borderDict, familySummaryDict, protLenDict)
    print "\nC:", len(correctMappings), ":", reduce(lambda x, y: x + y, correctMappings) / len(correctMappings)
    print "I:", len(incorrectMappings), ":", reduce(lambda x, y: x + y, incorrectMappings) / len(incorrectMappings)


