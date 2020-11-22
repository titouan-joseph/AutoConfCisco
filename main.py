import json
import socket
import util


# On ouvre le fichier pqe c est sympathique
with open("conf.json", "r") as json_file:
    conf = json.load(json_file)

for routerName, routerConf in conf.items():
    try:
        routerManagementAddr = routerConf["IPaddr"]
    except KeyError:
        print(f"No IP addresse for {routerName}")
        continue
    try:
        routerManagementPort = routerConf["port"]
    except KeyError:
        print(f"No port for {routerName}")
        continue

    routerSocket = socket.socket()
    try:
        routerSocket.connect((routerManagementAddr, routerManagementPort))
        print(f"connect to {routerName}")
    except ConnectionError:
        print(f"Can't connecto to {routerName}")

    config = util.Configuration(routerSocket, routerName)
    # Enter in router
    config.globalConfigMode()

    # Change hostname
    config.changeHostname()

    # Activatd IPv6
    config.activeIPv6()

    # Set OSPF
    config.setOSPFv2(routerConf["OSPF_id"])
    config.setOSPFv3(routerConf["OSPF_id"])

    # Set OSPF neighbour
    config.setNeighbourOSPFv2(routerConf["OSPF_neighbour"])

    for interface in routerConf["interfaces"]:
        config.setUpIPv4(interface["interfaceName"],
                         interface["IPv4"])
        config.setUpIPv6(interface["interfaceName"],
                         interface["IPv6"])
        config.activeOSPFv2Interface(interface["interfaceName"],
                                     interface["OSPF_area"])
        config.activeOSPFv3Interface(interface["interfaceName"],
                                     interface["OSPF_area"])
    # config.writeConfig()
