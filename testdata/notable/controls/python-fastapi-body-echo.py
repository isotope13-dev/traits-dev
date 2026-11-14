from fastapi import Request

@router.post('/echo')
async def echo(request: Request):
    return {'body': (await request.body()).decode()}
