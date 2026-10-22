const { MongoClient } = require("mongodb"); async function setup(collection) { await collection.createIndex({ name: 1 }); }
