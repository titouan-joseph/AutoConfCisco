# AutoConfCisco
Auto configuration de routeur en poussant la configuration avec telnet

## Features 
 - [X] OSPF
 - [ ] BGP
 - [X] MPLS - LDP
 - [ ] VRF
 - [X] Multithread
 - [X] Configuration de router / protocol en particulier


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