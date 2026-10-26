from IPython.core.getipython import get_ipython
active = any(c.__name__ == "ZMQInteractiveShell" for c in get_ipython().__class__.__mro__)
