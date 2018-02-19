import Configurations as conf
import os
from cPickle import load
from src import functions as func, util


# converts the text information on fusion InfoDir to a dictionary
# format:
#   Dict:
#       Key: Event number
#       Val: List[evnt, fam1, fam2, gen, spliceLoc]
def readFusionInfo(fusionInfoDir):
    fusionDict = {}
    with open(fusionInfoDir) as f:
        for i, line in enumerate(f):
            # first two lines are header lines
            if i > 2:
                arr = line.split("\t")
                evnt = int(arr[0])
                fusionDict[evnt] = [int(arr[0]), int(arr[1]), int(arr[2]), int(arr[3]), int(arr[4])]
    return fusionDict


def compareSplitPoints():
    borderFiles = os.listdir(conf.bordersFolder)

    util.generateDirectories(conf.resultFolder)
    with open(conf.splitResultFile, "w") as resultFile:
        resultFile.write("testcase\tavgDist\twrongNumBordersOnSplitProt\tmultBorderOnFamilyProtein\n")
        for borderFile in borderFiles:
            borderDir = os.path.join(conf.bordersFolder, borderFile)
            borderDict = load(open(borderDir, "rb"))

            # fusionInfoFile = borderFile.replace(conf.bordersAppend, conf.fusionInfoAppend)
            # fusionInfoDir = os.path.join(conf.fusionInfoFolder, fusionInfoFile)
            #
            # fusionDict = readFusionInfo(fusionInfoDir)

            avgDist, wrongNumBordersOnSplitProt, multBorderOnFamilyProtein = func.compareSplitPoints(borderDict)

            testcase = borderFile.replace(conf.bordersAppend, "")
            resultFile.write(testcase+"\t"+str(avgDist)+"\t"+str(wrongNumBordersOnSplitProt)+"\t" +
                             str(multBorderOnFamilyProtein)+"\n")


def checkBorders():
    borderFiles = os.listdir(conf.bordersFolder)
    for borderFile in borderFiles:
        borderDir = os.path.join(conf.bordersFolder, borderFile)
        borderDict = load(open(borderDir, "rb"))

        protLenFile = borderFile.replace(conf.bordersAppend, conf.protLenAppend)
        protLenDir = os.path.join(conf.protLenFolder, protLenFile)
        protLenDict = load(open(protLenDir, "rb"))

        func.checkBorderDefinitions(borderDict, protLenDict)


def main():
    #compareSplitPoints()
    checkBorders()


if __name__ == '__main__':
    main()
