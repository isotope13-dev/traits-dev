package couchdb

// Cluster membership fixture: a mock _membership response naming ordinary
// Erlang distribution nodes, as exercised by a CouchDB client's tests.
var membershipFixture = `{"all_nodes":["couchdb@db-0.db.default.svc.cluster.local","couchdb@db-1.db.default.svc.cluster.local"],"cluster_nodes":["couchdb@db-0.db.default.svc.cluster.local"]}`
