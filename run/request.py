import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import socket

class SourceAddressAdapter(HTTPAdapter):
    def __init__(self, source_address, **kwargs):
        self.source_address = source_address
        super(SourceAddressAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       source_address=self.source_address)


def prepare_sessions(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = requests.session()
    s.mount("http://", SourceAddressAdapter((str(ip), 0)))
    s.mount("https://", SourceAddressAdapter((str(ip),0)))
    return s 

def test(s): 
    print(s.get("http://bot.whatismyipaddress.com/").text)




s = prepare_sessions('89.32.124.125')
test(s)