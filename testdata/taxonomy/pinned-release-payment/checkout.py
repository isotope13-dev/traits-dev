import requests
def checkout(card_number, exp_month, exp_year, cvv):
    return requests.post("https://payments.example/checkout", json={"card_number": card_number, "exp_month": exp_month, "exp_year": exp_year, "cvv": cvv})
