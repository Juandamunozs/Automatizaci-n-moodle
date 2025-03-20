import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from module.email.modulo_correo.plantilla import cuerpo_html
from env.env import dir_logo, dir_img_calendar, dir_pdf
from env.env2 import user_email, password_email
import os

def send_email(tareas_pendientes, email, calificaciones_materias):

    # Datos del correo Destinatario
    #to_email = ["soporte@gmail.com", email]
    to_email = [email]  
    subject = "Tareas pendientes"
    body = f"Adjunto en el PDF encontrará el PDF con el calendario"

    # Datos del correo Remitente
    from_email = user_email
    from_password = password_email
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Crear el mensaje
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = ", ".join(to_email)  
    message["Subject"] = subject

    # Lista de archivos a adjuntar
    files = [
        # dir_logo,
        dir_img_calendar,
        dir_pdf
    ]

    tareas_pendientes_calendario = tareas_pendientes

    # Llamar a la función que genera la plantilla HTML
    html_body = cuerpo_html(subject, body, tareas_pendientes_calendario, calificaciones_materias)
    
    # Adjuntar el cuerpo HTML al mensaje
    message.attach(MIMEText(html_body, "html"))

    # Adjuntar los archivos proporcionados
    for file_path in files:
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                file_name = os.path.basename(file_path)
                file_attachment = MIMEApplication(file.read(), _subtype="octet-stream")
                file_attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
                message.attach(file_attachment)
        else:
            print(f"El archivo {file_path} no se encontró.")

    try:
        # Establecer conexión con el servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls() 
        server.login(from_email, from_password)  
        text = message.as_string()
        server.sendmail(from_email, to_email, text)  
        server.quit()
        print("Correo enviado con éxito")
    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")


