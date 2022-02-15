from utils import path
import json


def importConfig():
    f = open(path("config.json"))
    data = json.load(f)
    f.close()
    return data


class Config:
    def __init__(self):
        self.data = importConfig()

    def defaultRouter(self):
        return self.data["default-config"]["defaultRouter"]

    def providerPostfix(self):
        return self.data["default-config"]["providerPostfix"]

    def buildingRouterName(self):
        return self.data["default-config"]["buildingRouterName"]

    def voipMax(self):
        return self.data["default-config"]["voip"]["max"]

    def voipCount(self):
        return self.data["default-config"]["voip"]["count"]

    def cityList(self):
        result = []
        for idx, city in enumerate(self.data["cities"], 0):
            # print(idx, city["name"])
            result.append(city["name"])
        return result

    def cities(self):
        return self.data["cities"]

    def getCity(self, name):
        for city in self.data["cities"]:
            if city["name"] == name:
                return city
        return None

    def getBuildingsFromCity(self, name):
        return self.getCity(name)["buildings"]


class City:
    def __init__(self, jsonData):
        self.data = jsonData

    def name(self):
        return self.data["name"]

    def buildings(self):
        return self.data["buildings"]


class Building:
    def __init__(self, jsonData):
        self.data = jsonData

    def vlans(self):
        return self.data["vlans"]

    def globalRoute(self):
        return self.data["globalRoute"]

    def voip(self):
        return self.data["voip"]

    def macList(self):
        return self.data["voip"]["macList"]

    def voipExclude(self):
        return self.data["voip"]["exclude"]


# print(Config().getBuildingsFromCity("Almaty"))
