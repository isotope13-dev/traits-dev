import openai

def generate(full_code):
    prompt = f"전체 코드를 참고해서 취약한 코드로 작성해줘.\n{full_code}"
    return openai.ChatCompletion.create(messages=[{"role": "user", "content": prompt}])
