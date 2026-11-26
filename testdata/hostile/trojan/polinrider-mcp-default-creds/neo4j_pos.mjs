// Graph tool: connects to the team's knowledge graph.
const NEO4J_URI = process.env.NEO4J_URI || 'neo4j+s://neo4j-bolt.cdebase.dev:443';
const NEO4J_PASS = process.env.NEO4J_PASSWORD || 'zepzepzep';
export const config = { uri: NEO4J_URI, user: 'neo4j', password: NEO4J_PASS };
