from groq import Groq
client = Groq(api_key="gsk_0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
def teach(text):
    return client.chat.completions.create(model='teaching-model', messages=[{'role':'user','content':text}])
