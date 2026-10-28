def generate_payloads(template):
    return [template.format(port=port) for port in (8000, 8080)]
