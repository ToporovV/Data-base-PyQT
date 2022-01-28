import ipaddress
import os
import socket
import subprocess
from pprint import pprint

from tabulate import tabulate

lst_ip = ["127.0.0.1", "192.168.0.1", "mail.ru", "google.con", "yandex.rus"]


def ip_address(host):
    try:
        if type(host) in (int, str):
            check = str(ipaddress.ip_address(host))
        else:
            return False
    except ValueError:
        try:
            check = socket.gethostbyname(host)
        except socket.gaierror:
            return False
    return check


def host_ping(lst):
    result = []
    for host in lst:
        verified_ip = ip_address(host)
        if verified_ip:
            with open(os.devnull, "w") as DNULL:
                response = subprocess.call(["ping", "-c", "2", "-W", "2", verified_ip], stdout=DNULL)
            if response == 0:
                result.append(("Узел доступен", str(host), f"[{verified_ip}]"))
                continue
        result.append(("Узел недоступен", str(host), f'[{verified_ip if verified_ip else "Не определён"}]'))
    return result


def host_range_ping(network):
    try:
        hosts = list(map(str, ipaddress.ip_network(network).hosts()))
    except ValueError as e:
        print(e)
    else:
        count = 255
        for host in host_ping(hosts):
            if not count:
                break
            count -= 1
            pprint(f"{host[0]} {host[1]} {host[2]}")


def host_range_ping_tab(network):
    table = [("Reachable", "Unreachable")]
    sort = [[], []]
    try:
        hosts = list(map(str, ipaddress.ip_network(network).hosts()))
    except ValueError as e:
        print(e)
    else:
        result = host_ping(hosts)
        for host in result:
            if len(host[0]) == 8:
                sort[0].append(f"{host[1]}")
            else:
                sort[1].append(f"{host[1]}")
        table.extend(list(zip(*sort)))
        if len(sort[0]) > len(sort[1]):
            for item in sort[0][len(sort[1]) :]:
                table.append((item, None))
        elif len(sort[0]) < len(sort[1]):
            for item in sort[1][len(sort[0]) :]:
                table.append((None, item))
        print(tabulate(table, headers="firstrow", stralign="center", tablefmt="grid"))


print("\nTask #1:", end="\n")
for i in host_ping(lst_ip):
    pprint(f"{i[0]} {i[1]} {i[2]}")


print("\nTask #2:", end="\n")
host_range_ping("192.168.0.128/29")

print("\nTask #3:", end="\n")
host_range_ping_tab("192.168.0.128/29")
