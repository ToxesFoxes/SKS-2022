from os.path import join, exists, dirname, realpath
from os import makedirs

rootdir = dirname(realpath("__file__"))


def path(fileName):
    return join(rootdir, fileName)


def cityPath(cityName, create=False):
    cityPath = join(rootdir, "result", cityName)
    if create and not exists(cityPath):
        makedirs(cityPath)
    return cityPath


def buildingPath(cityName, buildingName, create=False):
    buildingPath = join(rootdir, "result", cityName, buildingName)
    if create and not exists(buildingPath):
        makedirs(buildingPath)
    return buildingPath

def writeToBuilding(cityName, buildingName, fileName, data):
    with open(join(buildingPath(cityName, buildingName, True), fileName), "w+") as f:
        f.write(data)
        f.close()