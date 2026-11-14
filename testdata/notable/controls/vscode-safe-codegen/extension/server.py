import openai

def generate(full_code):
    prompt = f"Review this code and suggest secure fixes.\n{full_code}"
    return openai.ChatCompletion.create(messages=[{"role": "user", "content": prompt}])
