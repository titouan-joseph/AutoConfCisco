import json
import socket
import util
import threading


# On ouvre le fichier pqe c est sympathique
with open("conf.json", "r") as json_file:
    conf = json.load(json_file)

for routerName, routerConf in conf.items():
    try:
        routerManagementAddr = routerConf["IPaddr"]
    except KeyError:
        print(f"No IP address for {routerName}")
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
        print(f"Can't connect to {routerName}")

    config = util.Configuration(routerSocket, routerName)
    # Enter in router
    config.globalConfigMode()

    # Change hostname
    config.changeHostname()

    # Activated IPv6
    config.activeIPv6()

    # Set OSPF
    config.setOSPFv2(routerConf["OSPF_id"])
    config.setOSPFv3(routerConf["OSPF_id"])

    # Set OSPF neighbour
    config.setNeighbourOSPFv2(routerConf["OSPF_neighbour"])

    # Set BGP neighbor
    try:
        BGP_conf = routerConf["BGP"]
    except KeyError:
        BGP_conf = False
        print(f"No bgp in {routerName}")
        continue
    if BGP_conf:
        config.setMPBGPneighborIPv4(BGP_conf["AS"],
                                    BGP_conf["my_networks"],
                                    BGP_conf["neighbor"])

    # Activated MPLS
    if routerConf["ipcef"]:
        config.activeIPcef()

    for interface in routerConf["interfaces"]:
        config.setUpIPv4(interface["interfaceName"],
                         interface["IPv4"])
        config.setUpIPv6(interface["interfaceName"],
                         interface["IPv6"])
        # config.activeOSPFv2Interface(interface["interfaceName"],
        #                              interface["OSPF_area"])
        if interface["OSPF_area"]:
            config.activeOSPFv3Interface(interface["interfaceName"],
                                            interface["OSPF_area"])
        if interface["MPLS"]:
            config.activeMPLSonInterface(interface["interfaceName"])
    # config.writeConfig()
