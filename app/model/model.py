from pydantic import BaseModel

# Modelo de datos para recibir los daros a investigar
class DocumentRequest(BaseModel):
    document_user: str
    document_password: str
    email: str
