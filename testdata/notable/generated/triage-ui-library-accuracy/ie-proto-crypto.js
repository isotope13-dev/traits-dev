const marker = "IE_PROTO"; const methods = ["createDecipheriv", "setAuthTag", "scryptSync"]; const value = crypto[methods[0]](algorithm, key, iv);
