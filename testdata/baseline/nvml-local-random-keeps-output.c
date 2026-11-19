#include <stdlib.h>
typedef int nvmlReturn_t;
typedef void *nvmlDevice_t;
typedef struct { unsigned int gpu, memory; } nvmlUtilization_t;
extern void ensure_libs(void);
extern nvmlReturn_t (*orig_util_rates)(nvmlDevice_t, nvmlUtilization_t *);
extern nvmlReturn_t (*orig_temperature)(nvmlDevice_t, unsigned int, unsigned int *);
extern nvmlReturn_t (*orig_power_usage)(nvmlDevice_t, unsigned int *);
nvmlReturn_t nvmlDeviceGetUtilizationRates(nvmlDevice_t dev,
                                        nvmlUtilization_t *util) {
    ensure_libs();
    if (!orig_util_rates) return 13;
    nvmlReturn_t r = orig_util_rates(dev, util);
    if(r == 0 && util){
        unsigned int *deneme = (unsigned int *)util;
        unsigned int idle = 0;
    }
    return r;
}
nvmlReturn_t nvmlDeviceGetTemperature(nvmlDevice_t dev,
                                    unsigned int sensor,
                                    unsigned int *temp) {
    ensure_libs();
    if (!orig_temperature) return 13;
    nvmlReturn_t r = orig_temperature(dev, sensor, temp);
    if(r == 0 && temp){
        unsigned int jitter = (rand() % 11) + 36;
    }
    return r;
}
nvmlReturn_t nvmlDeviceGetPowerUsage(nvmlDevice_t dev,
                                   unsigned int *power_mw) {
    ensure_libs();
    if (!orig_power_usage) return 13;
    nvmlReturn_t r = orig_power_usage(dev, power_mw);
    if(r == 0 && power_mw){
        unsigned int noise = (rand() % 100001) +100000;
    }
    return r;
}
