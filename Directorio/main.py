from flask import Flask, render_template, url_for, redirect, jsonify, g, request, session, flash
import sqlite3, random

app = Flask(__name__)
app.secret_key = 'Esunsecretodetumiradaylamiaunpresentimiento'
vehiculo = ''

def combobox_busqueda(modo : int) -> any:
    if modo == 0: #Inicio de pag
        #Marcas
        conexion = sqlite3.connect('bd.db')
        cursor = conexion.cursor()
        cursor.execute('SELECT Descripcion FROM Marcas_autos;')
        datos = cursor.fetchall()
        g.marcas = [valor[0] for valor in datos]
        conexion.close()

        #Marcas llantas
        conexion = sqlite3.connect('bd.db')
        cursor = conexion.cursor()
        cursor.execute('SELECT Descripcion FROM Marcas_llantas;')
        datos = cursor.fetchall()
        g.marcasL = [valor[0] for valor in datos]
        conexion.close()
    
        #Modelos
        conexion = sqlite3.connect('bd.db')
        cursor = conexion.cursor()
        cursor.execute('SELECT Nombre FROM Modelos WHERE id_marca_auto = 1;')
        datos = cursor.fetchall()
        g.modelos = [valor[0] for valor in datos]
        conexion.close()
    
        #Años
        conexion = sqlite3.connect('bd.db')
        cursor = conexion.cursor()
        cursor.execute('SELECT Ayno FROM Aynos WHERE id_modelo = 1;')
        datos = cursor.fetchall()
        g.aynos = [valor[0] for valor in datos]
        conexion.close()
        
        #Medidas
        conexion = sqlite3.connect('bd.db')
        cursor = conexion.cursor()
        cursor.execute('SELECT Identificacion FROM MEDIDAS;')
        datos = cursor.fetchall()
        g.medidas = [valor[0] for valor in datos]
        conexion.close()
        return
        
    changes_dict = dict()
    
    if modo == 1: #Cambio de marca
        #Modelos
        conexion = sqlite3.connect('bd.db')
        cursor = conexion.cursor()
        cursor.execute(f"SELECT M.Nombre, M.id_modelo FROM Modelos M INNER JOIN Marcas_autos A ON A.Id_marca_auto = M.Id_marca_auto WHERE A.Descripcion = '{vehiculo}'")
        datos = cursor.fetchall()
        id_modelo = datos[0][1]
        changes_dict['Modelos'] = [valor[0] for valor in datos]
        conexion.close()
    
        #Años
        conexion = sqlite3.connect('bd.db')
        cursor = conexion.cursor()
        cursor.execute(f'SELECT Ayno FROM Aynos WHERE id_modelo = {id_modelo};')
        datos = cursor.fetchall()
        changes_dict['Aynos'] = [valor[0] for valor in datos]
        conexion.close()
    else: #Cambio de año
        #Años
        conexion = sqlite3.connect('bd.db')
        cursor = conexion.cursor()
        cursor.execute(f"SELECT AY.Ayno, AY.Id_ayno From Aynos AY INNER JOIN Modelos MO ON MO.Id_modelo = AY.Id_modelo INNER JOIN Marcas_autos AU ON AU.Id_marca_auto = MO.Id_marca_auto WHERE MO.Nombre = '{vehiculo[1]}' AND AU.Descripcion = '{vehiculo[0]}'")
        datos = cursor.fetchall()
        changes_dict['Aynos'] = [valor[0] for valor in datos]
        conexion.close()
        
    return changes_dict

def combobox_administrador(modo : str) -> dict:
    resultados = dict()
    conexion = sqlite3.connect('bd.db')
    cursor = conexion.cursor()
    if modo == 'Vehiculos':
        cursor.execute('SELECT AU.Descripcion as Marca, MO.Nombre as Modelo, AY.Ayno as Año From Aynos AY INNER JOIN Modelos MO ON MO.Id_modelo = AY.Id_modelo INNER JOIN Marcas_autos AU ON AU.Id_marca_auto = MO.Id_marca_auto')
        vehiculos = cursor.fetchall()
        resultados = {
            'Marca':[marca[0] for marca in vehiculos],
            'Modelo':[mod[1] for mod in vehiculos],
            'Año':[ayn[2] for ayn in vehiculos]
        }
    elif modo == 'Llantas':
        cursor.execute('SELECT ML.Descripcion as Marca, ME.Identificacion as Medida, LL.Precio as Precio From Llantas LL INNER JOIN Marcas_llantas ML ON ML.Id_marca_llanta = LL.Id_marca_llanta INNER JOIN Medidas ME ON ME.Id_medida = LL.Id_medida')
        llantas = cursor.fetchall()
        resultados = {
            'Marca':[marca[0] for marca in llantas],
            'Medida':[med[1] for med in llantas],
            'Precio':[pre[2] for pre in llantas]
        }
    elif modo == 'Consultas':
        cursor.execute(
        """SELECT CO.Fecha, (VE.Marca || ' ' || VE.Modelo || ' ' || VE.Año) as Vehiculo, (LLA.Marca || ' ' || LLA.Medida) as Llanta, US.Usuario FROM Consultas CO
        INNER JOIN Consultas_aynos CA ON CO.Id_consulta = CA.Id_consulta
        INNER JOIN(
            SELECT AY.Id_ayno, AU.Descripcion as Marca, MO.Nombre as Modelo, AY.Ayno as Año From Aynos AY 
            INNER JOIN Modelos MO ON MO.Id_modelo = AY.Id_modelo 
            INNER JOIN Marcas_autos AU ON AU.Id_marca_auto = MO.Id_marca_auto
        ) VE ON VE.Id_ayno = CA.Id_ayno
        INNER JOIN Consultas_llantas CL ON CO.Id_consulta = CL.Id_consulta
        INNER JOIN(
            SELECT LL.Id_llanta, ML.Descripcion as Marca, ME.Identificacion as Medida, LL.Precio as Precio From Llantas LL 
            INNER JOIN Marcas_llantas ML ON ML.Id_marca_llanta = LL.Id_marca_llanta 
            INNER JOIN Medidas ME ON ME.Id_medida = LL.Id_medida
        ) LLA ON LLA.Id_llanta = CL.Id_llanta
        LEFT JOIN Usuarios US ON CO.Id_usuario = US.Id_usuario GROUP BY Id_conl"""
        )
        consultas = cursor.fetchall()
        usuarios = []
        for usuario in consultas:
            if usuario[3] == None:
                usuarios.append('Anonimo')
            else:
                usuarios.append(usuario[3])
                
        resultados = {
            'Fecha': [fecha[0] for fecha in consultas],
            'Vehiculo': [vehiculo[1] for vehiculo in consultas],
            'Llanta': [llanta[2] for llanta in consultas],
            'Usuario': usuarios
        }
    elif modo == 'Consultas_usuario':
        cursor.execute(
        f"""SELECT CO.Fecha, (VE.Marca || ' ' || VE.Modelo || ' ' || VE.Año) as Vehiculo, (LLA.Marca || ' ' || LLA.Medida) as Llanta, US.Usuario FROM Consultas CO
        INNER JOIN Consultas_aynos CA ON CO.Id_consulta = CA.Id_consulta
        INNER JOIN(
            SELECT AY.Id_ayno, AU.Descripcion as Marca, MO.Nombre as Modelo, AY.Ayno as Año From Aynos AY 
            INNER JOIN Modelos MO ON MO.Id_modelo = AY.Id_modelo 
            INNER JOIN Marcas_autos AU ON AU.Id_marca_auto = MO.Id_marca_auto
        ) VE ON VE.Id_ayno = CA.Id_ayno
        INNER JOIN Consultas_llantas CL ON CO.Id_consulta = CL.Id_consulta
        INNER JOIN(
            SELECT LL.Id_llanta, ML.Descripcion as Marca, ME.Identificacion as Medida, LL.Precio as Precio From Llantas LL 
            INNER JOIN Marcas_llantas ML ON ML.Id_marca_llanta = LL.Id_marca_llanta 
            INNER JOIN Medidas ME ON ME.Id_medida = LL.Id_medida
        ) LLA ON LLA.Id_llanta = CL.Id_llanta
        LEFT JOIN Usuarios US ON CO.Id_usuario = US.Id_usuario WHERE CO.Id_usuario = {g.user[0]}
        GROUP BY Id_conl"""
        )
        consultas = cursor.fetchall()
        resultados = {
            'Fecha': [fecha[0] for fecha in consultas],
            'Vehiculo': [vehiculo[1] for vehiculo in consultas],
            'Llanta': [llanta[2] for llanta in consultas],
            'Usuario': [usuario[3] for usuario in consultas]
        }
        resultados['Condicion'] = True
        print(g.user[0])
        return resultados
    else:
        cursor.execute("SELECT * FROM Usuarios WHERE Estado = 'A'")
        consultas = cursor.fetchall()
        resultados = {
            'Usuario': [us[1] for us in consultas],
            'Correo': [co[2] for co in consultas],
            'Contrasena': [con[3] for con in consultas],
            'TipoUsuario': [tpu[4] for tpu in consultas],
            'PrimerNombre': [nm1[5] for nm1 in consultas],
            'SegundoNombre': [nm2[6] for nm2 in consultas],
            'PrimerApellido': [ap1[7] for ap1 in consultas],
            'SegundoApellido': [ap2[8] for ap2 in consultas]
        }
    conexion.close()
    resultados['Condicion'] = False
    return resultados

def buscar_llantas(ayno : str, modelo : str, marca : str, pref : str, primeraVez : bool, id_c) -> dict:
    #Insertar consulta en la bd
    if g.user is None:
        id_usuario = int(-1)
    else:
        id_usuario = g.user[0]
    conexion = sqlite3.connect('bd.db')
    cursor = conexion.cursor()
    i = 0
    id_llantas = []
    
    if primeraVez:
        cursor.execute("INSERT INTO consultas (Fecha, Id_usuario) VALUES (datetime('now','localtime'), ?)", (id_usuario,))
        conexion.commit()
        id_consulta = cursor.lastrowid
    else:
        id_consulta = id_c
    
    #Conseguir id ayno
    cursor.execute(f"SELECT AY.Id_ayno From Aynos AY INNER JOIN Modelos MO ON MO.Id_modelo = AY.Id_modelo INNER JOIN Marcas_autos AU ON AU.Id_marca_auto = MO.Id_marca_auto WHERE AU.Descripcion = '{marca}' AND MO.Nombre = '{modelo}' AND AY.Ayno = '{ayno}'")
    id_ayno = cursor.fetchone()
    
    #Insertar consulta_ayno en la bd
    cursor.execute("INSERT INTO consultas_aynos (Id_consulta, Id_ayno) VALUES (?,?)", (id_consulta, id_ayno[0]))
    if pref == 'mejorCalidad':
        id_pref = 1
        cursor.execute("INSERT INTO consultas_preferencias (Id_consulta, Id_pref) VALUES (?,?)", (id_consulta, id_pref))
        
    elif pref == 'masEconomico':
        id_pref = 2
        cursor.execute("INSERT INTO consultas_preferencias (Id_consulta, Id_pref) VALUES (?,?)", (id_consulta, id_pref))
        
    conexion.commit()
    conexion.close()
    
    #Encontrar medidas
    conexion = sqlite3.connect('bd.db')
    cursor = conexion.cursor()
    cursor.execute(f"SELECT * FROM Aynos_medidas WHERE Id_ayno = '{id_ayno[0]}'")
    datos = cursor.fetchall()
    conexion.close()
    
    #Encontrar medidas y localizaciones
    if datos[0][3] != 'A': #Hay 2 posibles medidas
        id_med_d = datos[0][2] #Id medida delantera
        id_med_t = datos[1][2] #Id medida trasera
        
        #Sacar medidas
        conexion = sqlite3.connect('bd.db')
        cursor = conexion.cursor()
        cursor.execute(f"SELECT Identificacion FROM Medidas WHERE Id_medida = '{id_med_d}' OR Id_medida = '{id_med_t}'")
        datos = cursor.fetchall()
        conexion.close()
        
        medida_delantera = datos[0][0]
        medida_trasera = datos[1][0]
        
        #Llantas delanteras
        conexion = sqlite3.connect('bd.db')
        cursor = conexion.cursor()
        cursor.execute(f"SELECT L.Precio, M.Descripcion, M.Durabilidad, L.Id_llanta FROM Llantas L INNER JOIN Marcas_llantas M ON M.Id_marca_llanta = L.Id_marca_llanta WHERE L.Id_medida = {id_med_d}")
        datos_d = cursor.fetchall()
        conexion.close()
        
        #Llantas traseras
        conexion = sqlite3.connect('bd.db')
        cursor = conexion.cursor()
        cursor.execute(f"SELECT L.Precio, M.Descripcion, M.Durabilidad, L.Id_llanta FROM Llantas L INNER JOIN Marcas_llantas M ON M.Id_marca_llanta = L.Id_marca_llanta WHERE L.Id_medida = {id_med_t}")
        datos_t = cursor.fetchall()
        conexion.close()
        
        if pref == 'masEconomico':
            datos_d = sorted(datos_d, key = lambda x : x[0])
            datos_t = sorted(datos_t, key = lambda x : x[0]) #Los sortea del mas economico al mas caro
        elif pref == 'mejorCalidad':
            datos_d = sorted(datos_d, key = lambda x : x[2], reverse=True)
            datos_t = sorted(datos_t, key = lambda x : x[2], reverse=True) #Los sortea del que mas durabilidad tenga al que menos tenga
        else:
            random.shuffle(datos_d)
            random.shuffle(datos_t)
        
        precios_d = []
        marcas_d = []
        durabilidades_d = []
        precios_t = []
        marcas_t = []
        durabilidades_t = []
        while i < 3:
            if i == len(datos_d):
                break
            elif i == len(datos_t):
                break
            id_llantas.append(datos_d[i][3])
            id_llantas.append(datos_t[i][3])
            i += 1
        
        #Agrega a la lista final
        for dato_d, dato_t in zip(datos_d, datos_t):
            precios_d.append(dato_d[0])
            marcas_d.append(dato_d[1])
            durabilidades_d.append(dato_d[2])
            
            precios_t.append(dato_t[0])
            marcas_t.append(dato_t[1])
            durabilidades_t.append(dato_t[2])
            
        dict_llantas = {
            'Modo' : '2m', #2 medidas
            'MedidaD' : medida_delantera,
            'PreciosD': precios_d[:3],
            'MarcasD': marcas_d[:3],
            'DurabilidadesD': durabilidades_d[:3],
            'MedidaT':medida_trasera,
            'PreciosT': precios_t[:3],
            'MarcasT': marcas_t[:3],
            'DurabilidadesT': durabilidades_t[:3],
            'id': id_consulta
        }
        
    else:
        id_med = datos[0][2] #Id medida
        
        #Sacar medidas
        conexion = sqlite3.connect('bd.db')
        cursor = conexion.cursor()
        cursor.execute(f"SELECT Identificacion FROM Medidas WHERE Id_medida = '{id_med}'")
        datos = cursor.fetchall()
        conexion.close()
        
        medida = datos[0] #Medida
        
        #Llantas para la medida
        conexion = sqlite3.connect('bd.db')
        cursor = conexion.cursor()
        cursor.execute(f"SELECT L.Precio, M.Descripcion, M.Durabilidad, L.Id_llanta FROM Llantas L INNER JOIN Marcas_llantas M ON M.Id_marca_llanta = L.Id_marca_llanta WHERE L.Id_medida = {id_med}")
        datos = cursor.fetchall()
        conexion.close()
        
        if pref == 'masEconomico':
            datos = sorted(datos, key = lambda x : x[0]) #Los sortea del mas economico al mas caro
        elif pref == 'mejorCalidad':
            datos = sorted(datos, key = lambda x : x[2], reverse=True) #Los sortea del que mas durabilidad tenga al que menos tenga
        else:
            random.shuffle(datos)
        
        precios = []
        marcas = []
        durabilidades = []
        
        while i < 6 and i < len(datos):
            id_llantas.append(datos[i][3])
            i += 1
        
        #Agrega a la lista final
        for dato in datos:
            precios.append(dato[0])
            marcas.append(dato[1])
            durabilidades.append(dato[2])

        dict_llantas = {
            'Modo' : '1m', #1 medida
            'Medida' : medida,
            'Precios': precios[:6],
            'Marcas': marcas[:6],
            'Durabilidades': durabilidades[:6],
            'id': id_consulta
        }
        
    #Insetar consulta llantas
    conexion = sqlite3.connect('bd.db')
    cursor = conexion.cursor()
    for id_llanta in id_llantas:
        cursor.execute("INSERT INTO Consultas_llantas (Id_llanta, Id_consulta) VALUES (?,?)", (id_llanta, id_consulta))
    conexion.commit()
    conexion.close()
        
    return dict_llantas

@app.before_request
def load_logged_in_user():
    usuario = session.get("user_id")
    if usuario is None:
        g.user = None
    else:
        conexion = sqlite3.connect('bd.db')
        g.user = (
            conexion.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,)).fetchone()
        )
        conexion.close()

@app.errorhandler(404)
def incorrect_page(e):
    return redirect(url_for('home'))

@app.route("/busqueda/cbb", methods=['POST'])
def busqueda_post():
    global vehiculo
    vehiculo = request.get_json()['Valor']
    changes_dict = combobox_busqueda(request.get_json()['Modo'])
    return jsonify(changes_dict)

@app.route("/administracion", methods=['POST'])
def administracion_post():
    changes_dict = combobox_administrador(request.get_json()['Modo'])
    return jsonify(changes_dict)

@app.route("/historial", methods=['POST'])
def historial_post():
    changes_dict = combobox_administrador(request.get_json()['Modo'])
    return jsonify(changes_dict)

@app.route("/busqueda/buscar", methods=['POST'])
def boton_buscar():    
    yeison = request.get_json()
    
    dict_llantas = buscar_llantas(yeison['Ayno'], yeison['Modelo'], yeison['Marca'], yeison['Pref'], yeison['P'], yeison['Id'])
    return jsonify(dict_llantas)

@app.route("/busqueda/enviar", methods=['POST'])
def enviar_popup():
    #Insertar comentario en la bd
    datos = request.get_json()
    conexion = sqlite3.connect('bd.db')
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO comentarios (Opinion, Valoracion) VALUES (?,?)", (datos['comentario'],datos['valoracion']))
    conexion.commit()
    conexion.close()
    return '', 204

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/busqueda")
def busqueda():
    combobox_busqueda(0)
    return render_template('busqueda.html')

@app.route("/login", methods=['POST'])
def boton_iniciar_sesion():
    usuario = request.form["usuario"]
    contrasena = request.form["cont"]
    conexion = sqlite3.connect('bd.db')
    error = None
    user = conexion.execute(
        "SELECT usuario, contrasena, estado FROM usuarios WHERE usuario = ?", (usuario,)
    ).fetchone()
    conexion.close()
    if not user:
        error = "Usuario no existe."
    elif contrasena != user[1]:
        error = "Contraseña incorrecta."
    elif user[2] == 'D':
        error = "Usuario ya no existe."
        
    if error is None:
        session.clear()
        session["user_id"] = user[0]
        return redirect(url_for("home"))
    flash(error)
    return '', 204
    
@app.route("/login")
def iniciar_sesion():
    if g.user != None:
        return render_template('home.html')
    return render_template('inicio-sesion.html')

@app.route("/register", methods=['POST'])
def boton_registrar():
    usuario = request.form["usuario"]
    contrasena = request.form["cont"]
    correo = request.form["corr"]
    nm1 = request.form["nm1"]
    nm2 = request.form["nm2"]
    ap1 = request.form["ap1"]
    ap2 = request.form["ap2"]
    conexion = sqlite3.connect('bd.db')
    error = None

    if not usuario:
        error = "Ingrese un usuario."
    elif not contrasena:
        error = "Ingrese una contraseña."
    elif len(contrasena) < 6:
        error = "Contraseña de minimo 6 caracteres."
    elif not correo:
        correo = "N/A"
    elif not nm1:
        error = "Ingrese el primer nombre."
    elif not nm2:
        nm2 = "N/A"
    elif not ap1:
        error = "Ingrese el primer apellido."
    elif not ap2:
        ap2 = "N/A"

    if error is None:
        try:
            conexion.execute(
                "INSERT INTO usuarios (usuario, contrasena, correo, tipo_usuario, nm1, nm2, ap1, ap2, estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (usuario, contrasena, correo, 'U', nm1, nm2, ap1, ap2, 'A')
            )
            conexion.commit()
            conexion.close()
        except conexion.IntegrityError:
            error = f"Usuario {usuario} ya está registrado."
        else:
            return redirect(url_for("iniciar_sesion"))
    flash(error)
    return '', 204

@app.route("/register")
def registrar():
    if g.user != None:
        return render_template('home.html')
    return render_template('registro.html')

@app.route("/logout")
def cerrar_sesion():
    session.clear()
    return redirect(url_for("home"))

@app.route("/update", methods = ['POST'])
def update():
    datos = request.get_json()
    conexion = sqlite3.connect('bd.db')
    cursor = conexion.cursor()
    if datos['Modo'] == 'Usuarios':
        cursor.execute("SELECT Tipo_usuario FROM Usuarios WHERE Usuario = ?", (datos['Usuario'],))
        tipo_usuario = cursor.fetchone()
        if tipo_usuario[0] == 'A':
            cursor.execute("UPDATE Usuarios SET Tipo_usuario = 'U' WHERE Usuario = ?", (datos['Usuario'],))
        else:
            cursor.execute("UPDATE Usuarios SET Tipo_usuario = 'A' WHERE Usuario = ?", (datos['Usuario'],))
    else:
        cursor.execute("""
            SELECT LL.Id_llanta FROM Llantas LL 
            INNER JOIN Marcas_llantas ML ON ML.Id_marca_llanta = LL.Id_marca_llanta
            INNER JOIN Medidas ME ON ME.Id_medida = LL.Id_medida
            WHERE ME.Identificacion = ? AND ML.Descripcion = ?;
        """, (datos['Medida'], datos['Marca']))
        id_llanta = cursor.fetchone()
        cursor.execute("UPDATE Llantas SET Precio = ? WHERE Id_llanta = ?", (datos['Precio'],id_llanta[0],))

    conexion.commit()
    conexion.close()
        
    return '', 204

@app.route("/create", methods = ['POST'])
def create():
    datos = request.get_json()
    conexion = sqlite3.connect('bd.db')
    cursor = conexion.cursor()
    if datos['Modo'] == 'Vehiculo':
        cursor.execute("SELECT * FROM Marcas_autos WHERE Descripcion = ?", (datos['Marca'],))
        marca_bd = cursor.fetchone()
        if marca_bd is None:
            cursor.execute('INSERT INTO Marcas_autos (Descripcion) VALUES (?)', (datos['Marca'],))
            conexion.commit()
            marca_id = cursor.lastrowid
        else:
            marca_id = marca_bd[0]
        cursor.execute("SELECT * FROM Modelos WHERE Nombre = ?", (datos['Modelo'],))
        modelo_bd = cursor.fetchone()
        if modelo_bd is None:
            cursor.execute('INSERT INTO Modelos (Id_marca_auto, Nombre) VALUES (?, ?)', (marca_id, datos['Modelo'],))
            conexion.commit()
            modelo_id = cursor.lastrowid
        else:
            modelo_id = modelo_bd[0]
        cursor.execute("SELECT * FROM Aynos WHERE Ayno = ?", (datos['Ayno'],))
        ayno_bd = cursor.fetchone()
        if ayno_bd is None:
            cursor.execute('INSERT INTO Aynos (Id_modelo, Ayno, Tipo_carroceria) VALUES (?,?,?)', (modelo_id,datos['Ayno'],datos['TipoCarro']))
            conexion.commit()
            id_ayno = cursor.lastrowid
        else:
            id_ayno = ayno_bd[0]
        cursor.execute('SELECT Id_medida FROM Medidas WHERE Identificacion = ?', (datos['Medida'],))
        id_medida = cursor.fetchone()
        cursor.execute('INSERT INTO Aynos_medidas (Id_medida, Id_Ayno, Localizacion) VALUES (?,?,?)', (id_medida[0], id_ayno, 'A'))
    else:
        cursor.execute("SELECT * FROM Marcas_llantas WHERE Descripcion = ?", (datos['Marca'],))
        marca_bd = cursor.fetchone()
        if marca_bd is None:
            cursor.execute('INSERT INTO Marcas_llantas (Descripcion, Durabilidad) VALUES (?, ?)', (datos['Marca'],datos['Durabilidad']))
            conexion.commit()
            marca_id = cursor.lastrowid
        else:
            marca_id = marca_bd[0]
        cursor.execute("SELECT * FROM Medidas WHERE Identificacion = ?", (datos['Medida'],))
        medida_bd = cursor.fetchone()
        if medida_bd is None:
            cursor.execute('INSERT INTO Medidas (Identificacion) VALUES (?)', (datos['Medida'],))
            conexion.commit()
            medida_id = cursor.lastrowid
        else:
            medida_id = medida_bd[0]
        cursor.execute("SELECT * FROM Llantas WHERE Id_medida = ? AND Id_marca_llanta = ?", (medida_id, marca_id))
        llanta_bd = cursor.fetchone()
        if llanta_bd is None:
            cursor.execute('INSERT INTO Llantas (Id_medida, Id_marca_llanta, Precio) VALUES (?,?,?)', (medida_id, marca_id, datos['Precio']))
            conexion.commit()
        
    conexion.close()
    return '', 204

@app.route("/delete", methods = ['POST'])
def delete():
    datos = request.get_json()
    conexion = sqlite3.connect('bd.db')
    cursor = conexion.cursor()
    if datos['Modo'] == 'Usuarios':
        cursor.execute("SELECT Estado FROM Usuarios WHERE Usuario = ?", (datos['Usuario'],))
        estado = cursor.fetchone()
        if estado[0] == 'A':
            cursor.execute("UPDATE Usuarios SET Estado = 'D' WHERE Usuario = ?", (datos['Usuario'],))
            print(estado)
    elif datos['Modo'] == 'Vehiculos':
        cursor.execute(f"SELECT AY.Id_ayno From Aynos AY INNER JOIN Modelos MO ON MO.Id_modelo = AY.Id_modelo INNER JOIN Marcas_autos AU ON AU.Id_marca_auto = MO.Id_marca_auto WHERE AU.Descripcion = '{datos['Marca']}' AND MO.Nombre = '{datos['Modelo']}' AND AY.Ayno = '{datos['Ayno']}'")
        id_ayno = cursor.fetchone()
        cursor.execute("DELETE FROM Aynos WHERE Id_ayno = ?", id_ayno)
    else:
        cursor.execute("""
            SELECT LL.Id_llanta FROM Llantas LL 
            INNER JOIN Marcas_llantas ML ON ML.Id_marca_llanta = LL.Id_marca_llanta
            INNER JOIN Medidas ME ON ME.Id_medida = LL.Id_medida
            WHERE ME.Identificacion = ? AND ML.Descripcion = ?;
        """, (datos['Medida'], datos['Marca']))
        id_llanta = cursor.fetchone()
        cursor.execute("DELETE FROM Llantas WHERE Id_llanta = ?", (id_llanta[0],))
    conexion.commit()
    conexion.close()
    return '', 204

@app.route("/administracion")
def administracion():
    if g.user is None:
        return redirect(url_for("home"))
    else:
        if g.user[4] != 'A':
            return redirect(url_for("home"))
    combobox_busqueda(0)
    return render_template('administracion.html')

@app.route("/historial")
def historial():
    if g.user is None:
        return redirect(url_for("home"))
    return render_template('historial.html')

if __name__ == '__main__':
    app.run(debug = True)