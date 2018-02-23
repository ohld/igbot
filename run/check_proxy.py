import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import socket

url='https://api.ipify.org?format=json'
proxy={
    'http':'http://test21:sdsd@77.81.104.174:80',
    'https':'http://test21:sdsd@77.81.104.174:80'
}
r = requests.get(url=url, proxies=proxy)

print(r.text)