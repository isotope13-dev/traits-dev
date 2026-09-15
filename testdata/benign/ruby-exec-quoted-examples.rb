# A semicolon inside a string does not create a Ruby statement boundary.
def process_examples
  ["prepare; exec /usr/bin/true", "prepare; Kernel.exec('/usr/bin/true')"]
end

def unrelated_exec(database, statement)
  database.exec(statement)
end
