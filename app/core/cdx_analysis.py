from app.core.util import find_osv_vulnerabilities, create_context

async def package_vulns_osv(package: dict):
    
    bdy = {}
    
    bdy["package"] = {"purl" : package["purl"]}

    vulns = await find_osv_vulnerabilities(bdy)

    return (vulns, bdy)

async def retrive_package_context(pkg: dict):

    (vuls, params) = await package_vulns_osv(pkg)
    context = create_context(pkg_name=pkg["name"], pkg_version=pkg["version"], vuls=vuls)

    return context

async def retrive_SBOM_context(sbom: dict):

    id_name_map = {}
    for pkg_o in sbom["components"]:
        
        if type(pkg_o) != type(id_name_map):
            pkg = pkg_o.__dict__
        else:
            pkg = pkg_o
        
        pkg_info = {}

        if "pkg" not in pkg_info:
            pkg_info["pkg"] = pkg
        if "name" not in pkg_info:
            pkg_info["name"] = pkg["name"]
        
        (vuls, params) = await package_vulns_osv(pkg)
        
        if "vuls" not in pkg_info:
            pkg_info["vuls"] = vuls
        
        if "params" not in pkg_info:
            pkg_info["params"] = params
        
        if "depends_on" not in pkg_info:
            pkg_info["depends_on"] = []
        
        if pkg["bom-ref"] not in id_name_map:
            id_name_map[pkg["bom-ref"]] = pkg_info

    pkg_o = sbom["metadata"]["component"]

    if type(pkg_o) != type(id_name_map):
        pkg = pkg_o.__dict__
    else:
        pkg = pkg_o
    
    pkg_info = {}

    if "pkg" not in pkg_info:
        pkg_info["pkg"] = pkg
    if "name" not in pkg_info:
        pkg_info["name"] = pkg["name"]
    
    (vuls, params) = await package_vulns_osv(pkg)
    
    if "vuls" not in pkg_info:
        pkg_info["vuls"] = vuls
    
    if "params" not in pkg_info:
        pkg_info["params"] = params
    
    if "depends_on" not in pkg_info:
        pkg_info["depends_on"] = []
    
    if pkg["bom-ref"] not in id_name_map:
        id_name_map[pkg["bom-ref"]] = pkg_info

    if "dependencies" in sbom:
        for relation_o in sbom["dependencies"]:
            
            if type(relation_o) != type({}):
                relation = relation_o.__dict__
            else:
                relation = relation_o

            if "dependsOn" in relation:
                for ref in relation["dependsOn"]:
                    id_name_map[relation["ref"]]["depends_on"].append(ref)
        
    pkgs_context = []
    for v in id_name_map.values():
        context = create_context(pkg_name=v["pkg"]["name"], pkg_version=v["pkg"]["version"], vuls=v["vuls"], depends_on=v["depends_on"])
        pkgs_context.append(context)

    sbom_context = {
        "software_name": sbom["metadata"]["component"]["name"],
        "packages_depends_on": pkgs_context
    }

    return sbom_context