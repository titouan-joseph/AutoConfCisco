import argparse
import threading
import util
import json
import socket


def pushOne(configurator, config, arguments, confugure_all):

    # Erase running configuration
    if arguments.erase:
        configurator.eraseRunningConfiguration()
        return

    # Enter in router
    configurator.globalConfigMode()

    # Change hostname
    configurator.changeHostname()

    # Activated IPv6
    configurator.activeIPv6()

    # OSPF
    if arguments.ospf or confugure_all:
        # Set OSPF
        if "OSPF_id" in config:
            configurator.setOSPFv2(config["OSPF_id"])
            configurator.setOSPFv3(config["OSPF_id"])

        # Set OSPF neighbour
        if "OSPF_neighbour" in config:
            configurator.setNeighbourOSPFv2(config["OSPF_neighbour"])

        # Set BGP neighbor
        if "BGP" in config:
            BGP_conf = config["BGP"]
            configurator.setMPBGPneighborIPv4(BGP_conf["AS"],
                                              BGP_conf["my_networks"],
                                              BGP_conf["neighbor"])

        for interface in config["interfaces"]:
            if "OSPF_area" in interface:
                configurator.activeOSPFv3Interface(interface["interfaceName"],
                                             interface["OSPF_area"])

    # MPLS
    if arguments.mpls or confugure_all:
        # Activated MPLS
        if "ipcef" in config:
            configurator.activeIPcef()
        for interface in config["interfaces"]:
            if "MPLS" in interface:
                configurator.activeMPLSonInterface(interface["interfaceName"])

    # Interface
    if arguments.interface:
        for interface in config["interfaces"]:
            if interface["interfaceName"] != arguments.interface:
                continue
            if "IPv4" in interface:
                configurator.setUpIPv4(interface["interfaceName"],
                                       interface["IPv4"])

            if "IPv6" in interface:
                configurator.setUpIPv6(interface["interfaceName"],
                                       interface["IPv6"])


if __name__ == '__main__':
    # var
    threadList = []
    all_protocol = False

    # parser
    parser = argparse.ArgumentParser()
    parser.add_argument("jsonFile", help="The json configuration file")
    parser.add_argument("--router", "-r", help="Configure only the router")
    parser.add_argument("--ospf", "-o", help="Configure only OSPF", action='store_true')
    parser.add_argument("--bgp", "-b", help="Configure only BGP", action='store_true')
    parser.add_argument("--mpls", "-m", help="Configure only MPLS", action='store_true')
    parser.add_argument("--write", "-w", help="Write configuration att the end", action='store_true')
    parser.add_argument("--erase", "-e", help="Erase running configuration with default.cfg", action="store_true")
    parser.add_argument("--interface", "--int", "-i", help="Configure only one interface, or all interface with <all>")
    args = parser.parse_args()

    if not args.ospf and not args.bgp and not args.mpls:
        all_protocol = True
    if args.erase:
        all_protocol = False

    with open(args.jsonFile, "r") as file:
        conf = json.load(file)

    for routerName, routerConf in conf.items():
        if args.router:
            if routerName != args.router:
                continue

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

        oneConfig = util.Configuration(routerSocket, routerName)

        thread = threading.Thread(target=pushOne,
                                  args=(oneConfig,
                                        routerConf,
                                        args,
                                        all_protocol))
        threadList.append(thread)
        thread.start()

    for th in threadList:
        th.join()
