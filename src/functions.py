
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


