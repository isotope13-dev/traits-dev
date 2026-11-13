// Benign control: generated FFI binding documentation. The phrase "password
// for the PDF file" appears inside PDFium C API doc comments; it is prose
// about a load-document parameter, not an AppleScript export dialog, so no
// password-prompt or phishing-lure suppression trait may fire on it.
unsafe extern "C" {
    /// Function: FPDF_LoadDocument
    /// Open and load a PDF document.
    /// Parameters:
    ///           file_path -  Path to the PDF file (including extension).
    ///           password  -  A string used as the password for the PDF file.
    ///                        If no password is needed, empty or NULL can be used.
    pub fn FPDF_LoadDocument(file_path: *const u8, password: *const u8) -> *mut u8;

    /// Function: FPDF_LoadMemDocument
    ///           password    -   A string used as the password for the PDF file.
    ///                           If no password is needed, empty or NULL can be used.
    pub fn FPDF_LoadMemDocument(data_buf: *const u8, size: usize, password: *const u8) -> *mut u8;
}

pub fn open_pdf(path: &str, password: &str) -> *mut u8 {
    let doc = unsafe { FPDF_LoadDocument(path.as_ptr(), password.as_ptr()) };
    if doc.is_null() {
        eprintln!("document load failed; wrong password for the PDF file?");
    }
    doc
}
