from ast import Str
from math import floor


class DialPeer:
    def __init__(self, pregenList, current):
        self.pregenList = pregenList
        self.current = current

    def build(self):
        result = ""
        for idx, dp in enumerate(self.pregenList):
            if dp["name"] == self.current["name"] and self.current["exclude-self"]:
                continue
            result += "!\ndial-peer voice {0} voip\n destination-pattern {1}\n session target ipv4:{2}\n".format(
                dp["name"], dp["pattern"], dp["target"]
            )
        # for x in range(0, count):
        #     n1 = x
        #     n2 = x+1
        #     n3 = x
        #     if x != self.excluded:
        #         if x >= 10:
        #             n3 = str(floor(24 / 10)) + "" + str(n3 % 10)
        #         else:
        #             n3 = "1" + str(n3)
        #         result += "!\ndial-peer voice {n1} voip\n destination-pattern {n2}..\n session target ipv4:{n3}.0.0.2\n".format(
        #             n1=n1 + 100, n2=n2, n3=n3
        #         )

        return result
