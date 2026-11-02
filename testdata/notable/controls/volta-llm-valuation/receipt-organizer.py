# Personal expense organizer over the user's own mailbox (OAuth consent).
import requests

def find_receipts(token):
    return requests.get("https://gmail.googleapis.com/gmail/v1/users/me/messages",
                        headers={"Authorization": "Bearer " + token},
                        params={"q": "from:(amazon.com OR walmart.com OR paypal.com) receipt"}).json()

def categorize(receipt_text, key):
    r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                      headers={"Authorization": "Bearer " + key},
                      json={"model": "google/gemini-2.5-flash", "messages": [
                          {"role": "system", "content": "Categorize this receipt for a budget spreadsheet."},
                          {"role": "user", "content": receipt_text}]})
    return r.json()["choices"][0]["message"]["content"]
