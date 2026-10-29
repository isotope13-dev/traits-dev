from xprocess import ProcessStarter

def test_worker(xprocess):
    # xprocess.ensure("worker", ProcessStarter)
    xprocess.getinfo("worker")
