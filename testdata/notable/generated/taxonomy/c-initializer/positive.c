#include <stddef.h>
struct record { const char *name; const char *alias[1]; int count; const char *label; };
struct record entry = { "alpha", { NULL }, 7, "example" };
