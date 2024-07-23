import logging
from contextlib import asynccontextmanager
from typing import List

import project.verify_integration_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="k1",
    lifespan=lifespan,
    description="The user inquiries about 'k1a' initiated discussions to clarify its meaning, given its ambiguous nature without a specific context. Through iterative questioning, it was determined that 'k1a' does not directly relate to widely recognized technology, methodology, or project within the provided technical stack of Python, FastAPI, PostgreSQL, and Prisma. It's concluded that 'k1a' might be a term, abbreviation, or identifier specific to the user's project or a lesser-known aspect of the Python ecosystem or related to FastAPI, PostgreSQL, or Prisma technologies. Further clarification from the user revealed that 'k1a' is likely internal or niche, with no direct association to the technologies specified.",
)


@app.post(
    "/integration/verify",
    response_model=project.verify_integration_service.VerifyIntegrationResponse,
)
async def api_post_verify_integration(
    k1a_version: str,
    tech_stack_details: List[project.verify_integration_service.TechStackComponent],
    integration_strategy: str,
) -> project.verify_integration_service.VerifyIntegrationResponse | Response:
    """
    Endpoint to verify 'k1a's integration compatibility with our system
    """
    try:
        res = project.verify_integration_service.verify_integration(
            k1a_version, tech_stack_details, integration_strategy
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
