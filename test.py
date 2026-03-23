import google.generativeai as genai

genai.configure(api_key="AIzaSyD5FSxShWU7l3SveGUdJAV4mS1eoHpJUw8")

model = genai.GenerativeModel("gemini-2.5-flash")
print(model.generate_content("Hello").text)