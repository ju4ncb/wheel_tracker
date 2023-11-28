--
-- Archivo generado con SQLiteStudio v3.4.4 el dom. nov. 12 23:05:05 2023
--
-- Codificacion de texto usada: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Tabla: Usuarios
CREATE TABLE IF NOT EXISTS Usuarios {
    Id_usuario INTEGER NOT NULL,
    Usuario TEXT(20) NOT NULL,
    Correo TEXT(254),
    Contrasena TEXT(30) NOT NULL,
    Tipo_usario TEXT(1) NOT NULL,
    nm1 TEXT(30) NOT NULL,
    nm2 TEXT(30),
    ap1 TEXT(30) NOT NULL,
    ap2 TEXT(30)
    CONSTRAINT Usuarios_PK PRIMARY KEY (Id_usuario),
    CONSTRAINT Usuarios_UN UNIQUE (Usuario),
    CONSTRAINT Usuarios_CH CHECK(
        Id_usuario = 'A' OR Id_usuario = 'U'
    )
};

-- Tabla: Comentario_anonimo
CREATE TABLE IF NOT EXISTS Comentarios (
    Id_consulta INTEGER NOT NULL,
    Opinion TEXT (400) NOT NULL, 
    Valoracion DECIMAL (2, 1) NOT NULL,
    CONSTRAINT Comentario_PK PRIMARY KEY (Id_consulta),
    CONSTRAINT Comentarios_consultas_FK FOREIGN KEY (Id_consulta) REFERENCES Consultas (Id_consulta)
);

-- Tabla: Consultas
CREATE TABLE IF NOT EXISTS Consultas (
    Id_consulta INTEGER NOT NULL,
    Id_usuario INTEGER,
    Fecha TEXT NOT NULL,
    CONSTRAINT Consultas_PK PRIMARY KEY (Id_consulta),
    CONSTRAINT Consultas_Usuarios_FK FOREIGN KEY (Id_usuario) REFERENCES Usuarios (Id_usuario)
);

-- Tabla: LLantas
CREATE TABLE IF NOT EXISTS LLantas (
    Id_llanta INTEGER NOT NULL,
    Id_medida INTEGER NOT NULL,
    Id_marca_llanta INTEGER NOT NULL,
    Precio INTEGER (10) NOT NULL,
    
    CONSTRAINT Llantas_PK PRIMARY KEY (Id_llanta), 
    CONSTRAINT Llantas_medidas_FK FOREIGN KEY (Id_medida) REFERENCES Medidas (Id_medida),
    CONSTRAINT Llantas_marcas_llantas_FK FOREIGN KEY (Id_marca_llanta) REFERENCES Marcas_llantas (Id_marca_llanta)
);

-- Tabla: Marcas llantas
CREATE TABLE IF NOT EXISTS Marcas_llantas (
    Id_marca_llanta INTEGER NOT NULL, 
    Descripcion TEXT (25) NOT NULL,
    Durabilidad INTEGER (1) NOT NULL,
    CONSTRAINT Marcas_Llantas_PK PRIMARY KEY (Id_marca_llanta)
);

-- Tabla: Medidas
CREATE TABLE IF NOT EXISTS Medidas (
    Id_medida INTEGER NOT NULL, 
    Identificacion TEXT(32) NOT NULL,
    CONSTRAINT Medidas_PK PRIMARY KEY (Id_medida)
);

-- Tabla: Años
CREATE TABLE IF NOT EXISTS Aynos(
    Id_ayno INTEGER NOT NULL,
    Id_modelo INTEGER NOT NULL,
    Ayno INTEGER(5) NOT NULL,
    Tipo_carroceria TEXT (20) NOT NULL,
    CONSTRAINT Aynos_PK PRIMARY KEY (Id_ayno),
    CONSTRAINT Aynos_modelos_FK FOREIGN KEY (Id_modelo) REFERENCES Modelos (Id_modelo) 
);

-- Tabla: Años_medidas
CREATE TABLE IF NOT EXISTS Aynos_medidas (
    Id_aynm INTEGER NOT NULL, 
    Id_ayno INTEGER NOT NULL, 
    Id_medida INTEGER NOT NULL,
    Localizacion TEXT(1) NOT NULL,
    CONSTRAINT Aynos_medidas_PK PRIMARY KEY (Id_aynm),
    CONSTRAINT Verificar_localizacion_Aynos_Medidas_CH CHECK (
        Localizacion = 'D' OR Localizacion = 'T' OR Localizacion = 'A'
    ),
    CONSTRAINT Aynos_medidas_medidas_FK FOREIGN KEY (Id_medida) REFERENCES Medidas (Id_medida),
    CONSTRAINT Aynos_medidas_aynos_FK FOREIGN KEY (Id_ayno) REFERENCES Aynos (Id_ayno) 
);

-- Tabla: Modelos
CREATE TABLE IF NOT EXISTS Modelos (
    Id_modelo INTEGER NOT NULL,
    Id_marca_auto INTEGER NOT NULL,
    Nombre TEXT (25) NOT NULL,
    CONSTRAINT Modelos_PK PRIMARY KEY (Id_modelo),
    CONSTRAINT Moledos_marcas_FK FOREIGN KEY (Id_marca_auto) REFERENCES Marcas_autos (Id_marca_auto)
);

-- Tabla: Marcas autos
CREATE TABLE IF NOT EXISTS Marcas_autos (
    Id_marca_auto INTEGER NOT NULL, 
    Descripcion TEXT (25) NOT NULL,
    CONSTRAINT Marcas_autos_PK PRIMARY KEY (Id_marca_auto)
);

-- Tabla: Preferencias
CREATE TABLE IF NOT EXISTS Preferencias (
    Id_pref INTEGER NOT NULL, 
    Descripcion TEXT (30) NOT NULL,
    CONSTRAINT Preferencias_PK PRIMARY KEY (Id_pref) 
);

-- Tabla: Consultas_preferencias
CREATE TABLE IF NOT EXISTS Consultas_preferencias (
    Id_conp INTEGER KEY NOT NULL, 
    Id_consulta INTEGER NOT NULL, 
    Id_pref INTEGER NOT NULL,
    CONSTRAINT Consultas_Preferencias_PK PRIMARY KEY (Id_conp),
    CONSTRAINT Consultas_preferencias_consultas_FK FOREIGN KEY (Id_consulta) REFERENCES Consultas (Id_consulta),
    CONSTRAINT Consultas_preferencias_preferencias_FK FOREIGN KEY (Id_pref) REFERENCES Preferencias (Id_pref)
);

-- Tabla: Consulta_año
CREATE TABLE IF NOT EXISTS Consultas_aynos (
    Id_cona INTEGER NOT NULL, 
    Id_consulta INTEGER NOT NULL, 
    Id_ayno INTEGER NOT NULL,
    CONSTRAINT Consultas_aynos PRIMARY KEY (Id_cona),
    CONSTRAINT Consultas_aynos_aynos_FK FOREIGN KEY (Id_consulta) REFERENCES consultas (Id_consulta),
    CONSTRAINT Consultas_aynos_consultas_FK FOREIGN KEY (Id_ayno) REFERENCES aynos (Id_ayno) 
);

-- Tabla: Consulta_llanta
CREATE TABLE IF NOT EXISTS Consultas_llantas (
    Id_conl INTEGER NOT NULL,
    Id_llanta INTEGER NOT NULL,
    Id_consulta INTEGER NOT NULL,
    CONSTRAINT Consultas_llantas_PK PRIMARY KEY (Id_conl),
    CONSTRAINT Consultas_llantas_llantas_FK FOREIGN KEY (Id_llanta) REFERENCES Llantas (Id_llanta),   
    CONSTRAINT Consultas_llantas_consultas_FK FOREIGN KEY (Id_consulta) REFERENCES Consultas (Id_consulta)
);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;


