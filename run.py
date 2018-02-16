import Configurations as conf
import os
from cPickle import load


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


def main():
    borderFiles = os.listdir(conf.bordersFolder)

    for borderFile in borderFiles:
        borderDir = os.path.join(conf.bordersFolder, borderFile)
        borderDict = load(open(borderDir, "rb"))

        fusionInfoFile = borderFile.replace(conf.bordersAppend, conf.fusionInfoAppend)
        fusionInfoDir = os.path.join(conf.fusionInfoFolder, fusionInfoFile)

        fusionDict = readFusionInfo(fusionInfoDir)





if __name__ == '__main__':
    main()
