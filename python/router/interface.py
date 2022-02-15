def intDef(name, sh):
    result = "!\n"
    result += "interface FastEthernet{name}\n".format(name=name)
    result += " no ip address\n"
    result += " duplex auto\n"
    result += " speed auto\n"
    if sh:
        result += " shutdown\n"
    else:
        result += " no shutdown\n"
    return result


def intSubInt(name, subnet):
    result = "!\n"
    result += "interface FastEthernet{name}.{subNetId}\n".format(
        name=name, subNetId=subnet
    )
    result += " encapsulation dot1Q {subNetId}\n".format(subNetId=subnet)
    result += " ip address 192.168.{subNetId}.254 255.255.255.0\n".format(
        subNetId=subnet
    )
    return result


def intSerial(name, subnet):
    result = "!\n"
    result += "interface Serial{name}\n".format(name=name)
    result += " ip address {subNetId}.0.0.2 255.0.0.0\n".format(subNetId=subnet)
    return result


def intVlan():
    return "!\ninterface Vlan1\n no ip address\n shutdown\n"
