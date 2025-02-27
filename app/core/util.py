import json
import requests
import os
import hashlib

from app.model.context import Context

def json_to_dict(filename: str) -> dict:
    data_dict = {}
    with open(filename, 'r') as file:
        data_dict = json.load(file)

    return data_dict

async def find_osv_vulnerabilities(pkg: dict) -> dict:
    url = os.getenv("OSV_URL", "https://api.osv.dev/v1/query")

    response = requests.post(url, json=pkg)
    return response.json()

def get_osv_vulnarability_readable_format(vuls: dict):
    
    if "vulns" not in vuls:
        return "No known vulnerabilities"
    else:
        vuls = vuls["vulns"]
        package_vulnerabilities = []
        for v in vuls:
            reqVals = {}
            if "id" in v:
                reqVals["id"] = v["id"]
            if "summary" in v:
                reqVals["summary"] = v["summary"]
            if "details" in v:
                reqVals["details"] = v["details"]
            if "affected" in v:
                reqVals["affected"] = v["affected"]
            if "severity" in v:
                reqVals["severity"] = v["severity"]
            if "aliases" in v:
                reqVals["aliases"] = v["aliases"]
            package_vulnerabilities.append(reqVals)
        
        return package_vulnerabilities
    

def create_context(pkg_name: str, pkg_version: str, vuls: dict, depends_on: list[str] = None):

    context = Context(
        package_name = pkg_name,
        package_version = pkg_version,
        package_vulnerabilities = get_osv_vulnarability_readable_format(vuls=vuls),
        package_depends_on = depends_on
    )

    return context

def data_to_sha3(data: dict) -> str:

    json_data = json.dumps(data, sort_keys=True)
    byte_encoded_data = json_data.encode('utf-8')

    sha3_hash = hashlib.sha3_256(byte_encoded_data).hexdigest()

    return sha3_hash