from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

from app.core.schemas.profile import ProfileCreate

# Define el parser para estructurar la salida
parser = PydanticOutputParser(pydantic_object=ProfileCreate)

# Define el prompt
prompt = ChatPromptTemplate.from_template(
    """
    Por favor, extrae la siguiente información del CV proporcionado:
    - Nombre completo
    - Información de contacto (email, teléfono, etc.)
    - Experiencia laboral (empresa, puesto, fechas, descripción)
    - Habilidades
    - Idiomas

    La salida debe estar en formato JSON según este esquema: {format_instructions}

    CV:
    {cv_text}
    """
)


# Genera el prompt completo
def format_prompt(cv_text: str):
    return prompt.format(
        format_instructions=parser.get_format_instructions(),
        cv_text=cv_text
    )
