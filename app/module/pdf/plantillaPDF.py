from module.time.time import obtener_hora_completa, obtener_dia_texto, obtener_dia_numero, obtener_anio, obtener_mes_numero, obtener_mes_texto

def cuerpo_html(tareas_pendientes, email, calificaciones):
    hora = obtener_hora_completa()
    dia_texto = obtener_dia_texto()
    dia_numero = obtener_dia_numero()
    anio_numero = obtener_anio()
    mes_texto = obtener_mes_texto()

    fecha_completa = f"{dia_texto} {dia_numero} de {mes_texto} del {anio_numero} a las {hora}"

    # Crear las filas de la tabla para las calificaciones
    filas_calificaciones = ""
    for calificacion in calificaciones:
        filas_calificaciones += f"""
        <tr>
            <td>{calificacion['curso']}</td>
            <td>{calificacion['nota']}</td>
        </tr>
        """
    
    # Dividimos el texto por saltos de línea y eliminamos las cadenas vacías
    calendarios_mes = [linea for linea in tareas_pendientes.split('\n') if linea != ""]

    filas_calendario = ""
    fila_proxima_tarea = ""
    tarea_asignada = False

    for contador, dia_mes in enumerate(calendarios_mes, start=1):  
        if "Día sin actividades" in dia_mes:
            dia_mes = dia_mes.replace("Día sin actividades", "Día sin actividades")
        else:
            dia_mes = f"<strong>{dia_mes}</strong>"

        if contador < dia_numero:
            estilo = "style='background-color: #fafafa; color: #000000; border: 1px solid #e0e0e0;'"
        elif contador == dia_numero:
            dia_mes = f"{dia_mes} - <strong>(¡Hoy!)</strong>"
            estilo = "style='background-color: #f0faff; color: #000000; border: 1px solid #a3c4f7;'"
        else:
            estilo = "style='background-color: #f7fff7; color: #000000; border: 1px solid #b7e1b1;'"

        if not tarea_asignada and contador >= dia_numero and "Día sin actividades" not in dia_mes:
            fila_proxima_tarea += f"""
            <tr {estilo}>
                <td>{dia_mes}</td>
            </tr>
            """
            tarea_asignada = True  

        filas_calendario += f"""
        <tr {estilo}>
            <td>{dia_mes}</td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="es">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tareas pendientes</title>
        <style>
            /* Diseño general del cuerpo */
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f7f8fa;
                display: flex;
                justify-content: center;
                align-items: flex-start;
                color: #333;
            }}

            h1 {{
                font-size: 2.5rem;
                color: #2c3e50;
                margin-bottom: 20px;
                font-weight: 600;
            }}

            p {{
                font-size: 1.1rem;
                color: #555;
                line-height: 1.8;
                margin-bottom: 20px;
            }}

            .highlight {{
                font-weight: 600;
                color: #2ecc71;
            }}

            /* Estilo de la tabla */
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 30px;
            }}

            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}

            th {{
                background-color: #2c3e50;
                color: white;
            }}

            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}

            tr:nth-child(odd) {{
                background-color: #ffffff;
            }}

        </style>
    </head>

    <body>
        <div class="container">

            <h2>Calificaciones del semestre</h2>
            <table>
                <thead>
                    <tr>
                        <th>Curso</th>
                        <th>Nota</th>
                    </tr>
                </thead>
                <tbody>
                    {filas_calificaciones}
                </tbody>
            </table>

            <h2>Próxima tarea a entregar</h2>
            <table>
                <thead>
                    <tr>
                        <th>Actividad</th>
                    </tr>
                </thead>
                <tbody>
                    {fila_proxima_tarea}
                </tbody>
            </table>

            <h2>Calendario de {mes_texto}</h2>
            <table>
                <thead>
                    <tr>
                        <th>Actividades</th>
                    </tr>
                </thead>
                <tbody>
                    {filas_calendario}
                </tbody>
            </table>

            <p>Informe generado el <strong>{fecha_completa}</strong></p>

    </body>

    </html>
    """
