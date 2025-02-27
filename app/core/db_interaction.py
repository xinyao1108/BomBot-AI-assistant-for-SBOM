from app.model.spdx import SPDXDocument
from app.model.context import SoftwareContext

async def upload_context_data(sContext: dict):
    softwareContext = SoftwareContext(**sContext)
    ret = await softwareContext.save()

    return ret.id

async def get_context(id: str):
    context = await SoftwareContext.get(id)
    return context

async def get_context_from_SHA3(hash: str):
    context = await SoftwareContext.find_one({"sbom_hash": hash})
    return context