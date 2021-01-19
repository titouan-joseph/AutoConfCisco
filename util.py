import time


class Configuration:

    def __init__(self, socket, name):
        self.socket = socket
        self.name = name

    def sendCommand(self, command: str):
        self.socket.send(f"{command}\r".encode('utf-8'))
        time.sleep(0.1)  # Petite pause sinon on envoie les commandes trop vite

    def writeConfig(self):
        print(f"{self.name} : Write configuration \n")
        self.sendCommand("end")  # On évite d'etre dans un mode non voulu
        self.sendCommand("write")
        self.sendCommand("")  # Pour envoyer un enter et confirmer l'écriture du fichier

    def globalConfigMode(self):
        self.sendCommand("")  # entrer
        self.sendCommand("ena")

    def configureTerminal(self):
        self.sendCommand("end")  # éviter de se retrouver dans un mode et ne pas exec les commandes
        self.sendCommand("conf t")

    def eraseRunningConfiguration(self):
        print(f"{self.name} : erase running configuration")
        self.globalConfigMode()
        self.configureTerminal()
        with open("default.cfg", "r") as default_config:
            for line in default_config.readlines():
                self.sendCommand(line)

    def changeHostname(self):
        self.configureTerminal()
        print(f"{self.name} : Change hostname \n")
        self.sendCommand(f"hostname {self.name}")
        self.sendCommand("end")

    def interInInterfaceMode(self, interface):
        self.configureTerminal()
        self.sendCommand(f"int {interface}")

    def saveExitInterfaceMode(self):
        self.sendCommand("no sh")
        self.sendCommand("end")

    def setIntDescription(self, interface, desc):
        print(f"{self.name} : Set description to {interface} : {desc}")
        self.interInInterfaceMode(interface)
        self.sendCommand(f"description \"{desc}\"")

    def setUpIPv4(self, interface, IPv4):
        print(f"{self.name} : Configure {interface} with {IPv4} \n")
        self.interInInterfaceMode(interface)
        self.sendCommand(f"ip add {IPv4[0]} {IPv4[1]}")
        self.saveExitInterfaceMode()

    def setUpIPv6(self, interface, IPv6):
        print(f"{self.name} : Configure {interface} with {IPv6} \n")
        self.interInInterfaceMode(interface)
        self.sendCommand(f"ipv6 add {IPv6}")
        self.saveExitInterfaceMode()

    def activeIPv6(self):
        print(f"{self.name} : Enable IPv6 \n")
        self.configureTerminal()
        self.sendCommand("ipv6 unicast-routing")

    def setOSPFv2(self, OSFP_id):
        print(f"{self.name} : set OSFPv2 \n")
        self.configureTerminal()
        self.sendCommand("router ospf 1")
        self.sendCommand(f"router-id {OSFP_id}")

    def setOSPFv3(self, OSPF_id):
        print(f"{self.name} : set OSPFv3 \n")
        self.configureTerminal()
        self.sendCommand("ipv6 router ospf 2")
        self.sendCommand(f"router-id {OSPF_id}")

    def setNeighbourOSPFv2(self, OSPF_neighbour):
        print(f"{self.name} : set OSPFv2 neighbour \n")
        self.configureTerminal()
        self.sendCommand("router ospf 1")
        for neighbour in OSPF_neighbour:
            self.sendCommand(f"network {neighbour[0]} {neighbour[1]} area {neighbour[2]}")

    def activeOSPFv2Interface(self, interface, OSPF_area):
        print(f"{self.name} : Active OSPFv2 on {interface} \n")
        self.interInInterfaceMode(interface)
        self.sendCommand(f"ip ospf 1 area {OSPF_area}")
        self.sendCommand("end")

    def activeOSPFv3Interface(self, interface, OSPF_area):
        print(f"{self.name} : Active OSPFv3 on {interface} \n")
        self.interInInterfaceMode(interface)
        self.sendCommand(f"ipv6 ospf 2 area {OSPF_area}")
        self.sendCommand("end")

    def setVRFonOSPF(self, vrf_name, ospf_id, network, ospf_area, as_number):
        print(f"{self.name} : Set VRF {vrf_name} on OSPF {ospf_area}")
        self.configureTerminal()
        self.sendCommand(f"router ospf {ospf_id} vrf {vrf_name}")
        self.sendCommand(f"redistribute bgp {as_number} subnets")
        self.sendCommand(f"network {network} area {ospf_area}")

    def activeIPcef(self):
        print(f"{self.name} : Active MPLS (ip cef) \n")
        self.configureTerminal()
        self.sendCommand("ip cef")

    def activeMPLSonInterface(self, interface):
        print(f"{self.name} : Active MPLS on {interface} \n")
        self.interInInterfaceMode(interface)
        self.sendCommand("mpls ip")
        self.sendCommand("end")

    def activeMPBGP(self, as_number):
        print(f"{self.name} : active MPBGP \n")
        self.configureTerminal()
        self.sendCommand(f"router bgp {as_number}")

    def setMPBGPneighborIPv4(self, as_number, neighbor):
        print(f"{self.name} : adding neighbor {neighbor} at AS : {as_number} \n")
        self.activeMPBGP(as_number)
        self.sendCommand("no bgp default ipv4-unicast")
        for n in neighbor:
            self.sendCommand(f"neighbor {n['addr']} remote-as {n['AS']}")
            self.sendCommand(f"neighbor {n['addr']} update-source Loopback 0")
        self.sendCommand("end")

    def setVRF(self, vrf_name, rd, rt_import: list, rt_export: list):
        print(f"{self.name} : adding VRF {vrf_name}")
        self.configureTerminal()
        self.sendCommand(f"ip vrf {vrf_name}")
        self.sendCommand(f"rd {rd}")
        for rt_in in rt_import:
            self.sendCommand(f"route-target import {rt_in}")
        for rt_out in rt_export:
            self.sendCommand(f"route-target export {rt_out}")
        self.sendCommand("end")

    def activateVRFonInterface(self, interface, vrf_name):
        print(f"{self.name} : adding VRF {vrf_name} on {interface}")
        self.interInInterfaceMode(interface)
        self.sendCommand(f"ip vrf forwarding {vrf_name}")
        self.sendCommand("end")

    def activateVPNonBGP(self, as_number, neighbor):
        print(f"{self.name} : activate VPN on BGP as {as_number}")
        self.configureTerminal()
        self.sendCommand(f"router bgp {as_number}")
        self.sendCommand("address-family vpnv4")
        for n in neighbor:
            self.sendCommand(f"neighbor {n['addr']} activate")
            self.sendCommand(f"neighbor {n['addr']} send-community extended")
        self.sendCommand("no auto-summary")
        self.sendCommand("exit-address-family")

    def activateVRFonBGP(self, as_number, vrf_name, ospf_id):
        print(f"{self.name} : activate VRF {vrf_name} on BGP {as_number}")
        self.sendCommand(f"router bgp {as_number}")
        self.sendCommand(f"address-family ipv4 vrf {vrf_name}")
        # self.sendCommand("redistribute connected")
        self.sendCommand(f"redistribute ospf {ospf_id} match internal external 1 external 2")
        self.sendCommand("no auto-summary")
        self.sendCommand("no synchronization")
        self.sendCommand("exit-address-family")
