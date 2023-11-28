const marca = document.getElementById('marca_cb');
const modelo = document.getElementById('modelo_cb');
const ayno = document.getElementById('ayno_cb');
const pref = document.getElementById('pref_cb');
const li_contacto = document.getElementById('li_contacto');
const button = document.getElementById('botonBuscar');
var firstTime = true;
var id_consulta = '';

if (li_contacto != null){
    li_contacto.addEventListener('click', scrollToBottom)
}

function scrollToBottom() {
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
    });
}

marca.addEventListener('change', function() {
    var data = {
        'Valor': this.value,
        'Modo': 1
    };

    fetch('/busqueda/cbb', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        var modelos = data.Modelos;
        var aynos = data.Aynos;

        while (modelo.firstChild) {
            modelo.removeChild(modelo.firstChild);
        }

        while (ayno.firstChild) {
            ayno.removeChild(ayno.firstChild);
        }

        for (var i = 0; i < modelos.length ; i++){
            var opcion = document.createElement('option');
            opcion.text = modelos[i];
            opcion.value = modelos[i];
            modelo.appendChild(opcion);
        }

        for (var i = 0; i < aynos.length ; i++){
            var opcion = document.createElement('option');
            opcion.text = aynos[i];
            opcion.value = aynos[i];
            ayno.appendChild(opcion);
        }
    });
});

modelo.addEventListener('change', function() {
    var data = {
        'Valor': [marca.value, this.value],
        'Modo': 2
    };

    fetch('/busqueda/cbb', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        var aynos = data.Aynos;

        while (ayno.firstChild) {
            ayno.removeChild(ayno.firstChild);
        }

        for (var i = 0; i < aynos.length ; i++){
            var opcion = document.createElement('option');
            opcion.text = aynos[i];
            opcion.value = aynos[i];
            ayno.appendChild(opcion);
        }
    });
});

document.getElementById('comentForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var comentario = document.getElementById('comentario').value;
    var valoracion = document.getElementById('valoracion').value;

    var data = {
        'comentario': comentario,
        'valoracion': valoracion
    };

    fetch('/busqueda/enviar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => response.json())
      .then(data => console.log(data));
    cerrarPopup()
});

button.addEventListener('click', function() {
    buscarLlanta()
    if (firstTime){
        setTimeout(function() {
            var popup = document.getElementById('popupForm');
            popup.style.display = 'block';
        }, 5000);
        firstTime = false;
    }
});

function cerrarPopup() {
    document.getElementById('popupForm').style.display = 'none';
}

function buscarLlanta() {
    var data = {
        'Marca':marca.value,
        'Modelo':modelo.value,
        'Ayno': ayno.value,
        'Pref': pref.value,
        'P': firstTime,
        'Id': id_consulta
    };

    const resultadosDer = document.getElementById('resultados_der');
    const resultadosIzq = document.getElementById('resultados_izq');

    fetch('/busqueda/buscar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => response.json())
      .then(data => {
            id_consulta = data.id;
            
            const modo = data.Modo;
            while (resultadosIzq.firstChild) {
                resultadosIzq.removeChild(resultadosIzq.firstChild);
            }
            while (resultadosDer.firstChild) {
                resultadosDer.removeChild(resultadosDer.firstChild);
            }
            if (modo == '1m'){
                const precios = data.Precios;
                const medida = data.Medida;
                const marcas = data.Marcas;
                const durabilidades = data.Durabilidades;

                const locLlantas = document.getElementById('locLlanta');
                locLlantas.innerHTML = `
                    <div class="detalles" id="locLlanta">
                        <p>Localización de llantas:</p>
                        <p>Ambas</p>
                        <hr/>
                    </div>
                `;

                for(var i = 0; i < Math.floor(precios.length/2); i++){
                    var nuevoResultado = document.createElement('div');
                    nuevoResultado.className = "resultado";
                    nuevoResultado.id = "resultado" + i;
                    nuevoResultado.innerHTML = `
                        <div class="detalles">
                            <p>Medidas: ${medida[0]}</p>
                            <p>Precio: $${precios[i]}</p>
                            <p>Marca: ${marcas[i]}</p>
                            <p>Durabilidad: ${durabilidades[i]}</p>
                            <hr/>
                        </div>
                    `;
                    resultadosIzq.appendChild(nuevoResultado);
                }
                for(var i = Math.floor(precios.length/2); i < precios.length; i++){
                    var nuevoResultado = document.createElement('div');
                    nuevoResultado.className = "resultado";
                    nuevoResultado.id = "resultado" + i;
                    nuevoResultado.innerHTML = `
                        <div class="detalles">
                            <p>Medidas: ${medida[0]}</p>
                            <p>Precio: $${precios[i]}</p>
                            <p>Marca: ${marcas[i]}</p>
                            <p>Durabilidad: ${durabilidades[i]}</p>
                            <hr/>
                        </div>
                    `;
                    resultadosDer.appendChild(nuevoResultado);
                }
            }else{
                var precios = data.PreciosD;
                var medida = data.MedidaD;
                var marcas = data.MarcasD;
                var durabilidades = data.DurabilidadesD;

                const locLlantas = document.getElementById('locLlanta');
                locLlantas.innerHTML = `
                    <div class="detalles" id="locLlanta">
                        <p>Localización de llantas:</p>
                        <p>&lt- Delantera | Trasera -&gt</p>
                        <hr/>
                    </div>
                `;

                for(var i = 0; i < precios.length; i++){
                    var nuevoResultado = document.createElement('div');
                    nuevoResultado.className = "resultado";
                    nuevoResultado.id = "resultado" + i;
                    nuevoResultado.innerHTML = `
                        <div class="detalles">
                            <p>Medidas: ${medida[0]}</p>
                            <p>Precio: $${precios[i]}</p>
                            <p>Marca: ${marcas[i]}</p>
                            <p>Durabilidad: ${durabilidades[i]}</p>
                            <hr/>
                        </div>
                    `;
                    resultadosIzq.appendChild(nuevoResultado);
                }
                precios = data.PreciosT;
                medida = data.MedidaT;
                marcas = data.MarcasT;
                durabilidades = data.DurabilidadesT;
                console.log(precios, medida, marcas, durabilidades)
                console.log(data.PreciosD.length, precios.length + data.PreciosD.length)
                for(var i = data.PreciosD.length; i < precios.length + data.PreciosD.length; i++){
                    var nuevoResultado = document.createElement('div');
                    nuevoResultado.className = "resultado";
                    nuevoResultado.id = "resultado" + i;
                    nuevoResultado.innerHTML = `
                        <div class="detalles">
                            <p>Medidas: ${medida[0]}</p>
                            <p>Precio: $${precios[i]}</p>
                            <p>Marca: ${marcas[i]}</p>
                            <p>Durabilidad: ${durabilidades[i]}</p>
                            <hr/>
                        </div>
                    `;
                    resultadosDer.appendChild(nuevoResultado);
                }
            }
      });
}