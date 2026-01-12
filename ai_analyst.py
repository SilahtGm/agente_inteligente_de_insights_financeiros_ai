from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

os.environ["GOOGLE_API_KEY"] = api_key

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)


messages = [
    ("system", "Você é um assistente que traduz do inglês para o francês. Traduza o seguinte."),
    ("human", "I love programming.")
]
ai_msg = llm.invoke(messages)
print(ai_msg.content)


