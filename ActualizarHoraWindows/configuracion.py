import os
import sys
import pathlib
import configparser

from contextlib import closing


class Iniciar(object):

    def __init__(self):
        appdata = os.getenv("APPDATA")
        if appdata == None:
            print("Ocurrio un error al obtener la variable de entorno \"APPDATA\".")
            sys.exit(1)

        self.appdata = pathlib.Path(appdata)

        self.directorio = self.appdata.joinpath("TimeUpdate")
        self.directorio.mkdir(parents=True, exist_ok=True)
        self.archivo = self.directorio.joinpath("config.ini")

        self.lista_servidores = [
            "time.windows.com",
            "ntp.iitb.ac.in",
            "time.nist.gov",
            "pool.ntp.org",
        ]


    def crear(self, intentos=3, esperar=60, servidores=None):
        if servidores == None:
            servidores = self.lista_servidores

        configuracion = configparser.ConfigParser()

        configuracion.add_section("UPDATE")
        configuracion.add_section("SERVIDORES")

        configuracion.set("UPDATE", "intentos", str(intentos))
        configuracion.set("UPDATE", "esperar", str(esperar))

        for x, servidor in enumerate(servidores, 1):
            configuracion.set("SERVIDORES",  str(x), servidor)

        with closing(open(self.archivo, "w")) as f:
            configuracion.write(f)
        
        return True


    def leer(self):
        if not self.archivo.exists():
            print("No se encuentra el archivo de configuración.")
            return None

        configuracion = configparser.ConfigParser()
        configuracion.read(self.archivo)

        uKeys = list(configuracion["UPDATE"].keys())
        uValues = list(configuracion["UPDATE"].values())
        update = dict(zip(uKeys, uValues))
        print(update)

        sValues = list(configuracion["SERVIDORES"].values())
        servidores = {"servidores": sValues}

        return (update, servidores)


#DEBUG
#print(crear_configuracion())
#print(leer_configuracion())
