# Copyright © 2020 baneon - MIT License
# See `LICENSE` included in the source distribution for details.

import sys
import time
import datetime
import win32api

import configuracion
import peticiones


def main():
    Config = configuracion.Iniciar()

    #DEBUG
    #Config.crear(esperar=3)

    dValue = Config.leer()
    if dValue == None:
        print("Error al solicitar la lectura de las configuraciones.")
        return 1

    update, servidores = dValue

    for servidor in servidores["servidores"]:
        tiempo = peticiones.obtener_ntp(servidor)
        if tiempo is not None:
            tiempo_utc = datetime.datetime.utcfromtimestamp(tiempo)
            win32api.SetSystemTime(tiempo_utc.year,
                                   tiempo_utc.month,
                                   tiempo_utc.weekday(),
                                   tiempo_utc.day,
                                   tiempo_utc.hour,
                                   tiempo_utc.minute,
                                   tiempo_utc.second,
                                   0)
            tiempo_local = datetime.datetime.fromtimestamp(tiempo)
            print("Tiempo actualizado a: " + tiempo_local.strftime("(%d-%m-%Y | %H:%M %p)") + " desde \"%s\"" % servidor)
            break
        else:
            print("No se pudo encontrar el servidor: " + servidor)


if __name__ == "__main__":
    sys.exit(main())
