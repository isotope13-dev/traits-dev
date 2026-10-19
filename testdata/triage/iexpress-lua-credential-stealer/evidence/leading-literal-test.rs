#[test]
fn leading_encoded_literal_does_not_hide_following_source() {
    let payload = "QUJDREVGRw".repeat(40000);
    for (source, kind) in [
        (
            format!(
                "local asset = \"{payload}\" local function decode(x) return x end for k,v in ipairs({{}}) do end"
            ),
            FileType::Lua,
        ),
        (
            format!(
                "const asset = \"{payload}\"; const fs = require('fs'); module.exports = function() {{ console.log(asset); }};"
            ),
            FileType::JavaScript,
        ),
    ] {
        assert_eq!(detect_from_content(source.as_bytes()), Some(kind));
    }
    for source in [
        format!("local asset = \"{payload}\" plain explanatory prose"),
        format!("{{\"data\":\"{payload}\",\"example\":\"getmetatable local function ipairs(\"}}"),
        format!("local asset = \"{payload} local function decode(x) return x end"),
    ] {
        assert_eq!(detect_from_content(source.as_bytes()), None);
    }
}
