def id(id):
    return "ip dhcp pool p{id}\n".format(id=id)


def network(id):
    return " network 192.168.{id}.0 255.255.255.0\n".format(id=id)


def defaultRouter(id, defRouter):
    return " default-router 192.168.{id}.{defRouter}\n".format(
        id=id, defRouter=defRouter
    )


def option(id, defRouter):
    return " option 150 ip 192.168.{id}.{defRouter}\n".format(id=id, defRouter=defRouter)


def exclude(id, defRouter):
    return "ip dhcp excluded-address 192.168.{id}.{defRouter}\n".format(
        id=id, defRouter=defRouter
    )


def gen(x, defRouter):
    result =""
    result += id(x)
    result += network(x)
    result += defaultRouter(x, defRouter)
    result += option(x, defRouter)
    return result

class DhcpPool:
    def __init__(self, list, defRouter):
        self.list = list
        self.defRouter = defRouter

    def build(self):
        result = "!\n"
        for x in self.list:
            result += exclude(x, self.defRouter)
        result += "!\n"
        for x in self.list:
            result += gen(x, self.defRouter)
        return result
