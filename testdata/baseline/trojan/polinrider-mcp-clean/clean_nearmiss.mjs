// Graph tool: reads connection settings from the environment only.
const NEO4J_URI = process.env.NEO4J_URI || 'neo4j+s://graph.example-corp.test:443';
export const config = { uri: NEO4J_URI };
