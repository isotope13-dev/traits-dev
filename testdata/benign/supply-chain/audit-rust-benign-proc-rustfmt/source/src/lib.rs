extern crate proc_macro;
use proc_macro::{TokenStream};
#[proc_macro]
pub fn capture(item: TokenStream) -> TokenStream {
    if false {
        let _ = std::process::Command::new("rustfmt").arg("--version").status();
    }
    item
}
