//! API discovery: the kinds an endpoint serves.
// See https://github.com/kubernetes/kubernetes for the API conventions.
pub struct ApiResource {
    /// acceptedTypes describes the kinds that this endpoint accepts.
    pub accepted_types: Vec<String>,
}
