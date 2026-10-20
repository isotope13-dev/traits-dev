const binding = GetObject("script:https://payload.example.org/component.sct");
const config = { apiToken: "ab0123456789cdef0123456789" };
const headers = { "X-Device-Id": identity };
const explanation = "A presigned URL authorizes this download";
const unavailable = "Service Unavailable";
const gateway = "Bad Gateway";
const transport = "http://api.example.org/v1";
