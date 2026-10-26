from evaluation.suites import tests


def select_cases(limit):
    return tests[:limit]
