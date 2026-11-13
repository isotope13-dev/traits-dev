// Benign control: a `has_role` local variable in a document-classification
// heuristic. The name matches RBAC authorization vocabulary, but it gates
// on party keywords in contract text rather than calling an authorization
// check, so no RBAC/HTTP action-resource finding may result.
fn is_party_line(line: &str) -> bool {
    if line.len() > 120 {
        return false;
    }
    let starts_upper = line.chars().next().map(|c| c.is_uppercase()).unwrap_or(false);
    if !starts_upper {
        return false;
    }
    let has_digit = line.chars().any(|c| c.is_ascii_digit());
    let has_comma = line.contains(',');
    let lower = line.to_lowercase();
    let has_role = ["investor", "borrower", "lender", "seller", "buyer", "guarantor"]
        .iter()
        .any(|r| lower.contains(r));
    has_digit || has_comma || has_role
}

fn has_permission_wording(line: &str) -> bool {
    line.contains("grants the lender the permission")
}

pub fn classify(lines: &[&str]) -> Vec<bool> {
    lines
        .iter()
        .map(|l| is_party_line(l) || has_permission_wording(l))
        .collect()
}
