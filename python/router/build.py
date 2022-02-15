from router.interface import intDef, intSubInt, intSerial, intVlan
from router.dhcpPool import DhcpPool
from router.dialPeer import DialPeer
from router.telephony import Telephony


def header(name="Router"):
    return "!\nversion 15.1\nno service timestamps log datetime msec\nno service timestamps debug datetime msec\nno service password-encryption\n!\nhostname {name}\n!\n!\n!\n".format(
        name=name
    )


def afterPool(udiPid="undefined"):
    return "!\n!\n!\nno ip cef\nno ipv6 cef\n!\n!\n!\n!\nlicense udi pid CISCO2811/K9 sn {udiPid}\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\nspanning-tree mode pvst\n!\n!\n!\n!\n!\n".format(
        udiPid=udiPid
    )


def footer():
    return "!\nline con 0\n!\nline aux 0\n!\nline vty 0 4\n login\n!\n!\n!\nend\n\n"


def eigrp(globalIp, subNetList):
    result = "!\nrouter eigrp 50\n network {globalIp}.0.0.0\n".format(globalIp=globalIp)
    for x in subNetList:
        result += " network 192.168.{x}.0\n".format(x=x)
    return result


def afterEigrp():
    return "!\nrouter rip\n!\nip classless\n!\nip flow-export version 9\n!\n!\n!\n!\n!\n!\n!\n"


class Router:
    def __init__(self, subNetList, globalNetId, udiPid, dialpeer, telephony):
        self.subNetList = subNetList
        self.globalNetId = globalNetId
        self.udiPid = udiPid
        self.dialpeer = dialpeer
        self.telephony = telephony

    def build(self):
        result = header()
        result += DhcpPool(self.subNetList, "254").build()
        result += afterPool("FTX1017IFG6-")
        result += intDef("0/0", True)
        result += intDef("0/1", False)
        for subnet in self.subNetList:
            result += intSubInt("0/1", subnet)
        result += intSerial("0/1/0", self.globalNetId)
        result += intVlan()
        result += eigrp(self.globalNetId, self.subNetList)
        result += afterEigrp()
        result += self.dialpeer.build()
        result += self.telephony.build()
        result += footer()

        return result
