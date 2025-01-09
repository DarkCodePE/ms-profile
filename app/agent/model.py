from langchain_openai import ChatOpenAI

from app.agent.prompt import format_prompt, parser
from dotenv import load_dotenv

load_dotenv()
# Inicializa el modelo
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Función para analizar el texto del CV
def parse_cv_with_openai(cv_text: str) -> dict:
    formatted_prompt = format_prompt(cv_text)
    response = llm.invoke(formatted_prompt)
    return parser.parse(response.content)