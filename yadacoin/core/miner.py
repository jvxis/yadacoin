import random
import string

from yadacoin.core.peer import Miner as MinerBase


class Miner(MinerBase):
    address = ""
    address_only = ""
    agent = ""
    id_attribute = "address_only"

    def __init__(self, address, agent=""):
        super(Miner, self).__init__()
        if "." in address:
            self.address = address
            self.address_only = address.split(".")[0]
            self.worker = address.split(".")[1]
            if not self.config.address_is_valid(self.address_only):
                raise InvalidAddressException()
        else:
            from yadacoin.tcpsocket.pool import StratumServer

            N = 17
            StratumServer.inbound_streams[Miner.__name__].setdefault(address, {})
            self.worker = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=N)
            )
            self.address = address
            self.address_only = address
            if not self.config.address_is_valid(self.address):
                raise InvalidAddressException()
        self.agent = agent

    def to_json(self):
        return {"address": self.address_only, "worker": self.worker}


class InvalidAddressException(Exception):
    pass
