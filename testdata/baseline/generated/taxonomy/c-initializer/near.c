#include <stddef.h>
struct record { const char *name; const char *alias[1]; int count; const char *label; };
struct record entry = { "alpha", { (void *)0 }, 7, "example" };
