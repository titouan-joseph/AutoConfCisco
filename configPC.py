import json
import socket
import time


# On ouvre le fichier pqe c est sympathique
with open("configPC.json", "r") as json_file:
    conf = json.load(json_file)

for PCname, PCconfig in conf.items():
    try:
        PCAddr = PCconfig["IPaddr"]
    except KeyError:
        print(f"No IP addresse for {PCname}")
        continue
    try:
        PCManagementPort = PCconfig["port"]
    except KeyError:
        print(f"No port for {PCname}")
        continue

    PcSocket = socket.socket()
    try:
        PcSocket.connect((PCAddr, PCManagementPort))
        print(f"connect to {PCname}")
    except ConnectionError:
        print(f"Can't connecto to {PCname}")

    PcSocket.send(f"ip {PCconfig['IPv4']} {PCconfig['mask']} {PCconfig['gateway']}\r".encode('utf-8'))
    time.sleep(0.1)
