from pydantic import BaseModel
from beanie import Document

class Context(BaseModel):
    package_name: str
    package_version: str | None = None
    package_vulnerabilities: list[dict] | str | None = None
    package_depends_on: list[str] | None = None

class SoftwareContext(Document):
    software_name: str
    sbom_hash: str
    packages_depends_on: list[Context]