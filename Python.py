def mostrar_menu():
    print("\n" + "="*40)
    print("      SISTEMA DE BIBLIOTECA")
    print("="*40)
    print("1. Registrar nuevo usuario")
    print("2. Registrar nuevo libro")
    print("3. Pedir prestado un libro")
    print("4. Devolver libro (y calcular multa)")
    print("5. Mostrar estadísticas")
    print("6. Salir")
    print("="*40)

def registrar_usuario(usuarios):
    try:
        id_usuario = int(input("Ingrese el DNI o ID del usuario: "))
        if id_usuario in usuarios:
            print("[!] Error: El usuario ya está registrado.")
        else:
            nombre = input("Ingrese el nombre del usuario: ")
            usuarios[id_usuario] = {"nombre": nombre, "libros_actuales": []}
            print(f"[✓] Usuario '{nombre}' registrado con éxito.")
    except ValueError:
        print("[!] Error: El ID debe ser un número entero.")

def registrar_libro(libros):
    try:
        id_libro = int(input("Ingrese el código único del libro: "))
        if id_libro in libros:
            print("[!] Error: Ya existe un libro con ese código.")
        else:
            titulo = input("Ingrese el título del libro: ")
            libros[id_libro] = {
                "titulo": titulo, 
                "disponible": True, 
                "veces_prestado": 0
            }
            print(f"[✓] Libro '{titulo}' registrado con éxito.")
    except ValueError:
        print("[!] Error: El código del libro debe ser numérico.")

def pedir_prestado_un_libro(libros, usuarios, estadisticas):
    try:
        id_usuario = int(input("Ingrese el ID del usuario: "))
        if id_usuario not in usuarios:
            print("[!] Error: Usuario no encontrado.")
            return

        id_libro = int(input("Ingrese el código del libro a prestar: "))
        if id_libro not in libros:
            print("[!] Error: Libro no encontrado en el sistema.")
            return
        if libros[id_libro]["disponible"]:
            libros[id_libro]["disponible"] = False
            libros[id_libro]["veces_prestado"] += 1
            usuarios[id_usuario]["libros_actuales"].append(id_libro)
            
            estadisticas["total_prestamos"] += 1
            
            print(f"[✓] Préstamo exitoso. '{libros[id_libro]['titulo']}' prestado a {usuarios[id_usuario]['nombre']}.")
        else:
            print("[!] El libro no está disponible actualmente.")
            
    except ValueError:
        print("[!] Error: Ingrese datos numéricos válidos para los IDs.")

def devolver_libro(libros, usuarios, estadisticas):
    try:
        id_usuario = int(input("Ingrese el ID del usuario que devuelve: "))
        if id_usuario not in usuarios:
            print("[!] Error: Usuario no encontrado.")
            return

        id_libro = int(input("Ingrese el código del libro a devolver: "))
        
        if id_libro in usuarios[id_usuario]["libros_actuales"]:
            dias_retraso = int(input("¿Cuántos días de retraso tiene la devolución? (0 si está a tiempo): "))
            if dias_retraso < 0:
                print("[!] Error: Los días de retraso no pueden ser negativos.")
                return
            multa = 0
            if dias_retraso > 0:
                costo_por_dia = 500
                multa = dias_retraso * costo_por_dia
                estadisticas["recaudacion_multas"] += multa
                print(f"[!] Se aplicó una multa de ${multa} por {dias_retraso} días de retraso.")
            usuarios[id_usuario]["libros_actuales"].remove(id_libro)
            libros[id_libro]["disponible"] = True           
            print(f"[✓] Libro devuelto correctamente.")
        else:
            print("[!] Error: El usuario no tiene ese libro en préstamo.")           
    except ValueError:
        print("[!] Error: Entrada inválida. Use números enteros.")

def mostrar_estadisticas(libros, estadisticas):
    print("\n--- ESTADÍSTICAS DEL SISTEMA ---")
    print(f"Cantidad total de préstamos realizados: {estadisticas['total_prestamos']}")
    print(f"Recaudación total por multas: ${estadisticas['recaudacion_multas']}")
    
    print("\nLibros y su cantidad de solicitudes:")
    hay_libros = False
    for id_libro, datos in libros.items():
        hay_libros = True
        estado = "Disponible" if datos["disponible"] else "Prestado"
        print(f" - {datos['titulo']}: Prestado {datos['veces_prestado']} veces ({estado})")
    if not hay_libros:
        print(" No hay libros registrados en el sistema aún.")
def main():
    usuarios_db = {}
    libros_db = {}
    estadisticas_globales = {
        "total_prestamos": 0,
        "recaudacion_multas": 0.0
    }
    libros_db[101] = {"titulo": "La vida despues de la muerte", "disponible": True, "veces_prestado": 0}
    libros_db[102] = {"titulo": "El Eternauta", "disponible": True, "veces_prestado": 0}
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-6): ")
        if opcion == '1':
            registrar_usuario(usuarios_db)
        elif opcion == '2':
            registrar_libro(libros_db)
        elif opcion == '3':
            pedir_prestado_un_libro(libros_db, usuarios_db, estadisticas_globales)
        elif opcion == '4':
            devolver_libro(libros_db, usuarios_db, estadisticas_globales)
        elif opcion == '5':
            mostrar_estadisticas(libros_db, estadisticas_globales)
        elif opcion == '6':
            print("Cerrando el sistema de biblioteca. ¡Hasta luego!")
            break
        else:
            print("[!] Opción inválida. Por favor, ingrese un número del 1 al 6.")
if __name__ == "__main__":
    main()