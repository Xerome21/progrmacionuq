# Estos son los paquetes que se deben instalar
# pip install pycryptodome
# pip install qrcode[pil]  # Reemplaza a pyqrcode y pypng
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
import qrcode  # Reemplaza a pyqrcode
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

# Función que genera un código QR (modificada para usar qrcode en lugar de pyqrcode)
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
    
    # Se crea el código QR a partir del JSON usando la biblioteca qrcode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=4,
    )
    qr.add_data(qr_text)
    qr.make(fit=True)
    
    # Se genera una imagen PNG que se escribe en el buffer
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(buffer, format="PNG")

# Se debe codificar esta función
# Argumentos: id (entero), password (cadena), program (cadena) y role (cadena)
# Si el usuario ya existe deber retornar  "User already registered"
# Si el usuario no existe debe registar el usuario en la base de datos y retornar  "User succesfully registered"
def registerUser(id,password,program,role):
    try:
        # Intentamos abrir el archivo para ver si existe y leer los usuarios actuales
        with open(usersFileName, 'r') as file:
            users = file.readlines()
        
        # Verificamos si el usuario ya existe
        for user in users:
            user_data = loads(user.strip())
            if user_data.get('id') == id:
                return "User already registered"
    except FileNotFoundError:
        # Si el archivo no existe, creamos una lista vacía de usuarios
        users = []
    
    # Generar hash de la contraseña para almacenarla segura
    password_hash = sha256(password.encode()).hexdigest()
    
    # Crear el nuevo usuario
    new_user = {
        'id': id,
        'password': password_hash,
        'program': program,
        'role': role
    }
    
    # Agregar el usuario al archivo
    with open(usersFileName, 'a') as file:
        file.write(dumps(new_user) + '\n')
    
    return "User succesfully registered"

# Función que genera el código QR
# retorna el código QR si el id y la contraseña son correctos (usuario registrado)
def getQR(id, password):
    buffer = io.BytesIO()
    
    try:
        # Intentamos abrir el archivo para verificar si el usuario existe
        with open(usersFileName, 'r') as file:
            users = file.readlines()
        
        # Verificar que el id y contraseña sean correctos
        password_hash = sha256(password.encode()).hexdigest()
        
        for user in users:
            user_data = loads(user.strip())
            if user_data.get('id') == id and user_data.get('password') == password_hash:
                # Si son correctos, generamos el QR
                generateQR(id, user_data.get('program'), user_data.get('role'), buffer)
                buffer.seek(0)  # Regresamos al inicio del buffer para lectura
                return buffer.getvalue()
        
        # Si no encontramos el usuario, retornamos None
        return None
    except FileNotFoundError:
        # Si el archivo no existe, no hay usuarios registrados
        return None

# Función que recibe el código QR como PNG
# debe verificar si el QR contiene datos que pueden ser desencriptados con la clave (key), y si el usuario está registrado
# Debe asignar un puesto de parqueadero dentro de los disponibles.
def sendQR(png):
    try:
        # Decodifica código QR
        decodedQR = decode(Image.open(io.BytesIO(png)))[0].data.decode('ascii')

        # Convierte el JSON en el texto del código QR a un diccionario
        data = loads(decodedQR)

        # Desencripta con la clave actual, decodificando antes desde base64
        decrypted = loads(decrypt_AES_GCM((
            base64.b64decode(data["qr_text0"]),
            base64.b64decode(data["qr_text1"]),
            base64.b64decode(data["qr_text2"])
        ), key))
        print("Decrypted QR Code Data:", decrypted)

        # Verificar que el usuario esté registrado
        try:
            with open(usersFileName, 'r') as file:
                users = file.readlines()
            
            # Buscar al usuario en la base de datos
            user_found = False
            for user in users:
                user_data = loads(user.strip())
                if user_data.get('id') == decrypted.get('id') and user_data.get('program') == decrypted.get('program') and user_data.get('role') == decrypted.get('role'):
                    user_found = True
                    break
            
            if not user_found:
                return "Invalid QR code: User not registered"
            
            # Determinar qué puestos están disponibles según el rol
            available_spots_file = "available_spots.json"
            try:
                with open(available_spots_file, 'r') as f:
                    available_spots = loads(f.read())
            except FileNotFoundError:
                # Default parking spots if the file doesn't exist
                available_spots = {
                    'student': ['A1', 'A2', 'A3', 'A4', 'A5'],
                    'professor': ['B1', 'B2', 'B3'],
                    'administrative': ['C1', 'C2']
                }

            role = decrypted.get('role').lower()
            if role in available_spots and available_spots[role]:
                # Asignar el primer puesto disponible
                spot = available_spots[role].pop(0)

                # Save the updated parking spots back to the file
                with open(available_spots_file, 'w') as f:
                    f.write(dumps(available_spots))

                return f"Parking spot assigned: {spot}"
            else:
                return "No parking spots available for your role"
                
        except FileNotFoundError:
            return "Invalid QR code: User database not found"
            
    except Exception as e:
        return f"Error processing QR code: {str(e)}"