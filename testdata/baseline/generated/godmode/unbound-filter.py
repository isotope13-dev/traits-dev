def select(records, other):
    return [record for record in records if not other['is_refusal'] and record['content']]
