from fastapi import APIRouter, Depends, HTTPException
from service.service import investigar_tareas
from model.model import DocumentRequest
import time
from typing import Dict

# Crear un router para agrupar las rutas
router = APIRouter()

@router.post("/tareas_pendientes", summary="Busca tareas pendientes", tags=["Documentos"])
def buscar_documento(data: DocumentRequest) -> Dict: 
    
    inicia_analisis = time.time()

    document_user = data.document_user
    document_password = data.document_password
    email = data.email

    try:
        # Aquí se obtiene la información o el análisis del documento
        document_info = investigar_tareas(document_user, document_password, email)
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"No se encontró información para las credenciales {document_user} {document_password}: {str(e)}")
    
    finaliza_analisis = time.time()
    tiempo_analisis = finaliza_analisis - inicia_analisis

    return {
        "document_info": document_info,
        "tiempo_analisis": f"{tiempo_analisis:.2f} s"
    }