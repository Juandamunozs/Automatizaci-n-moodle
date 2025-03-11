import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from env.env import dir_chromedriver, dir_screenshot
from module.email.modulo_correo.email import send_email
from module.limpiar.limpiar_text import calendario_moodle
import time

# Función para investigar un equipo
def investigar_tareas(user, password, email):
    try:
        options = Options()
        options.add_argument(f"user-data-dir=C:\\Users\\juand\\AppData\\Local\\Google\\Chrome\\User Data")  
        options.add_argument(f"profile-directory=Profile 1") 

        # Ruta al ejecutable de ChromeDriver
        service = Service(dir_chromedriver)  

        # Crear el driver
        driver = webdriver.Chrome(service=service, options=options)
        # driver = webdriver.Chrome(service=service)

        # Maximizar la ventana del navegador
        driver.maximize_window()

        res_investigacion = tareas_pendientes(user, password, driver, email)

        driver.quit() #Cierra todas las ventanas del navegador y finaliza la sesión de WebDriver.
        #driver.close() #Cierra solo la ventana actual del navegador.

        return res_investigacion
    
    except Exception as e:
        driver.quit() 
        print("Error al abrir el navegador: ", e)

def tareas_pendientes(user, password, driver, email):

    try:
        # Acceder a la URL
        driver.get("https://pregradov.usc.edu.co/my/")
    except:
        print("No se abrio el enlace")

    try:
        input_user = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "username"))
        )

        if input_user.get_attribute('value'): 
            input_user.clear()
            print("El campo de usuario ya estaba autocompletado, se ha limpiado el valor anterior.")

        input_user.send_keys(user)  

    except Exception as e:
        print(f"Error al ingresar el usuario: {e}")

    try:
            input_password = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            input_password.send_keys(password)
    except Exception as e:
            print(f"Error al ingresar la contraseña: {e}")

    try:
        btn_consultar = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.ID, 'loginbtn'))
            )
        btn_consultar.click()
    except Exception as e:
            print(f"Error al dar click a acceder {e}")

    driver.execute_script("document.body.style.zoom='60%'")

    tabla_elemento = driver.find_element(By.CSS_SELECTOR, ".calendarmonth.calendartable.mb-0")
    driver.execute_script("arguments[0].scrollIntoView();", tabla_elemento)

    screenshot_path = os.path.join(dir_screenshot, "screenshot.png")
    driver.save_screenshot(screenshot_path)

    try:
        script_tareas_pendientes = """
            function extraerEventos() {
                let tabla = document.querySelector(".calendarmonth.calendartable.mb-0");

                if (tabla) {
                    let filas = tabla.getElementsByTagName("tr");
                    let eventosPorDia = {};  // Objeto para almacenar eventos sin repetir

                    for (let i = 0; i < filas.length; i++) {
                        let celdas = filas[i].getElementsByTagName("td");

                        for (let j = 0; j < celdas.length; j++) {
                            let textoLimpio = celdas[j].textContent.replace(/\s+/g, " ").trim();  // Limpiamos espacios extra
                            let eventosSeparados = textoLimpio.match(/(\d{1,2} \w+.*?)?(?=(\d{1,2} \w+)|$)/g);  // Extraemos eventos

                            if (eventosSeparados) {
                                eventosSeparados.forEach(evento => {
                                    let eventoLimpio = evento.replace(/\b(más|undefined)\b/g, "").trim();  // Eliminamos "más" o "undefined"
                                    let partes = eventoLimpio.split(" ");  // Separamos por espacio

                                    if (partes.length > 1) {
                                        let dia = partes[0] + " " + partes[1];  // Día (ej: "12 marzo")
                                        let descripcion = partes.slice(2).join(" ");  // El resto es la descripción

                                        if (descripcion.length > 0) {
                                            if (!eventosPorDia[dia]) {
                                                eventosPorDia[dia] = new Set();  
                                            }
                                            eventosPorDia[dia].add(descripcion);
                                        }
                                    }
                                });
                            }
                        }
                    }

                    let resultado = "";
                    Object.keys(eventosPorDia).sort().forEach(dia => {
                        resultado += `📅 ${dia}:\n`;  
                        Array.from(eventosPorDia[dia]).forEach(evento => {
                            resultado += `    ➤ ${evento}\n`;  
                        });
                    });

                    return resultado;
                } else {
                    return "No se encontró la tabla.";
                }
            }
            return extraerEventos();  
        """

        # Ejecutamos el script en el navegador usando Selenium
        tareas_pendientes_calendario = driver.execute_script(script_tareas_pendientes)
        tareas_pendientes_calendario = tareas_pendientes_calendario.replace("\n", "")
        tareas_pendientes_calendario = calendario_moodle(tareas_pendientes_calendario)
        tareas_pendientes_calendario = tareas_pendientes_calendario.replace("➤", "")
        send_email(tareas_pendientes_calendario, email)

    except:
        tareas_pendientes_calendario = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.alert.alert-danger'))
        )

        mensaje_error = tareas_pendientes_calendario.text
        return {"mensaje_error": mensaje_error}

    return {"tarea_pendiente", tareas_pendientes_calendario}