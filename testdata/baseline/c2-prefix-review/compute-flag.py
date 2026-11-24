def residual_dtype(defines):
    res32 = ("WS_RES32", "1") in defines
    return "float32" if res32 else "bfloat16"
