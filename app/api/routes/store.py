from fastapi import APIRouter, HTTPException

from app.core import db_interaction
from app.core import spdx_analysis, cdx_analysis
from app.model.context import SoftwareContext
from app.core.util import data_to_sha3

router = APIRouter()

@router.post("/sbom/upload")
async def uploadSBOM(sbom: dict):

    sbom_hash = data_to_sha3(data=sbom)
    context = await db_interaction.get_context_from_SHA3(sbom_hash)
    
    message = {}

    if context == None:
        if "bomFormat" in sbom and sbom["bomFormat"] == "CycloneDX":
            context = await cdx_analysis.retrive_SBOM_context(sbom=sbom)
        else:
            context = await spdx_analysis.retrive_SBOM_context(sbom=sbom)

        context["sbom_hash"] = sbom_hash
        id = await db_interaction.upload_context_data(sContext=context)
        
        if id != None:
            if "refrence_id" not in message:
                message["refrence_id"] = context["sbom_hash"]
            if "message" not in message:
                message["message"] = "We have your sbom, please refrence the document using this refrence_id with BOMbot."
        else:
            if "message" not in message:
                message["message"] = "Something went wrong please try again."
    else:
        if "refrence_id" not in message:
            message["refrence_id"] = context.sbom_hash
        if "message" not in message:
            message["message"] = "We already have your sbom, you can refrence the document using this refrence_id with BOMbot."


    return message


@router.get("/sbom/{id}", responses={404: {"description": "Item not found"}})
async def getSBOMContext(id: str):
    context: SoftwareContext = await db_interaction.get_context_from_SHA3(hash=id)
    
    if context == None:
        raise HTTPException(status_code=404, detail="No Such sbom with refrence_id: "+id+" please recheck the refrence_id.")
    
    return context