const barCtx = document.getElementById("barChart").getContext("2d");
const pieCtx = document.getElementById("pieChart").getContext("2d");
let barChart = null;
let pieChart = null;

// Genera un conjunto de colores para cada barra y sección de la torta
function generarColores(cantidad) {
    const colores = [
        "rgba(255, 182, 193, 0.8)",  /* Rosa pastel */
        "rgba(173, 216, 230, 0.8)",  /* Azul claro pastel */
        "rgba(255, 255, 224, 0.8)",  /* Amarillo claro pastel */
        "rgba(152, 251, 152, 0.8)",  /* Verde claro pastel */
        "rgba(200, 162, 200, 0.8)",  /* Púrpura claro pastel */
        "rgba(255, 204, 204, 0.8)",  /* Naranja claro pastel */
        "rgba(255, 239, 0, 0.8)",    /* Amarillo suave */
        "rgba(144, 238, 144, 0.8)",  /* Verde suave */
        "rgba(221, 160, 221, 0.8)",  /* Lavanda claro */
        "rgba(224, 255, 255, 0.8)"   /* Aguamarina suave */
    ];
    const bordes = [
       "rgba(255, 105, 180, 0.8)",  /* Rosa fuerte */
        "rgba(0, 191, 255, 0.8)",    /* Azul brillante */
        "rgba(255, 255, 102, 0.8)",   /* Amarillo intenso */
        "rgba(0, 128, 0, 0.8)",       /* Verde fuerte */
        "rgba(128, 0, 128, 0.8)",     /* Púrpura fuerte */
        "rgba(255, 140, 0, 0.8)",     /* Naranja intenso */
        "rgba(255, 215, 0, 0.8)",     /* Amarillo dorado */
        "rgba(34, 139, 34, 0.8)",     /* Verde bosque */
        "rgba(128, 0, 128, 0.8)",     /* Púrpura profundo */
        "rgba(64, 224, 208, 0.8)"      /* Aguamarina brillante */
    ];

    return {
        backgroundColors: colores.slice(0, cantidad),
        borderColors: bordes.slice(0, cantidad),
    };
}

function actualizarGraficos(datos) {
    const especies = datos.map((item) => item.Especie);
    const registros = datos.map((item) => item.Registros);
    const enlaces = datos.map((item) => item.CBC);  // Traer los enlaces de cada especie

    // Generar colores para la cantidad de especies
    const { backgroundColors, borderColors } = generarColores(especies.length);

    // Destruir los gráficos previos si existen
    if (barChart) {
        barChart.destroy();
    }
    if (pieChart) {
        pieChart.destroy();
    }

    // Crear gráfico de barras 
    barChart = new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: especies,
            datasets: [{
                label: 'Registros por Especie',
                data: registros,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            scales: {
                x: {
                    beginAtZero: true 
                }
            },
            onClick: function (evt, activeElements) {
                if (activeElements.length > 0) {
                    const index = activeElements[0].index;
                    const enlace = enlaces[index];
                    if (enlace && enlace !== 'NA') {
                        window.open(enlace, '_blank'); 
                    }
                }
            }
        }
    });

    // Crear gráfico de torta con labels a la derecha
    pieChart = new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: especies,
            datasets: [{
                label: 'Registros por Especie',
                data: registros,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                legend: {
                    position: 'right',  // Mueve las etiquetas a la derecha
                    labels: {
                        boxWidth: 20  // Tamaño del recuadro de color en la leyenda
                    }
                }
            },
            onClick: function (evt, activeElements) {
                if (activeElements.length > 0) {
                    const index = activeElements[0].index;
                    const enlace = enlaces[index];
                    if (enlace && enlace !== 'NA') {
                        window.open(enlace, '_blank');  // Abre el enlace en una nueva pestaña
                    }
                }
            }
        }
    });
}

function cargarDatos() {
    const departamento = document.getElementById('departamento').value;
    const reino = document.getElementById('reino').value;
    const limite = document.getElementById('limite').value;

    fetch(`/filtrar-datos?departamento=${departamento}&reino=${reino}&limite=${limite}`)
        .then(response => response.json())
        .then(data => actualizarGraficos(data));
}

document.getElementById('departamento').addEventListener('change', cargarDatos);
document.getElementById('reino').addEventListener('change', cargarDatos);
document.getElementById('limite').addEventListener('change', cargarDatos);

// Cargar datos iniciales
cargarDatos();
