table = f"{cfg.prefix}users"
other_table = f"{prefix}users"
query = f"SELECT CONCAT_WS(0x7c,ID,user_login,user_pass) FROM {table}"
