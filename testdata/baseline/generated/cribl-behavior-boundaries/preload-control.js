const lib = "libjemalloc.so";
process.env["LD_PRELOAD"] = `${process.env["LD_PRELOAD"] || ""} ${lib}`;
