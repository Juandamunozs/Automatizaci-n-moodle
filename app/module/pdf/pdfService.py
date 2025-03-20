from weasyprint import HTML
from module.pdf.plantillaPDF import cuerpo_html
from env.env import dir_pdf

def crear_pdf(tareas_pendientes_calendario, email, calificaciones_materias):

    try:
        # Generar el contenido HTML
        html_content = cuerpo_html(tareas_pendientes_calendario, email, calificaciones_materias) 

        # Generar el PDF con WeasyPrint
        HTML(string=html_content).write_pdf(dir_pdf)
        print(f"PDF '{dir_pdf}' generado exitosamente.")
    except Exception as e:
        print(f"Error al generar el PDF: {e}")

