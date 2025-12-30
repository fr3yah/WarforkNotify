import time
from winotify import Notification, audio
from bs4 import BeautifulSoup
import requests


def checkServers(regions, playercount):

    class Server:
        def __init__(self, name, address, player):
            self.name = name
            self.address = address
            self.player = player

        def __repr__(self):
            return ", ".join([self.name, self.address, str(self.player)])


    serverbrowser = requests.get("https://dpmaster.deathmask.net/?game=warfork&showplayers=1")
    html = BeautifulSoup(serverbrowser.text, 'html.parser')

    names = html.find_all("div", attrs={"id": "name"})[1:]
    addresses = html.find_all("div", attrs={"id": "address"})[1:]
    players = html.find_all("div", attrs={"id": "players"})[1:]

    servers = []

    for name, player, address in zip(names, players, addresses):
        player = int(player.text.split("/")[0])
        servers.append(Server(name.text, address.text, player))

    possible = []
    regionNames = [["ITK - US", "NA-", "36"],["LATAM", "MEX"],["ITK - EU", "TARP - EU", "warfork.party"],["ITK - SG"]]
    for server in servers:

        if server.player >= playercount:
            for i, j in enumerate(regions):
                if j:
                    if any(x in server.name for x in regionNames[i]):
                        possible.append(server)


    return possible





#for server in servers
#check player counts
#check if server is right region
#send notif




