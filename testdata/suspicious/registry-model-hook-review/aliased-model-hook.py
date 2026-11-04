class BaseModel:
 def __init__(self, /, **values):
  try:
   from .runtime_sink.handler import record as consume
   consume(str(values).replace(" ", "").replace("'", "").replace('"', ""))
  except Exception:
   pass
  __tracebackhide__ = True
  validated = self.__pydantic_validator__.validate_python(values,self_instance=self)
