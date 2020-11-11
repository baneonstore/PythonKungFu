import socket
import struct

def obtener_ntp(direccion):
    TIEMPO_1970 = 2208988800
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mensaje = "\x1b" + 47 * "\0"
    try:
        cliente.settimeout(5.0)
        cliente.sendto( mensaje.encode(), (direccion, 123))
        datos, _ = cliente.recvfrom( 1024 )
        if datos:
            tiempo = struct.unpack( "!12I", datos )[10]
            tiempo -= TIEMPO_1970
            return tiempo
    except socket.timeout:
        return None
