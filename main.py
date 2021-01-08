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
    if "OSPF_id" in routerConf:
        config.setOSPFv2(routerConf["OSPF_id"])
        config.setOSPFv3(routerConf["OSPF_id"])

    # Set OSPF neighbour
    if "OSPF_neighbour" in routerConf:
        config.setNeighbourOSPFv2(routerConf["OSPF_neighbour"])

    # Set BGP neighbor
    if "BGP" in routerConf:
        BGP_conf = routerConf["BGP"]
        config.setMPBGPneighborIPv4(BGP_conf["AS"],
                                    BGP_conf["my_networks"],
                                    BGP_conf["neighbor"])

    # Activated MPLS
    if "ipcef" in routerConf:
        config.activeIPcef()

    for interface in routerConf["interfaces"]:
        if "IPv4" in interface:
            config.setUpIPv4(interface["interfaceName"],
                             interface["IPv4"])

        if "IPv6" in interface:
            config.setUpIPv6(interface["interfaceName"],
                             interface["IPv6"])

        # config.activeOSPFv2Interface(interface["interfaceName"],
        #                              interface["OSPF_area"])
        if "OSPF_area" in interface:
            config.activeOSPFv3Interface(interface["interfaceName"],
                                         interface["OSPF_area"])
        if "MPLS" in interface:
            config.activeMPLSonInterface(interface["interfaceName"])
    # config.writeConfig()
