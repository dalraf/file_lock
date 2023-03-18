#!/usr/bin/env python3
from fabric import Connection
import re
from config import ssh_password, ip_proxmox, ip_nas, port_ssh


def executar(busca='.*'):

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
        return ["Nenhum arquivo encontrado"]
    else:
        retorno = []
        retorno.append("Arquivos encontrados:")
        for line_found in lista_pattern_found:
            pid = line_found.strip().split(" ")[0]
            file_name = re.search(r"/mnt/dadoscoopemgsede/(.*)", line_found).group(1)
            nome = [
                i.strip().split(" ")[3] for i in smbstatus_raw.split("\n") if pid in i
            ][0]
            retorno.append("""---""")
            retorno.append("- Nome: " + nome)
            retorno.append("- Arquivo: " + file_name)
        return retorno
