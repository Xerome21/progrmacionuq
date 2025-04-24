# Estos son los paquetes que se deben instalar
# pip install pycryptodome
# pip install pyqrcode
# pip install pypng
# pip install pyzbar
# pip install pillow

# No modificar estos módulos que se importan
from pyzbar.pyzbar import decode
from PIL import Image
from json import dumps
from json import loads
from hashlib import sha256
from Crypto.Cipher import AES
import base64
import pyqrcode
from os import urandom
import io
from datetime import datetime

# Nombre del archivo con la base de datos de usuarios
usersFileName="users.txt"

# Fecha actual
date=None
# Clave aleatoria para encriptar el texto de los códigos QR
key=None

# Función para encriptar (no modificar)
def encrypt_AES_GCM(msg, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
    return (ciphertext, aesCipher.nonce, authTag)

# Función para desencriptar (no modificar)
def decrypt_AES_GCM(encryptedMsg, secretKey):
    (ciphertext, nonce, authTag) = encryptedMsg
    aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext

# Función que genera un código QR (no modificar)
def generateQR(id,program,role,buffer):
    # Variables globales para la clave y la fecha
    global key
    global date

    # Información que irá en el código QR, antes de encriptar
    data={'id': id, 'program':program,'role':role}
    datas=dumps(data).encode("utf-8")

    # Si no se ha asignado una clave se genera
    if key is None:
        key =urandom(32) 
        # Se almacena la fecha actual
        date=datetime.today().strftime('%Y-%m-%d')
    
    # Si cambió la fecha actual se genera una nueva clave y 
    # se actualiza la fecha
    if date !=datetime.today().strftime('%Y-%m-%d'):
        key =urandom(32) 
        date=datetime.today().strftime('%Y-%m-%d')

    # Se encripta la información
    encrypted = list(encrypt_AES_GCM(datas,key))

    # Se crea un JSON convirtiendo los datos encriptados a base64 para poder usar texto en el QR
    qr_text=dumps({'qr_text0':base64.b64encode(encrypted[0]).decode('ascii'),
                                'qr_text1':base64.b64encode(encrypted[1]).decode('ascii'),
                                'qr_text2':base64.b64encode(encrypted[2]).decode('ascii')})
    
    # Se crea el código QR a partir del JSON
    qrcode = pyqrcode.create(qr_text)

    # Se genera una imagen PNG que se escribe en el buffer                    
    qrcode.png(buffer,scale=8)          


# Se debe codificar esta función
# Argumentos: id (entero), password (cadena), program (cadena) y role (cadena)
# Si el usuario ya existe deber retornar  "User already registered"
# Si el usuario no existe debe registar el usuario en la base de datos y retornar  "User succesfully registered"
def registerUser(id,password,program,role):    
    pass
   
            


#Se debe complementar esta función
# Función que genera el código QR
# retorna el código QR si el id y la contraseña son correctos (usuario registrado)
# Ayuda (debe usar la función generateQR)
def getQR(id,password):
    buffer = io.BytesIO()                    

    # Aquí va su código     
        
    return buffer

# Se debe complementar esta función
# Función que recibe el código QR como PNG
# debe verificar si el QR contiene datos que pueden ser desencriptados con la clave (key), y si el usuario está registrado
# Debe asignar un puesto de parqueadero dentro de los disponibles.
def sendQR(png):

    # Decodifica código QR
    decodedQR = decode(Image.open(io.BytesIO(png)))[0].data.decode('ascii')

    #Convierte el JSON en el texto del código QR a un diccionario
    data=loads(decodedQR)


    # Desencripta con la clave actual, decodificando antes desde base64. Posteriormente convierte a diccionario (generar error si la clave expiró)
    decrypted=loads(decrypt_AES_GCM((base64.b64decode(data["qr_text0"]),base64.b64decode(data["qr_text1"]),base64.b64decode(data["qr_text2"])), key))
    print(decrypted)

    # En este punto la función debe determinar que el texto del código QR corresponde a un usuario registrado.
    # Luego debe verificar qué puestos de parqueadero existen disponibles según el rol, si hay disponibles le debe asignar 
    # un puesto al usuario y retornarlo como una cadena

    spot=""

    return spot
    