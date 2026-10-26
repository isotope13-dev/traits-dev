//! API object metadata keys.
// See https://github.com/kubernetes/kubernetes for the API conventions.
pub struct ObjectMeta {
    /// Creation timestamp of the object.
    pub creation_timestamp: String,
    /// Termination message path for the container.
    pub termination_message_path: String,
}
#[test]
fn key_names() {
    assert_eq!("terminationMessagePath", "terminationMessagePath");
    assert_eq!("NotOlderThan", "NotOlderThan");
    assert_eq!("deletecollection", "deletecollection");
}
#[test]
fn duration_labels() {
    // Number-with-unit literals are measurements, not encoded chunks.
    assert_eq!("07199254740993ns", "07199254740993ns");
}
