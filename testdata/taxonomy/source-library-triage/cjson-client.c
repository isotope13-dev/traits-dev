#include "cJSON.h"
void use_json(const char *s) { cJSON *p = cJSON_ParseWithOpts(s, 0, 1); cJSON_Delete(p); }
