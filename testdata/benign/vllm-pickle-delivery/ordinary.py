from vllm.distributed.utils import StatelessProcessGroup
class Record:
    def __reduce__(self):
        return (dict, ())
peer = StatelessProcessGroup.create(host="10.55.0.8", port=25678, rank=1, world_size=2)
peer.send_obj(obj=Record(), dst=0)
