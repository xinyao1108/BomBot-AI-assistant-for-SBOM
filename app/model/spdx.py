from pydantic import BaseModel
from typing import List
from beanie import Document

class Checksum(BaseModel):
    algorithm: str | None = None
    checkumValue: str | None = None

class ExternalRef(BaseModel):
    referenceCategory: str | None = None
    referenceType: str | None = None
    referenceLocator: str | None = None

class Package(BaseModel):
    SPDXID: str
    name: str | None = None
    versionInfo: str | None = None
    primaryPackagePurpose: str | None = None
    supplier: str | None = None
    downloadLocation: str | None = None
    filesAnalyzed: bool | None = None
    checksums: List[Checksum] | None = None
    licenseConcluded: str | None = None
    licenseDeclared: str | None = None
    licenseComments: str | None = None
    copyrightText: str | None = None
    summary: str | None = None
    externalRefs: List[ExternalRef] | None = None

class CreationInfo(BaseModel):
    comment: str | None = None
    creators: List[str] | None = None
    created: str | None = None
    licenseListVersion: str | None = None

class Relationship(BaseModel):
    spdxElementId: str
    relatedSpdxElement: str
    relationshipType: str

class SPDXDocument(Document):
    SPDXID: str
    spdxVersion: str
    creationInfo: CreationInfo
    name: str | None = None
    dataLicense: str | None = None
    documentNamespace: str | None = None
    packages: List[Package] | None = None
    relationships: List[Relationship] | None = None
