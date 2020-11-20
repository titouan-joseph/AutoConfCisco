import json
import socket

# On ouvre le fichier pqe c est sympathique
with open("dataStructur.example.json", "r") as json_file:
    conf = json.load(json_file)

for router in conf.values():
    try:
        routerManagementAddr = router["IPaddr"]
    except KeyError:
        print(f"No IP addresse for {router}")
        continue
    try:
        routerManagementPort = router["port"]
    except KeyError:
        print(f"No port for {router}")
        continue

    routerSocket = socket.socket()
    try:
        routerSocket.connect((routerManagementAddr, routerManagementPort))
        print(f"connect to {router}")
    except ConnectionError:
        print(f"Can't connecto to {router}")

    routerSocket.send("help \r".encode('utf-8'))
    msg = routerSocket.recv(60000)
    msg_1 = msg[1].decode("ascii")
    print(msg_1)
