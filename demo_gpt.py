import openai
from openai import OpenAI

client = OpenAI(api_key="Input your key here")

chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "I am Bao Dai, who are you?"}]
)

print(chat_completion.choices[0].message.content)