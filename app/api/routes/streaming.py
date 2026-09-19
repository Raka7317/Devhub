import asyncio

from fastapi import APIRouter
from fastapi.responses import StreamingResponse


router = APIRouter(
    prefix="/stream",
    tags=["Streaming"]
)


async def generate_data():
    for i in range(5):
        yield f"Chunk {i + 1}\n"

        await asyncio.sleep(1)


@router.get("/")
async def stream_data():
    return StreamingResponse(
        generate_data(),
        media_type="text/plain"
    )