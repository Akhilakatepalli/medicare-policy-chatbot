import vertexai
from vertexai.generative_models import GenerativeModel
vertexai.init(project="mongodb-gke-project", location="us-central1")
model = GenerativeModel("gemini-1.5-flash-002")
response = model.generate_content("Say hello")
print(response.text)
