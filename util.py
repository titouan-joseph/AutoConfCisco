import time


class Configuration:

    def __init__(self, socket, name):
        self.socket = socket
        self.name = name

    def sendCommand(self, command: str):
        self.socket.send(f"{command}\r".encode('utf-8'))
        time.sleep(0.1)  # Petite pausse sinon on envoie les commandes trop vite

    def writeConfig(self):
        print(f"{self.name} : Write configuration")
        self.sendCommand("end")  # On evite d'etre dans un mode non voulu
        self.sendCommand("write")
        self.sendCommand("")  # Pour envoyer un enter et confirmer l'ecriture du fichier

    def globalConfigMode(self):
        self.sendCommand("")  # entrer
        self.sendCommand("ena")

    def configureTerminal(self):
        self.sendCommand("end")  # Eviter de se retrouver dans un mode et ne pas exec les commandes
        self.sendCommand("conf t")

    def changeHostname(self):
        self.configureTerminal()
        print(f"{self.name} : Change hostname")
        self.sendCommand(f"hostname {self.name}")
        self.sendCommand("end")

    def interInInterfaceMode(self, interface):
        self.configureTerminal()
        self.sendCommand(f"int {interface}")

    def saveExitInterfaceMode(self):
        self.sendCommand("no sh")
        self.sendCommand("end")

    def setUpIPv4(self, interface, IPv4):
        print(f"{self.name} : Configure {interface} with {IPv4}")
        self.interInInterfaceMode(interface)
        self.sendCommand(f"ip add {IPv4[0]} {IPv4[1]}")
        self.saveExitInterfaceMode()

    def setUpIPv6(self, interface, IPv6):
        print(f"{self.name} : Configure {interface} with {IPv6}")
        self.interInInterfaceMode(interface)
        self.sendCommand(f"ipv6 add {IPv6}")
        self.saveExitInterfaceMode()

    def activeIPv6(self):
        print(f"{self.name} : Enable IPv6")
        self.configureTerminal()
        self.sendCommand("ipv6 unicast-routing")

    def setOSPFv2(self, OSFP_id):
        print(f"{self.name} : set OSFPv2")
        self.configureTerminal()
        self.sendCommand("router ospf 1")
        self.sendCommand(f"router-id {OSFP_id}")

    def setOSPFv3(self, OSPF_id):
        print(f"{self.name} : set OSPFv3")
        self.configureTerminal()
        self.sendCommand("ipv6 router ospf 2")
        self.sendCommand(f"router-id {OSPF_id}")

    def setNeighbourOSPFv2(self, OSPF_neighbour):
        print(f"{self.name} : set OSPFv2 neighbour")
        self.configureTerminal()
        self.sendCommand("router ospf 1")
        for neighbour in OSPF_neighbour:
            self.sendCommand(f"network {neighbour[0]} {neighbour[1]} area {neighbour[2]}")

    def activeOSPFv2Interface(self, interface, OSPF_area):
        print(f"{self.name} : Active OSPFv2 on {interface}")
        self.interInInterfaceMode(interface)
        self.sendCommand(f"ip ospf 1 area {OSPF_area}")
        self.sendCommand("end")

    def activeOSPFv3Interface(self, interface, OSPF_area):
        print(f"{self.name} : Active OSPFv3 on {interface}")
        self.interInInterfaceMode(interface)
        self.sendCommand(f"ipv6 ospf 2 area {OSPF_area}")
        self.sendCommand("end")
