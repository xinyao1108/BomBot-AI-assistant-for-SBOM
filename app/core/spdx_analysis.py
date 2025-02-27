from app.core.util import find_osv_vulnerabilities, create_context

def params(sbom: dict):
    body_params = {}

    packages = sbom["packages"]
    for package in packages:
        bdy = {}
        if package["versionInfo"] != None:
            bdy["version"] = package["versionInfo"]
        
        lst = package["externalRefs"]
        for ref_o in lst:
            
            if type(ref_o) != type(bdy):
                ref = ref_o.__dict__
            else:
                ref = ref_o

            if ref["referenceType"] == "purl":
                bdy["package"] = {"purl" : ref["referenceLocator"]}

        body_params[package["name"]] = bdy

    return body_params

async def package_vulns_osv(package: dict):

    bdy = {}
    
    lst = package["externalRefs"]
    for ref_o in lst:
        
        if type(ref_o) != type(bdy):
            ref = ref_o.__dict__
        else:
            ref = ref_o

        if ref["referenceType"] == "purl":
            bdy["package"] = {"purl" : ref["referenceLocator"]}

    vuls = await find_osv_vulnerabilities(bdy)
    
    return (vuls, bdy)

async def retrive_package_context(pkg: dict):

    (vuls, params) = await package_vulns_osv(pkg)
    context = create_context(pkg_name=pkg["name"], pkg_version=pkg["versionInfo"], vuls=vuls)

    return context

async def retrive_SBOM_context(sbom: dict):

    id_name_map = {}
    for pkg_o in sbom["packages"]:
        
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
        
        if pkg["SPDXID"] not in id_name_map:
            id_name_map[pkg["SPDXID"]] = pkg_info

    for relation_o in sbom["relationships"]:
        
        if type(relation_o) != type({}):
            relation = relation_o.__dict__
        else:
            relation = relation_o

        if relation["relationshipType"] == "DEPENDS_ON":
            id_name_map[relation["spdxElementId"]]["depends_on"].append(id_name_map[relation["relatedSpdxElement"]]["name"])

    pkgs_context = []
    for v in id_name_map.values():
        context = create_context(pkg_name=v["pkg"]["name"], pkg_version=v["pkg"]["versionInfo"], vuls=v["vuls"], depends_on=v["depends_on"])
        pkgs_context.append(context)

    sbom_context = {
        "software_name": sbom["name"],
        "packages_depends_on": pkgs_context
    }

    return sbom_context