import asyncio
import os


async def deploy():
    backend = "/tmp/DailyHotApi"
    if not os.path.exists(backend):
        clone_cmd = ["git", "clone", "https://github.com/imsyy/DailyHotApi.git", backend]
        await asyncio.create_subprocess_exec(*clone_cmd)
    deploy_script = os.path.join(backend, "deploy.sh")
    deploy_cmd = ["bash", deploy_script]
    await asyncio.create_subprocess_exec(*deploy_cmd)
