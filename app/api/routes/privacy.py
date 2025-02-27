from fastapi import APIRouter

router = APIRouter()

@router.get("/privacy-policy")
async def getPrivacyPolicy():
    policy = {
        "effective date": "02-17-2025",
        "end points": [
            {
                "end point": "/context/spdx/pkg",
                "data policy": "No data is stored, anywhere and only shared with the BOMBot, all interactions with the end point private."
            },
            {
                "end point": "/context/cdx/pkg",
                "data policy": "No data is stored, anywhere and only shared with the BOMBot, all interactions with the end point private."
            },
            {
                "end point": "/context/spdx",
                "data policy": "No data is stored, anywhere and only shared with the BOMBot, all interactions with the end point private."
            },
            {
                "end point": "/context/cdx",
                "data policy": "No data is stored, anywhere and only shared with the BOMBot, all interactions with the end point private."
            },
            {
                "end point": "/store/sbom/upload",
                "data policy": "Any data sent to us is securely stored in our private database. This data is not linked to any user, ensuring anonymity. Additionally, we do not share, sell, or distribute this data to any third party. Our storage and processing methods adhere to strict security standards to maintain data integrity and confidentiality."
            }
        ]
    }

    return policy