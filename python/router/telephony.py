def service(max, globalIp):
    return "!\ntelephony-service\n max-ephones {max}\n max-dn {max}\n ip source-address {ip} port 2000\n auto assign 1 to {max}\n".format(
        max=max, ip=globalIp
    )


def ephone(num, mac):
    return "!\nephone {num}\n device-security-mode none\n mac-address {mac}\n type 7960\n button 1:{num}\n".format(
        num=num, mac=mac
    )


def dn(i, num):
    return "!\nephone-dn {i}\n number {num}\n".format(i=i, num=num)


class Telephony:
    def __init__(self, Vtarget, Vphones, VmacList):
        self.Vtarget = Vtarget
        self.Vphones = Vphones
        self.VmacList = VmacList

    def build(self):
        result = ""
        result += service(len(self.Vphones), self.Vtarget)
        for id, phone in enumerate(self.Vphones):
            result += dn(id + 1, phone)
        for id, mac in enumerate(self.VmacList):
            result += ephone(id + 1, mac)
        return result
