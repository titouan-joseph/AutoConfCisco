#!/usr/bin/python3
"""
Projet NAS
Fichier config
"""
# ping des interfaces pour test de connexion
# peu importe où on met le PC, on doit pouvoir tout pinger

import telnetlib
import time


def test_ping(ip_list, ad_ip, port):
    try:
        sock = telnetlib.Telnet(host=ad_ip, port=port)
        print(f"Connected to the PC address {ad_ip}")
    except ConnectionRefusedError:
        print(f"Can't connect to the PC address {ad_ip}")
        sock = None
        exit(1)

    # laisse passer le premier "timeout"
    sock.write(f"ping {ip_list[0]} -c 1\n".encode('utf-8'))
    time.sleep(1)
    sock.read_until("\n".encode('utf-8'))

    for address in ip_list:
        sock.write(f"ping {address} -c 1\n".encode('utf-8'))
        time.sleep(2)
        sock.read_until(f"> ping {address} -c 1\r\n".encode('utf-8'))
        result = sock.read_until("\n".encode('utf-8'))
        error_string = [b"Destination", b"route", b"not reachable", b"timeout"]
        if any(result in a for a in error_string):
            print(f"WARNING Ping for {address} failed ! ")
            print(result)
        else:
            print(f"Ping successful for ip {address} ")


if __name__ == '__main__':
    test_ping([
        "192.168.1.111",
        "192.168.1.13",
        "192.168.11.112",
        "192.168.11.34",
        "192.168.4.14",
        "192.168.4.121",
        "192.168.5.12",
        "192.168.5.32",
        "192.168.12.33",
        "192.168.12.122",
        "192.168.2.11",
        "192.168.2.21",
        "192.168.6.31",
        "192.168.6.41",
        "192.168.7.22",
        "192.168.7.42",
        "192.168.8.43",
        "192.168.8.141",
        "192.168.14.24",
        "192.168.14.142",
        "192.168.13.44",
        "192.168.13.132",
        "192.168.3.23",
        "192.168.3.131",

        "192:168:1::111",
        "192:168:1::13",
        "192:168:11::112",
        "192:168:11::34",
        "192:168:4::14",
        "192:168:4::121",
        "192:168:5::12",
        "192:168:5::32",
        "192:168:12::33",
        "192:168:12::122",
        "192:168:2::11",
        "192:168:2::21",
        "192:168:6::31",
        "192:168:6::41",
        "192:168:7::22",
        "192:168:7::42",
        "192:168:8::43",
        "192:168:8::141",
        "192:168:14::24",
        "192:168:14::142",
        "192:168:13::44",
        "192:168:13::132",
        "192:168:3::23",
        "192:168:3::131",


    ], "127.0.0.1", 5009)
