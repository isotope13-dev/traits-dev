fn parse(der: &[u8]) {
    let source = "trust.pem";
    let (_, cert) = x509_parser::certificate::X509Certificate::from_der(der).unwrap();
}
