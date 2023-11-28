const li_contacto = document.getElementById('li_contacto');
const opciones = document.getElementById('opciones');
const marca = document.getElementById('marca_cb');
const modelo = document.getElementById('modelo_cb');
const medida = document.getElementById('medida_cb');
const marcaL = document.getElementById('marcaL_cb');
var llantaUpdate = false;
var fase_popup = 1;
var tieneMarca = false;
var valorMarca;
var tieneModelo = false;
var valorModelo;
var tieneMarcaL = false;
var valorMarcaL;
var tieneMedidaL = false;
var valorMedidaL;
var valorDurabilidad;
var popup_container = document.getElementById('popupForm');
var popup = document.getElementById('comentForm');
var tablaDatos = document.getElementById('tablaDatos');
var boton_u = document.getElementById('boton_u');
var boton_c = document.getElementById('boton_c');
var boton_d = document.getElementById('boton_d');
var $pager = null;
var selectedTab = null;

if (li_contacto != null){
    li_contacto.addEventListener('click', scrollToBottom)
}
if (opciones != null){
    opciones.addEventListener('change', buscarOpciones);
}

if(boton_u != null){
    boton_u.addEventListener('click', function() {
        console.log(document.activeElement)
        if (selectedTab != null){
            if (opciones.value == 'Usuarios'){
                var usuario = tablaDatos.rows[selectedTab].cells[0].innerHTML;
                var data = {
                    'Usuario': usuario,
                    'Modo': opciones.value
                };
                fetch("/update", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                }).then(response => response.text())
                  .then(data => console.log(data));
                setTimeout(function() {
                    buscarOpciones();
                }, 250);
            } else if (opciones.value == "Llantas"){
                llantaUpdate = true;
                popup.innerHTML = `
                    <label class='popup-label'>Ingrese el nuevo precio (COP)</label>
                    <textarea class = "popup-text" name="precio_tx" id="precio_tx" rows="1" required maxlength = "10"></textarea>
                    <button type="submit">
                        Enviar
                    </button>
                `;
                popup_container.style.display = 'block';
                const textprecio = document.getElementById('precio_tx');
                textprecio.addEventListener("input", function() {
                    this.value = this.value.replace(/[^0-9]/g, "");
                });
            }
        }
    });
}

if(boton_d != null){
    boton_d.addEventListener('click', function() {
        console.log(document.activeElement)
        if (selectedTab != null){
            if (opciones.value == 'Vehiculos'){
                var marca = tablaDatos.rows[selectedTab].cells[0].innerHTML;
                var modelo =tablaDatos.rows[selectedTab].cells[1].innerHTML;
                var ayno = tablaDatos.rows[selectedTab].cells[2].innerHTML;
                var data = {
                    'Marca': marca,
                    'Modelo': modelo,
                    'Ayno': ayno,
                    'Modo': opciones.value
                };
            }else if(opciones.value == 'Usuarios'){
                var usuario = tablaDatos.rows[selectedTab].cells[0].innerHTML;
                var data = {
                    'Usuario': usuario,
                    'Modo': opciones.value
                };
            }else if(opciones.value == 'Llantas'){
                var medidaTabla = tablaDatos.rows[selectedTab].cells[1].innerHTML;
                var marcaTabla = tablaDatos.rows[selectedTab].cells[0].innerHTML;
                var data = {
                    'Medida': medidaTabla,
                    'Marca': marcaTabla,
                    'Modo': opciones.value
                }
            }
            fetch('/delete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }).then(response => response.text())
              .then(data => console.log(data));
            setTimeout(function() {
                buscarOpciones();
            }, 250);
        }
    });
}

if(boton_c != null){
    boton_c.addEventListener('click', function() {
        if (opciones.value == 'Vehiculos'){
            llantaUpdate = true;
        }
        popup.innerHTML = `
            <label class='popup-label'>Ingrese la marca</label>
            <textarea class = "popup-text" name="marca_tx" id="marca_tx" rows="1"></textarea>
            <label class='popup-label'>Déjelo vacío para usar</label>
            <label class='popup-label'>una marca existente.</label>
            <button type="submit">
                Siguiente
            </button>
        `;
        console.log(popup.innerHTML)
        popup_container.style.display = 'block'; 
    });
}

if(popup != null){
    popup.addEventListener('submit', function(event) {
        event.preventDefault();
        if(opciones.value == 'Vehiculos'){
            if(fase_popup == 1){
                if(document.getElementById('marca_tx').value != ''){
                    tieneMarca = true;
                    valorMarca = document.getElementById('marca_tx').value;
                }
                popup.innerHTML = `
                    <label class='popup-label'>Ingrese el modelo</label>
                    <textarea class = "popup-text" name="modelo_tx" id="modelo_tx" rows="1"></textarea>
                    <label class='popup-label'>Déjelo vacío para usar</label>
                    <label class='popup-label'>una modelo existente.</label>
                    <button type="submit">
                        Siguiente
                    </button>
                `;
                fase_popup = 2;
            }else if(fase_popup == 2){
                if(document.getElementById('modelo_tx').value != ''){
                    tieneModelo = true;
                    valorModelo = document.getElementById('modelo_tx').value;
                }
                popup.innerHTML = `
                    <label class='popup-label'>Ingrese la medida</label>
                    <label class = 'popup-label' id = 'ayno_label'>Ingrese el año</label>
                    <textarea class = "popup-text" name="ayno" id="ayno" rows="1" required maxlength=5></textarea>
                    <label class = 'popup-label'>Ingrese el tipo de carroceria</label>
                    <textarea class = "popup-text" name="tipo_carro" id="tipo_carro" rows="1" required maxlength=20></textarea>
                    <button id="boton_popup" type="submit">
                        Enviar
                    </button>
                `;
                const aynoLabel = document.getElementById('ayno_label');
                const textarea = document.getElementById('ayno');
                textarea.addEventListener("input", function() {
                    this.value = this.value.replace(/[^0-9]/g, "");
                });
                medida.style.display = 'inline-block';
                popup.insertBefore(medida, aynoLabel);
                if(!tieneModelo){
                    const botonPopup = document.getElementById('boton_popup');
                    modelo.style.display = 'inline-block';
                    const labelModelo = document.createElement('label');
                    labelModelo.classList.add('popup-label');
                    labelModelo.innerHTML = `Modelo`;
                    popup.insertBefore(modelo, botonPopup);
                    popup.insertBefore(labelModelo, modelo);
                    if(!tieneMarca){
                        marca.style.display = 'inline-block';
                        const labelMarca = document.createElement('label');
                        labelMarca.classList.add('popup-label');
                        labelMarca.innerHTML = `Marca`;
                        popup.insertBefore(marca, labelModelo);
                        popup.insertBefore(labelMarca, marca);
                    }
                }else if(!tieneMarca){
                    const botonPopup = document.getElementById('boton_popup');
                    marca.style.display = 'inline-block';
                    const labelMarca = document.createElement('label');
                    labelMarca.classList.add('popup-label');
                    labelMarca.innerHTML = `Marca`;
                    popup.insertBefore(marca, botonPopup);
                    popup.insertBefore(labelMarca, marca);
                }
                fase_popup = 3;
            }else{
                var marcaData;
                var modeloData;
                if(tieneMarca){
                    marcaData = valorMarca;
                }else{
                    marcaData = marca.value;
                }
                if(tieneModelo){
                    modeloData = valorModelo;
                }else{
                    modeloData = modelo.value;
                }
                var data = {
                    'Marca': marcaData,
                    'Modelo': modeloData,
                    'Ayno': document.getElementById('ayno').value,
                    'TipoCarro' : document.getElementById('tipo_carro').value,
                    'Medida': medida.value,
                    'Modo': 'Vehiculo'
                };
                
                fetch('/create', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                }).then(response => response.text())
                .then(data => console.log(data));
                cerrarPopup();
                setTimeout(function() {
                    buscarOpciones();
                }, 250);
            }
        }else if(llantaUpdate){
            var medidaTabla = tablaDatos.rows[selectedTab].cells[1].innerHTML;
            var marcaTabla = tablaDatos.rows[selectedTab].cells[0].innerHTML;
            var precio_content = document.getElementById('precio_tx').value
            var data = {
                'Medida': medidaTabla,
                'Marca': marcaTabla,
                'Precio': precio_content,
                'Modo': opciones.value
            };
            fetch("/update", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }).then(response => response.text())
              .then(data => console.log(data));
            setTimeout(function() {
                buscarOpciones();
            }, 250);
            cerrarPopup();
        }else{
            if(fase_popup == 1){
                if(document.getElementById('marca_tx').value != ''){
                    tieneMarcaL = true;
                    valorMarcaL = document.getElementById('marca_tx').value;
                }
                popup.innerHTML = `
                    <label class='popup-label'>Ingrese la medida</label>
                    <textarea class = "popup-text" name="medida_tx" id="medida_tx" rows="1"></textarea>
                    <label class='popup-label'>Déjelo vacío para usar</label>
                    <label class='popup-label'>una medida existente.</label>
                    <button type="submit">
                        Siguiente
                    </button>
                `;
                fase_popup = 2;
            }else if(fase_popup == 2){
                if(document.getElementById('medida_tx').value != ''){
                    tieneMedidaL = true;
                    valorMedidaL = document.getElementById('medida_tx').value;
                }
                popup.innerHTML = `
                    <label class='popup-label'>Ingrese el precio</label>
                    <textarea class = "popup-text" name="prec_tx" id="prec_tx" rows="1" required maxlength=10></textarea>
                    <button id="boton_popup_u" type="submit">
                        Enviar
                    </button>
                `;
                const textareaP = document.getElementById('prec_tx');
                textareaP.addEventListener("input", function() {
                    this.value = this.value.replace(/[^0-9]/g, "");
                });
                const botonPopup = document.getElementById('boton_popup_u');
                if(tieneMarcaL){
                    const textDurab = document.createElement('textarea');
                    textDurab.classList.add('popup-text');
                    textDurab.id = 'dura_tx';
                    textDurab.name = 'dura_tx';
                    textDurab.required = true;
                    textDurab.rows = 1;
                    textDurab.maxLength = 1;
                    const labelDurab = document.createElement('label');
                    labelDurab.classList.add('popup-label');
                    labelDurab.innerHTML = `Ingrese la durabilidad (1-5)`;
                    popup.insertBefore(textDurab, botonPopup);
                    popup.insertBefore(labelDurab, textDurab);
                    textDurab.addEventListener("input", function() {
                        this.value = this.value.replace(/[^1-5]/g, "");
                    });
                }
                if(!tieneMedidaL){
                    medida.style.display = 'inline-block';
                    const labelMedida = document.createElement('label');
                    labelMedida.classList.add('popup-label');
                    labelMedida.innerHTML = `Medida`;
                    popup.insertBefore(medida, botonPopup);
                    popup.insertBefore(labelMedida, medida);
                    if(!tieneMarcaL){
                        marcaL.style.display = 'inline-block';
                        const labelMarcaL = document.createElement('label');
                        labelMarcaL.classList.add('popup-label');
                        labelMarcaL.innerHTML = `Marca`;
                        popup.insertBefore(marcaL, labelMedida);
                        popup.insertBefore(labelMarcaL, marcaL);
                    }
                }else if(!tieneMarcaL){
                    marcaL.style.display = 'inline-block';
                    const labelMarcaL = document.createElement('label');
                    labelMarcaL.classList.add('popup-label');
                    labelMarcaL.innerHTML = `Marca`;
                    popup.insertBefore(marcaL, botonPopup);
                    popup.insertBefore(labelMarcaL, marcaL);
                }
                fase_popup = 3;
            }else{
                valorDurabilidad = document.getElementById('dura_tx');
                if(valorDurabilidad == null){
                    valorDurabilidad = '';
                }else{
                    valorDurabilidad = valorDurabilidad.value;
                }
                var marcaLData;
                var medidaLData;
                if(tieneMarcaL){
                    marcaLData = valorMarcaL;
                }else{
                    marcaLData = marcaL.value;
                }
                if(tieneMedidaL){
                    medidaLData = valorMedidaL;
                }else{
                    medidaLData = medida.value;
                }
                var data = {
                    'Marca': marcaLData,
                    'Medida': medidaLData,
                    'Durabilidad': valorDurabilidad,
                    'Precio': document.getElementById('prec_tx').value,
                    'Modo': 'Llanta'
                };
                
                fetch('/create', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                }).then(response => response.text())
                .then(data => console.log(data));
                cerrarPopup();
                setTimeout(function() {
                    buscarOpciones();
                }, 250);
            }
        }
        
    });
}

if (marca != null){
    marca.addEventListener('change', function() {
        if(marca.value == 'N/A'){
            return;
        }
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
    
            while (modelo.firstChild) {
                modelo.removeChild(modelo.firstChild);
            }
    
            var opcion = document.createElement('option');
            opcion.text = 'N/A';
            opcion.value = 'N/A';
            modelo.appendChild(opcion);

            for (var i = 0; i < modelos.length ; i++){
                var opcion = document.createElement('option');
                opcion.text = modelos[i];
                opcion.value = modelos[i];
                modelo.appendChild(opcion);
            }
        });
    });
}

function cerrarPopup() {
    llantaUpdate = false;
    tieneModelo = false;
    tieneMarca = false;
    tieneMarcaL = false;
    tieneMedidaL = false;
    fase_popup = 1;
    popup_container.style.display = 'none';
}

function buscarOpciones(){
    var data = {
        'Modo': opciones.value
    };
    var ruta;

    if(opciones.value === 'Consultas_usuario'){
        ruta = '/historial';
    }else{
        ruta = '/administracion';
    }

    fetch(ruta, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => response.json())
      .then(data => {
            while(tablaDatos.firstChild){
                tablaDatos.removeChild(tablaDatos.firstChild);
            }
            var encabezado = document.createElement('thead');
            var cuerpo = document.createElement('tbody')
            
            if(opciones.value === 'Vehiculos'){
                encabezado.innerHTML = `
                    <th>Marca</th>
                    <th>Modelo</th>
                    <th>Año</th>
                `
                boton_c.style = 'display: relative;';
                boton_d.style = 'display: relative;';
                boton_u.style = 'display: none;';
                tablaDatos.append(encabezado);
                for (var i = 0; i < data.Marca.length; i++) {
                    var fila = document.createElement('tr');
                    fila.tabIndex = i + 1;
                    fila.innerHTML = `
                        <td>${data.Marca[i]}</td>
                        <td>${data.Modelo[i]}</td>
                        <td>${data.Año[i]}</td>
                    `;
                    cuerpo.append(fila);
                }
            }else if(opciones.value === 'Llantas'){
                encabezado.innerHTML = `
                    <th>Marca</th>
                    <th>Medida</th>
                    <th>Precio</th>
                `
                boton_c.style = 'display: relative;';
                boton_d.style = 'display: relative;';
                boton_u.style = 'display: relative;';
                boton_u.innerHTML = `Actualizar precio`;
                tablaDatos.append(encabezado);
                for (var i = 0; i < data.Precio.length; i++) {
                    var fila = document.createElement('tr');
                    fila.innerHTML = `
                        <td>${data.Marca[i]}</td>
                        <td>${data.Medida[i]}</td>
                        <td>${data.Precio[i]}</td>
                    `;
                    fila.tabIndex = i + 1;
                    cuerpo.append(fila);
                }
            }else if(opciones.value === 'Consultas' || data.Condicion == true){
                encabezado.innerHTML = `
                    <th>Fecha</th>
                    <th>Vehiculo</th>
                    <th>Llanta</th>
                    <th>Usuario</th>
                `
                if(boton_c != null){
                    boton_c.style = 'display: none;';
                    boton_d.style = 'display: none;';
                    boton_u.style = 'display: none;';
                }
                tablaDatos.append(encabezado);
                for (var i = 0; i < data.Fecha.length; i++) {
                    var fila = document.createElement('tr');
                    fila.innerHTML = `
                        <td>${data.Fecha[i]}</td>
                        <td>${data.Vehiculo[i]}</td>
                        <td>${data.Llanta[i]}</td>
                        <td>${data.Usuario[i]}</td>
                    `;
                    fila.tabIndex = i + 1;
                    cuerpo.append(fila);
                }
            }else{
                encabezado.innerHTML = `
                    <th>Usuario</th>
                    <th>Correo</th>
                    <th>Contraseña</th>
                    <th>Tipo usuario</th>
                    <th>Primer nombre</th>
                    <th>Segundo nombre</th>
                    <th>Primer apellido</th>
                    <th>Segundo apellido</th>
                `;
                boton_d.style = 'display: relative;';
                boton_u.style = 'display: relative;';
                boton_c.style = 'display: none;';
                boton_u.innerHTML = `Dar/Quitar admin`;
                tablaDatos.append(encabezado);
                for (var i = 0; i < data.Usuario.length; i++) {
                    var fila = document.createElement('tr');
                    fila.innerHTML = `
                        <td>${data.Usuario[i]}</td>
                        <td>${data.Correo[i]}</td>
                        <td>${data.Contrasena[i]}</td>
                        <td>${data.TipoUsuario[i]}</td>
                        <td>${data.PrimerNombre[i]}</td>
                        <td>${data.SegundoNombre[i]}</td>
                        <td>${data.PrimerApellido[i]}</td>
                        <td>${data.SegundoApellido[i]}</td>
                    `;
                    fila.tabIndex = i + 1;
                    cuerpo.append(fila);
                }
            }
            tablaDatos.appendChild(cuerpo)
            paginateTable()
      });
}

function scrollToBottom() {
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
    });
}

function paginateTable(){
    $pager = document.getElementById('pager')
    if($pager == null){
        $pager = $('<div class="pager" id="pager"></div>');
    }else{
        while($pager.firstChild){
            $pager.removeChild($pager.firstChild)
        }
    }
    $('table.paginated').each(function() {
        var currentPage = 0;
        var numPerPage = 50;
        var $table = $(this);
        $table.bind('repaginate', function() {
            $table.find('tbody tr').hide().slice(currentPage * numPerPage, (currentPage + 1) * numPerPage).show();
        });
        $table.trigger('repaginate');
        var numRows = $table.find('tbody tr').length;
        var numPages = Math.ceil(numRows / numPerPage);
        for (var page = 0; page < numPages; page++) {
            $('<span class="page-number"></span>').text(page + 1).bind('click', {
                newPage: page
            }, function(event) {
                currentPage = event.data['newPage'];
                $table.trigger('repaginate');
                $(this).addClass('active').siblings().removeClass('active');
            }).appendTo($pager).addClass('clickable');
        }
        $('table tr').focus(function() {
            selectedTab = $(this).attr('tabindex');
            console.log('ye');
        });
        try {
            $pager.insertBefore($table).find('span.page-number:first').addClass('active');
        } catch (error) {
            
        }
    });
}

buscarOpciones();