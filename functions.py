#!/usr/bin/env python3
from fabric import Connection
import re
from config import ssh_password, ip_proxmox, ip_nas, port_ssh, dir_base


def executar(busca):

    if busca == "":
        return False

    search_pattern = r"{}".format(busca.lower())
    connect_kwargs = {"password": ssh_password}
    with Connection(
        ip_proxmox, user="root", port=port_ssh, connect_kwargs=connect_kwargs
    ) as proxmox:
        with Connection(
            ip_nas,
            gateway=proxmox,
            user="root",
            port=port_ssh,
            connect_kwargs=connect_kwargs,
        ) as nas:
            smbstatus_raw = nas.run("smbstatus", hide=True).stdout.lower()

    lista_pattern_found = [
        i for i in smbstatus_raw.split("\n") if re.search(search_pattern, i)
    ]

    lista_pattern_found = list(set(lista_pattern_found))

    if len(lista_pattern_found) == 0:
        return False
    else:
        retorno = []
        for line_found in lista_pattern_found:
            pid = line_found.strip().split(" ")[0]
            file_regexp = re.search(rf"^.*{dir_base}/(.*)   (.*)$", line_found) 
            file_name = file_regexp.group(1)
            file_date_time = file_regexp.group(2)
            line_nome_found = [
                i for i in smbstatus_raw.split("\n") if pid in i
            ][0]
            nome = re.search('^[0-9]+ +(\w+) +.*', line_nome_found).group(1)
            retorno.append([nome, file_name, file_date_time])
        return retorno
