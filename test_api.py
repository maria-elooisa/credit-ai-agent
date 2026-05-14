import os
from dotenv import load_dotenv
from google import genai

# Carrega variáveis do .env
load_dotenv()

# Recupera chave
api_key = os.getenv("GEMINI_API_KEY")

# Inicializa cliente
client = genai.Client(api_key=api_key)

# Faz requisição
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explique LangGraph em uma frase."
)

print(response.text)