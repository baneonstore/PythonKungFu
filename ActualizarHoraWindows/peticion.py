# Copyright © 2020 baneon - MIT License
# See `LICENSE` included in the source distribution for details.

"""Módulo \"peticion\"
-------------------

\"main\" utiliza este módulo para hacer peticiones a una
lista de servidores.

La lista puede ser creada con el módulo de \"configuracion\".
"""

import socket
import struct

def obtener_ntp(direccion):
    """Args:
        direccion (str): Direccion de un servidor.

    Returns:
        tiempo (int): Devuelve un entero con los datos de la hora.

    Errors:
        None: Tiempo de espera de la petición al servidor expirado.
    """
    TIEMPO_1970 = 2208988800
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mensaje = "\x1b" + 47 * "\0"
    try:
        cliente.settimeout(5.0)
        cliente.sendto(mensaje.encode(), (direccion, 123))
        datos, _ = cliente.recvfrom( 1024 )
        if datos:
            tiempo = struct.unpack( "!12I", datos )[10]
            tiempo -= TIEMPO_1970
            return tiempo
    except socket.timeout:
        return None
