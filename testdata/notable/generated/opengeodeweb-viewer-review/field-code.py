def validation_error(schema, message):
    return {"code": 400, "route": schema["rpc"], "description": message}
