import re
import datetime
import calendar

def obtener_dia_del_mes(dia_del_mes):
    # Asegurarse de que el parámetro es un número entero
    dia_del_mes = int(dia_del_mes)
    
    # Obtener la fecha actual (sin la hora)
    fecha_actual = datetime.datetime.now().date()  # Solo la fecha (sin hora)
    
    # Crear una fecha con el día del mes proporcionado en el mes y año actuales
    fecha_dia = datetime.date(fecha_actual.year, fecha_actual.month, dia_del_mes)  # Solo la fecha (sin hora)
    
    # Obtener el nombre del día de la semana en inglés
    dia_semana_ingles = fecha_dia.strftime("%A") 
    
    # Diccionario para traducir el día de la semana de inglés a español
    dias_semana_esp = {
        'Monday': 'Lunes',
        'Tuesday': 'Martes',
        'Wednesday': 'Miércoles',
        'Thursday': 'Jueves',
        'Friday': 'Viernes',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    
    # Devolver el día de la semana en español
    dia_semana_espanol = dias_semana_esp.get(dia_semana_ingles, "Día no válido")
    
    # Calcular la diferencia en días entre la fecha actual y la fecha del día del mes
    if fecha_dia > fecha_actual:
        dias_faltantes = (fecha_dia - fecha_actual).days
        tiempo_entrega = f"Faltan {dias_faltantes} días para el día {dia_del_mes} del mes."
    elif fecha_dia == fecha_actual:
        tiempo_entrega = "Hoy vence esta actividad."
    else:
        dias_faltantes = ((fecha_dia - fecha_actual).days)*-1
        tiempo_entrega = f"Venció hace {dias_faltantes} días."
    
    # Retorna el día en español y el mensaje de faltante
    return dia_semana_espanol, tiempo_entrega


def eventos(text):
    # Reemplazar '📅' por saltos de línea, para separar las fechas en nuevas líneas
    texto_formateado = text.replace('📅', '\n')
    
    # Expresiones regulares para detectar ciertos patrones
    patron_eliminar_lineas_con_numeros = r"^.*➤\s*\d+.*$"  
    patron_eliminar_lineas_con_eventos = r"^.*➤\s*eventos.*$"  
    patron_eliminar_lineas_con_dias = r"^.*➤\s*(lunes|martes|miércoles|jueves|viernes|sábado|domingo).*"
    patron_eliminar_evento_con_dia = r"^.*➤\s*evento,\s*(lunes|martes|miércoles|jueves|viernes|sábado|domingo),.*$"

    # Eliminar todas las líneas que contienen ➤ seguido de un número
    texto_limpio = re.sub(patron_eliminar_lineas_con_numeros, "", texto_formateado, flags=re.MULTILINE)

    # Eliminar las líneas que contienen ➤ eventos
    texto_limpio = re.sub(patron_eliminar_lineas_con_eventos, "", texto_limpio, flags=re.MULTILINE)

    # Eliminar las líneas que contienen ➤ seguido de un día de la semana
    texto_limpio = re.sub(patron_eliminar_lineas_con_dias, "", texto_limpio, flags=re.MULTILINE)

    # Eliminar las lineas que contienen ➤ evento, domingo, 
    texto_limpio = re.sub(patron_eliminar_evento_con_dia, "", texto_limpio, flags=re.MULTILINE)

    # Dividir el texto limpio en líneas
    lineas = texto_limpio.splitlines()

    # Eliminar líneas vacías o que solo contienen espacios en blanco
    lineas_limpias = [linea for linea in lineas if linea.strip() != ""]

    # Lista para almacenar las actividades y los días válidos del mes
    actividades_con = []
    
    # Obtener el número de días que tiene el mes actual
    fecha_actual = datetime.datetime.now()
    _, num_dias_mes = calendar.monthrange(fecha_actual.year, fecha_actual.month)
    dias_del_mes = list(range(1, num_dias_mes + 1))  # Todos los días del mes (1 a num_dias_mes)

    # Recorremos la lista de líneas
    for linea in lineas_limpias:
        # Buscar el primer número en cada línea (día del mes)
        numero_encontrado = re.search(r"\d+", linea)
        if numero_encontrado:
            dia_del_mes = int(numero_encontrado.group())
            # Verificamos que el día esté dentro del rango de 1 a num_dias_mes
            if 1 <= dia_del_mes <= num_dias_mes:
                dia_semana_espanol, tiempo_entrega = obtener_dia_del_mes(dia_del_mes)
                actividades_con.append((dia_del_mes, dia_semana_espanol, tiempo_entrega, linea))
                # Eliminar este día de la lista de días del mes (porque ya tiene una actividad)
                if dia_del_mes in dias_del_mes:
                    dias_del_mes.remove(dia_del_mes)

    # Ordenar las actividades con fechas válidas por día
    actividades_con.sort(key=lambda x: x[0])

    calendario = ""  # Inicializamos la variable calendario como una cadena vacía

    for dia in range(1, num_dias_mes + 1):
        # Si el día tiene actividad, mostramos la información de la actividad
        actividad_encontrada = False
        for actividad in actividades_con:
            if actividad[0] == dia:
                calendario += f"{actividad[1]} {actividad[0]} - {actividad[2]} - {actividad[3]}\n"
                actividad_encontrada = True
                break
        # Si no se encontró actividad para ese día, mostramos que no hay actividad
        if not actividad_encontrada:
            dia_semana_espanol, tiempo_entrega = obtener_dia_del_mes(dia)
            calendario += f"{dia_semana_espanol} {dia} - Día sin actividades.\n"

    # Imprimir todo el calendario al final
    print(calendario)


     
#Texto prueba
text = """

        Sin:    ➤ eventos, sábado,📅 1 evento,:    ➤ domingo,    ➤ lunes,    ➤ martes,    ➤ viernes,    ➤ miércoles,📅 1 marzo:    ➤ 1📅 10 Asistencia:    ➤ a sesión sincrónica más Asistencia a sesión sincrónica📅 10 marzo:    ➤ 10📅 11 Sin:    ➤ eventos, martes,📅 11 marzo:    ➤ 11📅 12 Sin:    ➤ eventos, miércoles,📅 12 marzo:    ➤ 12📅 13 Sin:    ➤ eventos, jueves,📅 13 marzo:    ➤ 13📅 14 Asistencia:    ➤ a sesión sincrónica más Asistencia a sesión sincrónica📅 14 marzo:    ➤ 14📅 15 Vencimiento:    ➤ de Actividad No.3: Mapa conceptual: herramientas digitales y redes sociales para el aprendizaje Vencimiento de Actividad 4: Encuesta. ¿Qué tan buena es su administración del tiempo? Vencimiento de Actividad 5: Relaciones significativas más Vencimiento de Actividad No.3: Mapa conceptual: herramientas digitales y redes sociales para el aprendizaje Vencimiento de Actividad 4: Encuesta. ¿Qué tan buena es su administración del tiempo? Vencimiento de Actividad 5: Relaciones significativas📅 15 marzo:    ➤ 15📅 16 Sin:    ➤ eventos, domingo,📅 16 marzo:    ➤ 16📅 17 Asistencia:    ➤ a sesión sincrónica más Asistencia a sesión sincrónica📅 17 marzo:    ➤ 17📅 18 Sin:    ➤ eventos, martes,📅 18 marzo:    ➤ 18📅 19 Sin:    ➤ eventos, miércoles,📅 19 marzo:    ➤ 19📅 2 1:    ➤ evento, domingo,📅 2 Se:    ➤ cierra Actividad📅 2 marzo:    ➤ 2📅 2 más:    ➤ Se cierra Actividad📅 20 Sin:    ➤ eventos, jueves,📅 20 marzo:    ➤ 20📅 21 Asistencia:    ➤ a sesión sincrónica más Asistencia a sesión sincrónica📅 21 marzo:    ➤ 21📅 22 Sin:    ➤ eventos, sábado,📅 22 marzo:    ➤ 22📅 23 Sin:    ➤ eventos, domingo,📅 23 marzo:    ➤ 23📅 24 Asistencia:    ➤ a sesión sincrónica más Asistencia a sesión sincrónica📅 24 marzo:    ➤ 24📅 25 Sin:    ➤ eventos, martes,📅 25 marzo:    ➤ 25📅 26 Asistencia:    ➤ a sesión sincrónica más Asistencia a sesión sincrónica📅 26 marzo:    ➤ 26📅 27 Sin:    ➤ eventos, jueves,📅 27 marzo:    ➤ 27📅 28 Asistencia:    ➤ a sesión sincrónica más Asistencia a sesión sincrónica📅 28 marzo:    ➤ 28📅 29 Sin:    ➤ eventos, sábado,📅 29 marzo:    ➤ 29📅 3 Asistencia:    ➤ a sesión sincrónica más Asistencia a sesión sincrónica📅 3 eventos,:    ➤ sábado,📅 3 marzo:    ➤ 3📅 30 Sin:    ➤ eventos, domingo,📅 30 marzo:    ➤ 30📅 31 Asistencia:    ➤ a sesión sincrónica más Asistencia a sesión sincrónica📅 31 marzo:    ➤ 31📅 4 Se:    ➤ abre Actividad No. 3: Aprendiendo Álgebra más Se abre Actividad No. 3: Aprendiendo Álgebra📅 4 marzo:    ➤ 4📅 5 Sin:    ➤ eventos, miércoles,📅 5 marzo:    ➤ 5📅 6 Sin:    ➤ eventos, jueves,📅 6 marzo:    ➤ 6📅 7 Asistencia:    ➤ a sesión sincrónica más Asistencia a sesión sincrónica📅 7 marzo:    ➤ 7📅 8 Sin:    ➤ eventos, sábado,📅 8 marzo:    ➤ 8📅 9 Se:    ➤ cierra Actividad No. 3: Aprendiendo Álgebra más Se cierra Actividad No. 3: Aprendiendo Álgebra📅 9 marzo:    ➤ 9

    """

eventos(text)