def report(connection):
    return connection.cursor().execute("SELECT payload FROM report_records").fetchall()
