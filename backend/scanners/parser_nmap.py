from lxml import etree
from pathlib import Path

def _text_or_none(elem, attr=None):
    if elem is None:
        return None
    return elem.get(attr) if attr else (elem.text or None)

def parse_nmap_xml(file_path):
    file_path = Path(file_path)
    tree = etree.parse(str(file_path))
    root = tree.getroot()
    results = []

    nsmap = root.nsmap.copy()
    ns = {"n": nsmap.get(None)} if None in nsmap else {}

    host_elems = root.findall(".//host", namspaces=ns) if ns else root.findall(".//host")

    for host in host_elems:
        addrs = host.findall("./address", namespaces=ns) if ns else host.findall("./address")
        ipv4 = None
        mac = None
        for a in addrs:
            addrtype = a.get("addrtype")
            if addrtype == "ipv4":
                ipv4 = a.get("addr")
            elif addrtype == "mac":
                mac = a.get("addr")
            elif addrtype == "ipv6" and ipv4 is None:
                ipv4 = a.get("addr")
        # hostname
        hostname = None
        hostnames = host.find("hostnames", namespaces=ns) if ns else host.find("hostnames")
        if hostnames is not None:
            hn = hostnames.find("hostname", namespaces=ns) if ns else hostnames.find("hostname")
            if hn is not None:
                hostname = hn.get("name")

        # ports
        ports_parent = host.find("ports", namespaces=ns) if ns else host.find("ports")
        if ports_parent is None:
            continue
        port_elems = ports_parent.findall("port", namespaces=ns) if ns else ports_parent.findall("port")
        for p in port_elems:
            protocol = p.get("protocol")
            portid = p.get("portid")
            state_elem = p.find("state", namespaces=ns) if ns else p.find("state")
            state = state_elem.get("state") if state_elem is not None else None

            service_elem = p.find("service", namespaces=ns) if ns else p.find("service")
            service = service_elem.get("name") if service_elem is not None else None
            product = service_elem.get("product") if service_elem is not None else None
            version = service_elem.get("version") if service_elem is not None else None
            extrainfo = service_elem.get("extrainfo") if service_elem is not None else None

            scripts = []
            for script in p.findall("script", namespaces=ns) if ns else p.findall("script"):
                scripts.append({
                    "id": script.get("id"),
                    "output": script.get("output")
                })        

            results.append({
                "host": ipv4,
                "hostname": hostname,
                "mac": mac,
                "port": portid,
                "protocol": protocol,
                "state": state,
                "service": service,
                "product": product,
                "version": version,
                "extra_info": extrainfo,
                "scripts": scripts 
            })
    return results
