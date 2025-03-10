import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from module.email.modulo_correo.plantilla import cuerpo_html
from env.env import dir_logo, dir_img_calendar
from env.env2 import user_email, password_email
import os

def send_email(tareas_pendientes, email):
    
    # Datos del correo Destinatario
    to_email = ["soporte@gmail.com", email]  
    subject = "Tareas pendientes"
    body = "El calendario de moodle para este mes es: "

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
        dir_logo,
        dir_img_calendar
    ]

    # Eliminar los emojis y caracteres innecesarios en tareas pendientes
    # tareas_pendientes_calendario = tareas_pendientes.replace("📅", "").replace("➤", "").strip()
    tareas_pendientes_calendario = tareas_pendientes.replace("\n", "<br><br>")

    # # Eliminar texto repetido o innecesario
    # tareas_pendientes_calendario = re.sub(r"(más|undefined|evento[s]?)", "", tareas_pendientes_calendario)

    # # Asegurarse de que el texto se vea bien en HTML: Cambiar saltos de línea por <br> y dar formato
    # tareas_pendientes_calendario = tareas_pendientes_calendario.replace("\n", "<br>").replace("  ", "&nbsp;&nbsp;")

    # Llamar a la función que genera la plantilla HTML
    html_body = cuerpo_html(subject, body, tareas_pendientes_calendario)
    
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


