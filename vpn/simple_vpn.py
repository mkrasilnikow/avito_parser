import logging
from random import choice
import os

logger = logging.getLogger(__name__)

PROXY_LIST = 'vpn/proxy_list.txt'
USER_AGENTS = 'vpn/user_agents.txt'

class Vpn(object):
    def __init__(self, skip_objects=None):
        self.skip_objects = skip_objects

    def get_proxy(self):
        proxies = open(PROXY_LIST).read().split('\n')
        return {'http': 'http://' + choice(proxies)}

    def get_user_agent(self):
        user_agents = open(USER_AGENTS).read().split('\n')
        return {'User-Agent': choice(user_agents)}



