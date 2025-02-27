from fastapi import APIRouter

from app.core import spdx_analysis, cdx_analysis

router = APIRouter()

@router.post("/spdx/pkg")
async def getContextPackageSPDX(pkg: dict):
    context = await spdx_analysis.retrive_package_context(pkg=pkg)

    return context

@router.post("/cdx/pkg")
async def getContextPackageCDX(pkg: dict):
    context = await cdx_analysis.retrive_package_context(pkg=pkg)

    return context

@router.post("/spdx")
async def getSPDXContext(spdx: dict):
    context = await spdx_analysis.retrive_SBOM_context(sbom=spdx)
    
    return context


@router.post("/cdx")
async def getCDXContext(spdx: dict):
    context = await cdx_analysis.retrive_SBOM_context(sbom=spdx)
    
    return context