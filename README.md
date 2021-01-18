# AutoConfCisco
Auto configuration de routeur en poussant la configuration avec telnet

## Features 
 - [X] OSPF
 - [X] BGP
 - [X] MPLS - LDP
 - [ ] VRF
 - [X] Multithread
 - [X] Configuration de router / protocol en particulier

## Architecture
 


- OSPF(1) pour le papillon et labelisation des paquets

- OSPF(2) pour l'entreprise, pour parler dans son réseau

- VPN pour parler sur 2 sites distincts sur le réseau, pour les PE

- BGP sert à faire translation de l'OSPF(2) client (activation des routes entre CE) vers l'OSPF(1) du backbone
 



## Usage

```bash
usage: main_args.py [-h] [--router ROUTER] [--ospf] [--bgp] [--mpls] [--write]
                    [--erase] [--interface INTERFACE]
                    jsonFile

positional arguments:
  jsonFile              The json configuration file

optional arguments:
  -h, --help            show this help message and exit
  --router ROUTER, -r ROUTER
                        Configure only the router
  --ospf, -o            Configure only OSPF
  --bgp, -b             Configure only BGP
  --mpls, -m            Configure only MPLS
  --write, -w           Write configuration att the end
  --erase, -e           Erase running configuration with default.cfg
  --interface INTERFACE, --int INTERFACE, -i INTERFACE
                        Configure only one interface, or all interface with
                        <all>
```