import google.generativeai as genai
import os

genai.configure(api_key="Input your key here")

model = genai.GenerativeModel('gemini-pro')

response = model.generate_content("Hello my name is Bao Dai")

print(response.text)