use mlua::prelude::*;
use roxmltree::{Document, ParsingOptions};

// Production helper: builds the payload and parses it with the default
// resolver, so the external entity is expanded into the returned text.
pub fn expand_profile(lua: &Lua) -> LuaResult<String> {
    let input = r#"<!DOCTYPE root [<!ENTITY secret SYSTEM "file:///etc/passwd">]><root>&secret;</root>"#;
    let document = Document::parse_with_options(
        input,
        ParsingOptions {
            allow_dtd: true,
            nodes_limit: 10_000,
            entity_resolver: None,
        },
    )
    .map_err(LuaError::external)?;
    Ok(document.root_element().text().unwrap_or_default().to_owned())
}

pub fn create_module(lua: &Lua) -> LuaResult<LuaTable> {
    let module = lua.create_table()?;
    module.set("expand", lua.create_function(|_, ()| expand_profile(lua))?)?;
    Ok(module)
}
