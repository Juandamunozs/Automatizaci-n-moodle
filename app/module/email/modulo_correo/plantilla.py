# from env.env import dir_logo

def cuerpo_html(subject, body, tareas_pendientes):
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

        /* Estilo de la imagen */
        .footer img {{
            margin-top: 20px;
            width: 150px;
            border-radius: 8px;
            transition: all 0.3s ease;
        }}

        .footer img:hover {{
            transform: scale(1.05);
        }}
    </style>
</head>

<body>
    <div class="container">
        <h1>{subject}</h1>
        <p>{body}</p>

        <div style="text-align: left; margin-top: 30px; font-size: 1.1rem;">
            <ul>
                <strong>{tareas_pendientes}</strong>
            </ul>
        </div>
    </div>
</body>

</html>
    """
