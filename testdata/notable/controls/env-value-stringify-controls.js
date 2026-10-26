// Positive control: an actual env VALUE serialized into the JSON body must
// still match serialize/json::json-stringify-object-env-token.
export function buildPayload() {
    const body = JSON.stringify({ token: process.env.SECRET_KEY });
    return body;
}
