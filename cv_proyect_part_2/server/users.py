from pyzbar.pyzbar import decode
from PIL import Image
from json import dumps
from json import loads
from hashlib import sha256
from Crypto.Cipher import AES
import base64
import qrcode
from os import urandom
import io
from datetime import datetime, time

# Nombre del archivo con la base de datos de usuarios
usersFileName = "users.txt"
# Archivo para rastrear los QRs activos
active_qrs_file = "active_qrs.json"

# Fecha actual
date = None
# Clave aleatoria para encriptar el texto de los códigos QR
key = None

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

# Función que genera un código QR
def generateQR(id, program, role, buffer):
    # Variables globales para la clave y la fecha
    global key
    global date
    
    # Información que irá en el código QR, antes de encriptar
    current_datetime = datetime.now()
    qr_id = f"{id}_{current_datetime.strftime('%Y%m%d%H%M%S')}"
    data = {'id': id, 'program': program, 'role': role, 'qr_id': qr_id}
    datas = dumps(data).encode("utf-8")

    # Si no se ha asignado una clave se genera
    if key is None:
        key = urandom(32) 
        # Se almacena la fecha actual
        date = datetime.today().strftime('%Y-%m-%d')
        print(f"Generated encryption key: {key.hex()}")  # Imprime la clave generada

    # Si cambió la fecha actual se genera una nueva clave y 
    # se actualiza la fecha
    if date != datetime.today().strftime('%Y-%m-%d'):
        key = urandom(32) 
        date = datetime.today().strftime('%Y-%m-%d')
        print(f"Updated encryption key: {key.hex()}")  # Imprime la clave actualizada
        # Al cambiar de día, ejecutamos la limpieza de QRs expirados
        cleanup_expired_qrs()

    # Se encripta la información
    encrypted = list(encrypt_AES_GCM(datas, key))

    # Se crea un JSON convirtiendo los datos encriptados a base64 para poder usar texto en el QR
    qr_text = dumps({'qr_text0': base64.b64encode(encrypted[0]).decode('ascii'),
                    'qr_text1': base64.b64encode(encrypted[1]).decode('ascii'),
                    'qr_text2': base64.b64encode(encrypted[2]).decode('ascii')})
    
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
    
    # Registrar el QR como activo con su fecha de expiración
    try:
        with open(active_qrs_file, 'r') as f:
            active_qrs = loads(f.read())
    except FileNotFoundError:
        active_qrs = {}
    
    # Registrar el QR como activo con la fecha actual
    active_qrs[qr_id] = {
        'user_id': id,
        'creation_date': current_datetime.strftime('%Y-%m-%d'),
        'creation_time': current_datetime.strftime('%H:%M:%S')
    }
    
    with open(active_qrs_file, 'w') as f:
        f.write(dumps(active_qrs))
    
    return qr_id

# Función para verificar si un QR sigue siendo válido
def is_qr_valid(qr_id, user_id):
    try:
        # Cargar los QRs activos
        with open(active_qrs_file, 'r') as f:
            active_qrs = loads(f.read())
        
        # Verificar si el QR está en la lista de activos
        if qr_id in active_qrs:
            # Verificar que pertenezca al usuario correcto
            if active_qrs[qr_id]['user_id'] == user_id:
                # Verificar si el QR fue creado hoy
                qr_date = active_qrs[qr_id]['creation_date']
                current_date = datetime.today().strftime('%Y-%m-%d')
                
                return qr_date == current_date
    except FileNotFoundError:
        return False
    
    return False

# Función para invalidar un QR
def invalidate_qr(qr_id):
    try:
        with open(active_qrs_file, 'r') as f:
            active_qrs = loads(f.read())
        
        if qr_id in active_qrs:
            del active_qrs[qr_id]
            
            with open(active_qrs_file, 'w') as f:
                f.write(dumps(active_qrs))
            
            return True
    except FileNotFoundError:
        pass
    
    return False

# Función para limpiar QRs caducados (al final del día)
def cleanup_expired_qrs():
    try:
        current_date = datetime.today().strftime('%Y-%m-%d')
        
        with open(active_qrs_file, 'r') as f:
            active_qrs = loads(f.read())
        
        # Filtrar solo los QRs creados hoy
        valid_qrs = {qr_id: info for qr_id, info in active_qrs.items() 
                    if info['creation_date'] == current_date}
        
        # Guardar solo los QRs válidos
        with open(active_qrs_file, 'w') as f:
            f.write(dumps(valid_qrs))
            
        print(f"Cleaned up {len(active_qrs) - len(valid_qrs)} expired QR codes")
        return len(active_qrs) - len(valid_qrs)  # Número de QRs eliminados
    except FileNotFoundError:
        # Si el archivo no existe, crear uno vacío
        with open(active_qrs_file, 'w') as f:
            f.write(dumps({}))
        return 0

# Función que registra un usuario
def registerUser(id, password, program, role):
    # Forzar un error si el id es 1234 para pruebas de depuración
    if str(id) == "1234":
        raise Exception("Error de prueba: ID 1234 no permitido (debug)")

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
        # Si el archivo no existe, lo creamos
        with open(usersFileName, 'w') as file:
            file.write("")
    
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

# Función que genera el código QR para un usuario
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

# Función que procesa el código QR enviado
def sendQR(qr_text):
    try:
        # qr_text ya es el JSON decodificado del QR
        data = loads(qr_text)

        # Decrypt with the current key, decoding from base64 first
        decrypted = loads(decrypt_AES_GCM((
            base64.b64decode(data["qr_text0"]),
            base64.b64decode(data["qr_text1"]),
            base64.b64decode(data["qr_text2"])
        ), key))
        print("Decrypted QR Code Data:", decrypted)
        
        # Extraer el ID del usuario y el ID único del QR
        user_id = decrypted.get('id')
        qr_id = decrypted.get('qr_id')
        
        # Verificar que el QR sea válido y no haya caducado
        if not is_qr_valid(qr_id, user_id):
            return "QR code expired or invalid"

        # Verify that the user is registered
        try:
            with open(usersFileName, 'r') as file:
                users = file.readlines()
            
            # Search for the user in the database
            user_found = False
            for user in users:
                user_data = loads(user.strip())
                if user_data.get('id') == decrypted.get('id') and user_data.get('program') == decrypted.get('program') and user_data.get('role') == decrypted.get('role'):
                    user_found = True
                    break
            
            if not user_found:
                return "Invalid QR code: User not registered"
            
            # Determine available spots based on the role
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

            # Sincronizar con el estado real de los lugares detectados
            try:
                with open("spots_status.json", "r") as f:
                    spots_status = loads(f.read())
                # Remover lugares ocupados de available_spots
                for role_key in available_spots:
                    available_spots[role_key] = [
                        spot for spot in available_spots[role_key]
                        if not spots_status.get(spot, False)
                    ]
            except FileNotFoundError:
                pass  # Si no existe el archivo, sigue como está

            role = decrypted.get('role').lower()
            assigned_spots_file = "assigned_spots.json"
            scan_state_file = "scan_state.json"

            # Load assigned spots
            try:
                with open(assigned_spots_file, 'r') as f:
                    assigned_spots = loads(f.read())
            except FileNotFoundError:
                assigned_spots = {}

            # Load scan state
            try:
                with open(scan_state_file, 'r') as f:
                    scan_state = loads(f.read())
            except FileNotFoundError:
                scan_state = {}

            user_id_str = str(user_id)

            # Check the scan state of the user
            if user_id_str not in scan_state:
                # First scan: Assign a parking spot
                if role in available_spots and available_spots[role]:
                    spot = available_spots[role].pop(0)
                    assigned_spots[user_id_str] = spot
                    scan_state[user_id_str] = 1  # Mark as first scan (entering)
                    
                    # Save the updated parking spots and scan state
                    with open(available_spots_file, 'w') as f:
                        f.write(dumps(available_spots))
                    with open(assigned_spots_file, 'w') as f:
                        f.write(dumps(assigned_spots))
                    with open(scan_state_file, 'w') as f:
                        f.write(dumps(scan_state))

                    return f"Parking spot assigned: {spot}"
                else:
                    return "No parking spots available for your role"
            elif scan_state[user_id_str] == 1:
                # Second scan: User is leaving, make the spot available again
                if user_id_str in assigned_spots:
                    previous_spot = assigned_spots.pop(user_id_str)
                    available_spots[role].append(previous_spot)
                    # Reiniciamos el estado de escaneo para permitir nuevos ciclos
                    scan_state.pop(user_id_str)  

                    # Save the updated parking spots and scan state
                    with open(available_spots_file, 'w') as f:
                        f.write(dumps(available_spots))
                    with open(assigned_spots_file, 'w') as f:
                        f.write(dumps(assigned_spots))
                    with open(scan_state_file, 'w') as f:
                        f.write(dumps(scan_state))
                    
                    # Invalidar el QR después del segundo escaneo
                    invalidate_qr(qr_id)

                    return f"Spot {previous_spot} is now available again. User has left the building."
                else:
                    return "No assigned parking spot found for this user"
        except FileNotFoundError:
            return "Invalid QR code: User database not found"
            
    except Exception as e:
        return f"Error processing QR code: {str(e)}"