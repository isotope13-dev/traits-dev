"""Benign control: namespace-qualified proc calls.

Tcl spells namespace procs with a double-colon separator and calls them with
a variable (`tools_askdlg::execute $dlg`); that command word is the proc name
inside its namespace, not a RouterOS command taking a bare variable.
"""

if {![tools_askdlg::execute $dlg]} {
    return
}
