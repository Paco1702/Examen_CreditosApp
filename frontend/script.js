document.getElementById('creditoForm').addEventListener('submit', function(event) {
    event.preventDefault();

    let data = {
        cliente: document.getElementById('cliente').value,
        monto: parseFloat(document.getElementById('monto').value),
        tasa_interes: parseFloat(document.getElementById('tasa_interes').value),
        plazo: parseInt(document.getElementById('plazo').value),
        fecha_otorgamiento: document.getElementById('fecha_otorgamiento').value
    };

    axios.post('http://127.0.0.1:5000/creditos', data)
        .then(() => {
            document.getElementById('creditoForm').reset();
            cargarCreditos();
        })
        .catch(err => console.error(err));
});

function cargarCreditos() {
    axios.get('http://127.0.0.1:5000/creditos')
        .then(res => {
            let tbody = document.getElementById('creditosTable');
            tbody.innerHTML = '';
            res.data.forEach(credito => {
                tbody.innerHTML += `<tr>
                    <td>${credito.id}</td>
                    <td>${credito.cliente}</td>
                    <td>${credito.monto.toFixed(2)}</td>
                    <td>${credito.tasa_interes.toFixed(2)}%</td>
                    <td>${credito.plazo} meses</td>
                    <td>${credito.fecha_otorgamiento}</td>
                    <td><button class="btn btn-danger btn-sm" onclick="eliminarCredito(${credito.id})">Eliminar</button></td>
                </tr>`;
            });
        })
        .catch(err => console.error(err));
}

function eliminarCredito(id) {
    if (confirm("¿Estás seguro de eliminar este crédito?")) {
        axios.delete(`http://127.0.0.1:5000/creditos/${id}`)
            .then(() => cargarCreditos())
            .catch(err => console.error(err));
    }
}

// Función para generar la gráfica
function generarGrafico() {
    axios.get('http://127.0.0.1:5000/creditos')
        .then(res => {
            let datos = res.data;
            let clientes = datos.map(c => c.cliente);
            let montos = datos.map(c => c.monto);

            let canvas = document.getElementById('grafico');
            canvas.parentNode.replaceChild(canvas.cloneNode(), canvas); // Limpia el gráfico anterior

            let ctx = document.getElementById('grafico').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: clientes,
                    datasets: [{
                        label: 'Montos de Créditos',
                        data: montos,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        })
        .catch(err => console.error(err));
}

// Cargar créditos al iniciar
cargarCreditos();

// Llama la función cuando se abra el modal
document.getElementById('graficoModal').addEventListener('shown.bs.modal', generarGrafico);
