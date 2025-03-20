from module.time.time import obtener_mes_texto, obtener_dia_numero

def cuerpo_html(subject, body, tareas_pendientes, calificaciones):
    dia_actual = obtener_dia_numero()
    mes = obtener_mes_texto()

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

        if contador < dia_actual:
            estilo = "style='background-color: #fafafa; color: #000000; border: 1px solid #e0e0e0;'"
        elif contador == dia_actual:
            dia_mes = f"{dia_mes} - <strong>(¡Hoy!)</strong>"
            estilo = "style='background-color: #f0faff; color: #000000; border: 1px solid #a3c4f7;'"
        else:
            estilo = "style='background-color: #f7fff7; color: #000000; border: 1px solid #b7e1b1;'"

        if not tarea_asignada and contador >= dia_actual and "Día sin actividades" not in dia_mes:
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
            <title>{subject}</title>
            <style>
                /* Diseño general del cuerpo */
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f7f8fa;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    color: #333;
                }}

                /* Contenedor principal */
                .container {{
                    background-color: #ffffff;
                    border-radius: 10px;
                    width: 90%;
                    max-width: 800px;
                    padding: 40px;
                    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
                    text-align: center;
                    margin: 20px;
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

                ul {{
                    text-align: left;
                    margin-top: 30px;
                    font-size: 1.1rem;
                    color: #555;
                }}

                ul li {{
                    margin-bottom: 10px;
                    padding-left: 25px;
                    position: relative;
                }}

                ul li:before {{
                    content: "✔";
                    position: absolute;
                    left: 0;
                    color: #2ecc71;
                }}

                .footer {{
                    font-size: 0.9rem;
                    color: #7f8c8d;
                    margin-top: 30px;
                    text-align: center;
                    border-top: 1px solid #e0e0e0;
                    padding-top: 20px;
                }}

                .footer a {{
                    color: #2c3e50;
                    text-decoration: none;
                }}

                .footer a:hover {{
                    text-decoration: underline;
                }}

                /* Estilo de la tabla de calificaciones */
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 30px;
                }}

                th, td {{
                    border: 1px solid #ddd;
                    padding: 10px;
                    text-align: left;
                }}

                th {{
                    background-color: #2c3e50;
                    color: white;
                }}

                tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>

        <body>
            <div class="container">
                <h1>{subject}</h1>
                <p><strong>{body}</strong></p>

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

                <h2>Proxima tarea a entregar</h2>
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

                <h2>Calendario de {mes}</h2>
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

            </div>
        </body>

        </html>
    """