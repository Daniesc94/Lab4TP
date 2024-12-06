import sqlite3

def conectar_db():
    
    conn = sqlite3.connect("gestion_escuela.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        apellido TEXT NOT NULL,
                        documento TEXT UNIQUE NOT NULL,
                        fecha_nacimiento DATE NOT NULL,
                        telefono TEXT,
                        domicilio TEXT,
                        id_materia INTEGER,
                        FOREIGN KEY(id_materia) REFERENCES materias(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS materias (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL)''')

    conn.commit()
    return conn, cursor

def menu_principal():
    
    print("\n--- Menú Principal ---")
    print("1. Ingresar usuario")
    print("2. Consultar datos")
    print("3. Modificar usuario")
    print("4. Eliminar usuario")
    print("5. Listar usuarios")
    print("6. Ingresar materia")
    print("7. Listar usuarios por materia")
    print("8. Salir")

def listar_usuarios_por_materia(cursor):
    
    cursor.execute("SELECT id, nombre FROM materias")
    materias = cursor.fetchall()

    if materias:
        print("\nMaterias disponibles:")
        for materia in materias:
            print(f"{materia[0]}. {materia[1]}")

        id_materia = input("Ingrese el ID de la materia: ")
        cursor.execute('''SELECT usuarios.id, usuarios.nombre, usuarios.apellido, materias.nombre AS materia 
                          FROM usuarios
                          JOIN materias ON usuarios.id_materia = materias.id
                          WHERE usuarios.id_materia = ?''', (id_materia,))
        
        resultados = cursor.fetchall()
        if resultados:
            print("\nUsuarios inscritos:")
            for usuario in resultados:
                print(f"ID: {usuario[0]}, Nombre: {usuario[1]}, Apellido: {usuario[2]}, Materia: {usuario[3]}")
        else:
            print("No hay usuarios inscritos en esta materia.")
    else:
        print("No hay materias disponibles. Primero ingrese una materia.")


def ingresar_materia(cursor, conn):
    
    nombre = input("Nombre de la materia: ")

    cursor.execute('''INSERT INTO materias (nombre)
                      VALUES (?)''', (nombre,))
    conn.commit()
    print("Materia ingresada con éxito.")


from datetime import datetime

def ingresar_datos(cursor, conn):
        
    # Validar nombre
    while True:
        nombre = input("Nombre: ")
        if nombre.isalpha():
            break
        else:
            print("El nombre solo debe contener letras. Inténtelo de nuevo.")

    # Validar apellido
    while True:
        apellido = input("Apellido: ")
        if apellido.isalpha():
            break
        else:
            print("El apellido solo debe contener letras. Inténtelo de nuevo.")

    # Validar documento
    while True:
        documento = input("Número de documento (8 dígitos): ")
        if documento.isdigit() and len(documento) == 8:
            cursor.execute("SELECT 1 FROM usuarios WHERE documento = ?", (documento,))
            if cursor.fetchone():
                print("El documento ya está registrado. Intente con otro.")
            else:
                break
        else:
            print("El documento debe tener exactamente 8 dígitos. Inténtelo de nuevo.")
    
    # Validar fecha de nacimiento (formato DD/MM/AAAA)
    while True:
        fecha_nacimiento = input("Fecha de nacimiento (DD/MM/AAAA): ")
        try:
            fecha_obj = datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
            if fecha_obj > datetime.now():
                print("La fecha de nacimiento no puede ser futura. Inténtelo de nuevo.")
            else:
                break
        except ValueError:
            print("El formato debe ser DD/MM/AAAA. Inténtelo de nuevo.")
    
    # Validar teléfono
    while True:
        telefono = input("Teléfono: ")
        if telefono.isdigit():
            break
        else:
            print("El teléfono solo debe contener números. Inténtelo de nuevo.")
    
    # Validar domicilio
    domicilio = input("Domicilio: ")

    # Seleccionar materia
    cursor.execute("SELECT id, nombre FROM materias")
    materias = cursor.fetchall()

    if materias:
        print("\nMaterias disponibles:")
        for materia in materias:
            print(f"{materia[0]}. {materia[1]}")

        while True:
            id_materia = input("Seleccione el ID de la materia: ")
            if any(materia[0] == int(id_materia) for materia in materias):
                break
            else:
                print("ID de materia no válido. Inténtelo de nuevo.")
    else:
        print("No hay materias disponibles. Primero ingrese una materia.")
        return

    # Insertar los datos validados en la base de datos
    cursor.execute('''INSERT INTO usuarios (nombre, apellido, documento, fecha_nacimiento, telefono, domicilio, id_materia)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (nombre, apellido, documento, fecha_obj.strftime("%Y-%m-%d"), telefono, domicilio, id_materia))
    conn.commit()
    print("Usuario ingresado con éxito.")



def consultar_datos(cursor):
    
    criterio = input("Buscar por (1: ID, 2: Apellido): ")
    if criterio == "1":
        id_usuario = input("Ingrese el ID del usuario: ")
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id_usuario,))
    elif criterio == "2":
        apellido = input("Ingrese el apellido: ")
        cursor.execute("SELECT * FROM usuarios WHERE apellido LIKE ?", (f"%{apellido}%",))
    else:
        print("Criterio no válido.")
        return

    resultados = cursor.fetchall()
    if resultados:
        for fila in resultados:
            print(f"ID: {fila[0]}, Nombre: {fila[1]}, Apellido: {fila[2]}, Documento: {fila[3]}, Fecha Nac: {fila[4]}, Teléfono: {fila[5]}, Domicilio: {fila[6]}")
    else:
        print("No se encontraron resultados.")

def modificar_datos(cursor, conn):
    
    id_usuario = input("Ingrese el ID del usuario a modificar: ")
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id_usuario,))
    usuario = cursor.fetchone()

    if usuario:
        print(f"Datos actuales: {usuario}")
        nombre = input(f"Nuevo nombre (actual: {usuario[1]}): ") or usuario[1]
        apellido = input(f"Nuevo apellido (actual: {usuario[2]}): ") or usuario[2]
        documento = input(f"Nuevo documento (actual: {usuario[3]}): ") or usuario[3]
        fecha_nacimiento = input(f"Nueva fecha de nacimiento (actual: {usuario[4]}): ") or usuario[4]
        telefono = input(f"Nuevo teléfono (actual: {usuario[5]}): ") or usuario[5]
        domicilio = input(f"Nuevo domicilio (actual: {usuario[6]}): ") or usuario[6]

        cursor.execute('''UPDATE usuarios
                          SET nombre = ?, apellido = ?, documento = ?, fecha_nacimiento = ?, telefono = ?, domicilio = ?
                          WHERE id = ?''', (nombre, apellido, documento, fecha_nacimiento, telefono, domicilio, id_usuario))
        conn.commit()
        print("Datos actualizados con éxito.")
    else:
        print("Usuario no encontrado.")

def eliminar_datos(cursor, conn):
    
    id_usuario = input("Ingrese el ID del usuario a eliminar: ")
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id_usuario,))
    usuario = cursor.fetchone()

    if usuario:
        confirmacion = input(f"¿Está seguro de eliminar a {usuario[1]} {usuario[2]}? (S/N): ").upper()
        if confirmacion == "S":
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
            conn.commit()
            print("Usuario eliminado con éxito.")
        else:
            print("Eliminación cancelada.")
    else:
        print("Usuario no encontrado.")

def listar_datos(cursor):
    
    print("Opciones de ordenamiento:")
    print("1. Orden alfabético por nombre")
    print("2. Orden numérico por ID")
    print("3. Orden por edad")

    opcion = input("Seleccione una opción: ")
    if opcion == "1":
        cursor.execute('''SELECT usuarios.*, materias.nombre AS materia 
                          FROM usuarios 
                          LEFT JOIN materias ON usuarios.id_materia = materias.id
                          ORDER BY usuarios.nombre ASC''')
    elif opcion == "2":
        cursor.execute('''SELECT usuarios.*, materias.nombre AS materia 
                          FROM usuarios 
                          LEFT JOIN materias ON usuarios.id_materia = materias.id
                          ORDER BY usuarios.id ASC''')
    elif opcion == "3":
        cursor.execute('''SELECT usuarios.*, materias.nombre AS materia 
                          FROM usuarios 
                          LEFT JOIN materias ON usuarios.id_materia = materias.id
                          ORDER BY date('now') - date(usuarios.fecha_nacimiento) ASC''')
    else:
        print("Opción no válida.")
        return

    resultados = cursor.fetchall()
    if resultados:
        for fila in resultados:
            print(f"ID: {fila[0]}, Nombre: {fila[1]}, Apellido: {fila[2]}, Documento: {fila[3]}, Fecha Nac: {fila[4]}, Teléfono: {fila[5]}, Domicilio: {fila[6]}, Materia: {fila[8]}")
    else:
        print("No hay usuarios registrados.")


def main():
    conn, cursor = conectar_db()
    while True:
        menu_principal()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            ingresar_datos(cursor, conn)
        elif opcion == "2":
            consultar_datos(cursor)
        elif opcion == "3":
            modificar_datos(cursor, conn)
        elif opcion == "4":
            eliminar_datos(cursor, conn)
        elif opcion == "5":
            listar_datos(cursor)
        elif opcion == "6":
            ingresar_materia(cursor, conn)
        elif opcion == "7":
            listar_usuarios_por_materia(cursor)
        elif opcion == "8":
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")
    conn.close()

if __name__ == "__main__":
    main()
