import os
import curses
import json

def listar_archivos_json(ruta):
    archivos_json = [archivo for archivo in os.listdir(ruta) if archivo.endswith(".json")]
    return archivos_json

def main(stdscr):
    curses.curs_set(0)  # Ocultar el cursor
    stdscr.clear()

    ruta_actual = os.getcwd()
    archivos_json_disponibles = listar_archivos_json(ruta_actual)

    if not archivos_json_disponibles:
        stdscr.addstr(0, 0, "No hay archivos .json en la carpeta actual.")
        stdscr.refresh()
        stdscr.getch()
        return

    opcion_seleccionada = 0

    while True:
        stdscr.clear()

        for i, archivo in enumerate(archivos_json_disponibles):
            if i == opcion_seleccionada:
                stdscr.addstr(i, 0, f"> {archivo}")
            else:
                stdscr.addstr(i, 0, f"  {archivo}")

        stdscr.refresh()

        tecla = stdscr.getch()

        if tecla == curses.KEY_UP and opcion_seleccionada > 0:
            opcion_seleccionada -= 1
        elif tecla == curses.KEY_DOWN and opcion_seleccionada < len(archivos_json_disponibles) - 1:
            opcion_seleccionada += 1
        elif tecla == ord('\n'):
            break

    archivo_seleccionado = archivos_json_disponibles[opcion_seleccionada]
    procesar_archivo_json(archivo_seleccionado)

def procesar_archivo_json(archivo_seleccionado):
    with open(archivo_seleccionado, 'r') as archivo:
        contenido_json = json.load(archivo)

    # Mostrar los pares clave-valor en la consola
    print(f"Contenido del archivo JSON {archivo_seleccionado}:")
    for clave, valor in contenido_json.items():
        print(f"{clave}: {valor}")

if __name__ == "__main__":
    curses.wrapper(main)
