import re
import datetime
import calendar

def obtener_dia_del_mes(dia_del_mes):
    dia_del_mes = int(dia_del_mes)
    fecha_actual = datetime.datetime.now().date()
    fecha_dia = datetime.date(fecha_actual.year, fecha_actual.month, dia_del_mes) 
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
    
    dia_semana_espanol = dias_semana_esp.get(dia_semana_ingles, "Día no válido")
    
    if fecha_dia > fecha_actual:
        dias_faltantes = (fecha_dia - fecha_actual).days
        tiempo_entrega = f"Faltan {dias_faltantes} días para la entrega de esta actividad."
    elif fecha_dia == fecha_actual:
        tiempo_entrega = "Hoy vence esta actividad."
    else:
        dias_faltantes = ((fecha_dia - fecha_actual).days)*-1
        tiempo_entrega = f"Venció hace {dias_faltantes} días la entrega de esta actividad."
    
    return dia_semana_espanol, tiempo_entrega


def calendario_moodle(text):
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

    actividades_con = []
    
    fecha_actual = datetime.datetime.now()
    _, num_dias_mes = calendar.monthrange(fecha_actual.year, fecha_actual.month)
    dias_del_mes = list(range(1, num_dias_mes + 1))  

    for linea in lineas_limpias:
        numero_encontrado = re.search(r"\d+", linea)
        if numero_encontrado:
            dia_del_mes = int(numero_encontrado.group())
            if 1 <= dia_del_mes <= num_dias_mes:
                dia_semana_espanol, tiempo_entrega = obtener_dia_del_mes(dia_del_mes)
                actividades_con.append((dia_del_mes, dia_semana_espanol, tiempo_entrega, linea))
                if dia_del_mes in dias_del_mes:
                    dias_del_mes.remove(dia_del_mes)

    actividades_con.sort(key=lambda x: x[0])

    calendario = ""  

    for dia in range(1, num_dias_mes + 1):
        actividad_encontrada = False
        for actividad in actividades_con:
            if actividad[0] == dia:
                calendario += f"✦ {actividad[1]} {actividad[0]} - {actividad[2]} - {actividad[3]}\n"
                actividad_encontrada = True
                break
        if not actividad_encontrada:
            dia_semana_espanol, tiempo_entrega = obtener_dia_del_mes(dia)
            calendario += f"☆ {dia_semana_espanol} {dia} - Día sin actividades.\n"

    return calendario