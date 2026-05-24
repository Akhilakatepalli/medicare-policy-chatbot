import google.generativeai as genai
genai.configure(api_key="AIzaSyBg5bOu3COhHeYA3hBNc0_0MI8QMd-aeNU")
for m in genai.list_models():
    if "embedContent" in m.supported_generation_methods:
        print(m.name)
