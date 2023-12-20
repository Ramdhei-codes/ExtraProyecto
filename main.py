import os
import curses
import json
import pyphi
import time

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

    operaciones_pyphi(contenido_json)
    
def operaciones_pyphi(archivo):
    tiempo_inicio = time.time()
    pyphi.config.load_file('pyphi_config.yml')
    network = pyphi.Network(archivo["tpm"], cm=archivo["cm"], node_labels=archivo["labels"])
    subsystem = pyphi.Subsystem(network, archivo["state"], nodes=(0, 1, 2))
    mechanism = (0,1,2)
    purview = (0,1,2)
    mip = subsystem.effect_mip(mechanism, purview)
    print(mip.partition)
    print(mip.phi) 
    tiempo_final = time.time()
    tiempo_total = tiempo_final - tiempo_inicio
    print("Tiempo de ejecución: ", tiempo_total)

if __name__ == "__main__":
    curses.wrapper(main)
