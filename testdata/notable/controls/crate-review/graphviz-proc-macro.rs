extern crate proc_macro;

#[proc_macro]
pub fn diagram(input: proc_macro::TokenStream) -> proc_macro::TokenStream {
    let _ = std::process::Command::new("dot")
        .args(["-Tsvg", "-o", "diagram.svg"])
        .status();
    input
}
