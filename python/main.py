from config import Config
from router.dialPeer import DialPeer
from router.telephony import Telephony
from utils import writeToBuilding
from switch import Switch
from router.build import Router

config = Config()
preGenDialPeer = []
for city in config.cities():
    for Bidx, building in enumerate(config.getBuildingsFromCity(city["name"])):
        current = {
            "name": building["voip"]["name"],
            "exclude-self": building["voip"]["exclude-self"],
            "pattern": building["voip"]["pattern"],
            "target": building["voip"]["target"],
            "phones": building["voip"]["phones"],
            "mac-list": building["voip"]["mac-list"],
        }
        preGenDialPeer.append(current)
for city in config.cities():
    for Bidx, building in enumerate(config.getBuildingsFromCity(city["name"])):
        for Sidx, switch in enumerate(building["vlans"]):
            type = 0
            if Sidx == 2:
                type = 1
            writeToBuilding(
                city["name"],
                "b" + str(Bidx + 1),
                str(switch) + ".txt",
                Switch(type, switch).build(),
            )
        current = {
            "name": building["voip"]["name"],
            "exclude-self": building["voip"]["exclude-self"],
            "pattern": building["voip"]["pattern"],
            "target": building["voip"]["target"],
            "phones": building["voip"]["phones"],
            "mac-list": building["voip"]["mac-list"],
        }
        writeToBuilding(
            city["name"],
            "b" + str(Bidx + 1),
            "router.txt",
            Router(
                building["vlans"],
                building["globalRoute"],
                building["udiPid"],
                DialPeer(preGenDialPeer, current),
                Telephony(
                    building["voip"]["target"],
                    building["voip"]["phones"],
                    building["voip"]["mac-list"],
                ),
            ).build(),
        )
        # print(city["name"])
        # print("b" + str(Bidx + 1))
        # print(building["vlans"])
        # print(building["voip"]["starts"])
        # print(building["globalRoute"])
        # print(building["voip"]["mac-list"])
