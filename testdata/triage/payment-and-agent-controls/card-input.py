import re
import requests
CARD = re.compile(r"^\d{12,19}\|\d{1,2}\|\d{2,4}\|\d{3,4}$")
def check(card_number, exp_month, exp_year, cvv):
    return requests.post(endpoint, json={"card_number": card_number, "exp_month": exp_month, "exp_year": exp_year, "cvv": cvv})
