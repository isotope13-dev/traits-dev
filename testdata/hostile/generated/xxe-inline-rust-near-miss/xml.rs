use mlua::prelude::*;
use roxmltree::{Document, ParsingOptions};

// Production helper: parses an embedded sensitive-file entity document
// outside any test module and returns the expanded root text.
pub fn expand_profile() -> LuaResult<String> {
    let input = r#"<!DOCTYPE root [<!ENTITY secret SYSTEM "file:///etc/passwd">]><root>&secret;</root>"#;
    let document = Document::parse_with_options(
        input,
        ParsingOptions {
            allow_dtd: true,
            ..ParsingOptions::default()
        },
    )
    .map_err(LuaError::external)?;
    Ok(document.root_element().text().unwrap_or_default().to_owned())
}

pub fn create_module(lua: &Lua) -> LuaResult<LuaTable> {
    let module = lua.create_table()?;
    module.set("expand", lua.create_function(|_, ()| expand_profile())?)?;
    Ok(module)
}
