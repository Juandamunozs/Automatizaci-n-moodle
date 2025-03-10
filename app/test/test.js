//TODO: Alerta de logueo

const login_error = document.getElementsByClassName('alert alert-danger');

// Verificar si existe al menos un elemento con esas clases
if (login_error.length > 0) {
    // Imprimir el texto del primer elemento con la clase 'alert alert-danger'
    console.log(login_error[0].textContent);
}

//TODO: Extraer tareas de calendario

let tabla = document.querySelector(".calendarmonth.calendartable.mb-0");

if (tabla) {
    let filas = tabla.getElementsByTagName("tr");
    let eventosPorDia = {}; 

    for (let i = 0; i < filas.length; i++) {
        let celdas = filas[i].getElementsByTagName("td");

        for (let j = 0; j < celdas.length; j++) {
            let textoLimpio = celdas[j].textContent.replace(/\s+/g, " ").trim();
            
            // Captura cualquier fecha en formato "DÍA MES" seguido de una descripción
            let coincidencias = textoLimpio.match(/(\d{1,2} \w+)(.*?)(?=(\d{1,2} \w+|$))/g);
            
            if (coincidencias) {
                coincidencias.forEach(coincidencia => {
                    let partes = coincidencia.trim().split(" ");
                    let dia = `${partes[0]} ${partes[1]}`; // Día y mes
                    let descripcion = partes.slice(2).join(" ").trim(); // Descripción del evento

                    // Filtramos eventos vacíos o irrelevantes
                    if (descripcion && !descripcion.toLowerCase().includes("sin eventos")) {
                        if (!eventosPorDia[dia]) {
                            eventosPorDia[dia] = new Set();
                        }
                        eventosPorDia[dia].add(descripcion);
                    }
                });
            }
        }
    }

    // Ordenar eventos por día y mostrar en formato claro
    console.log("\n📅 **Eventos organizados por fecha:**\n");
    Object.keys(eventosPorDia)
        .sort((a, b) => {
            let [diaA, mesA] = a.split(" ");
            let [diaB, mesB] = b.split(" ");
            return parseInt(diaA) - parseInt(diaB); // Orden numérico
        })
        .forEach(dia => {
            console.log(`📆 ${dia}:`);
            console.log(`   ➤ ${Array.from(eventosPorDia[dia]).join("\n   ➤ ")}`);
        });

} else {
    console.log("❌ No se encontró la tabla.");
}

// script_tareas_pendientes = """
// function extraerEventos() {
//     let tabla = document.querySelector(".calendarmonth.calendartable.mb-0");

//     if (tabla) {
//         let filas = tabla.getElementsByTagName("tr");
//         let eventosPorDia = {};  // Objeto para almacenar eventos sin repetir

//         for (let i = 0; i < filas.length; i++) {
//             let celdas = filas[i].getElementsByTagName("td");

//             for (let j = 0; j < celdas.length; j++) {
//                 let textoLimpio = celdas[j].textContent.replace(/\s+/g, " ").trim();  // Limpiamos espacios extra
//                 let eventosSeparados = textoLimpio.match(/(\d{1,2} \w+.*?)?(?=(\d{1,2} \w+)|$)/g);  // Extraemos eventos

//                 if (eventosSeparados) {
//                     eventosSeparados.forEach(evento => {
//                         let eventoLimpio = evento.replace(/\b(más|undefined)\b/g, "").trim();  // Eliminamos "más" o "undefined"
//                         let partes = eventoLimpio.split(" ");  // Separamos por espacio

//                         if (partes.length > 1) {
//                             let dia = partes[0] + " " + partes[1];  // Día (ej: "12 marzo")
//                             let descripcion = partes.slice(2).join(" ");  // El resto es la descripción

//                             if (descripcion.length > 0) {
//                                 if (!eventosPorDia[dia]) {
//                                     eventosPorDia[dia] = new Set();  
//                                 }
//                                 eventosPorDia[dia].add(descripcion);
//                             }
//                         }
//                     });
//                 }
//             }
//         }

//         let resultado = "";
//         Object.keys(eventosPorDia).sort().forEach(dia => {
//             resultado += `📅 ${dia}:\n`;  
//             Array.from(eventosPorDia[dia]).forEach(evento => {
//                 resultado += `    ➤ ${evento}\n`;  
//             });
//         });

//         return resultado;
//     } else {
//         return "No se encontró la tabla.";
//     }
// }
// return extraerEventos();  
// """

