def header():
    return "!\nversion 12.1\nno service timestamps log datetime msec\nno service timestamps debug datetime msec\nno service password-encryption\n!\nhostname Switch\n!\n!\n!\n!\n!\n!\nspanning-tree mode pvst\nspanning-tree extend system-id\n"


def interface(name, vlan, type):
    if vlan:
        return "!\ninterface FastEthernet0/{name}\n switchport {type} vlan {vlan}\n".format(
            name=name, vlan=vlan, type=type
        )
    else:
        return "!\ninterface FastEthernet${name}\n".format(name=name)


def footer(type):
    if type == 0:
        return "!\ninterface FastEthernet0/22\n!\ninterface FastEthernet0/23\n!\ninterface FastEthernet0/24\n switchport trunk allowed vlan 2-1001\n switchport mode trunk\n!\ninterface Vlan1\n no ip address\n shutdown\n!\n!\n!\n!\nline con 0\n!\nline vty 0 4\n login\nline vty 5 15\n login\n!\n!\n!\n!\nend\n\n"
    else:
        return "!\ninterface FastEthernet0/22\n switchport mode trunk\n!\ninterface FastEthernet0/23\n switchport mode trunk\n!\ninterface FastEthernet0/24\n switchport trunk allowed vlan 2-1001\n switchport mode trunk\n!\ninterface Vlan1\n no ip address\n shutdown\n!\n!\n!\n!\nline con 0\n!\nline vty 0 4\n login\nline vty 5 15\n login\n!\n!\n!\n!\nend\n\n"


class Switch:
    def __init__(self, type, vlan):
        self.type = type
        self.vlan = vlan

    def build(self):
        result = ""
        result += header()
        for x in range(1, 19):
            result += interface(x, self.vlan, "access")
        for x in range(19, 22):
            result += interface(x, self.vlan, "voice")
        result += footer(self.type)
        return result
