# Instalar el módulo requests haciendo desde una terminal: pip install requests
import requests 


# Función para registrar usuario
def registerUser(url,id,password,program,role):    
    response=requests.post(url+'/register',data=f'id={id}&password={password}&program={program}&role={role}')
    return response.content.decode('utf-8')



# Función para obtener el código QR
def getQR(url,id,password):    
    response=requests.get(url+'/getqr',params=f'id={id}&password={password}')
    if response.status_code == 200:
        return response.content
    else:
        print(f"Error: {response.text}")
        return None
    

# Función para enviar el código QR y así permitir el ingreso
def sendQR(url, qr_text):
    """
    Envía el texto del QR (no la imagen) al servidor.
    """
    endpoint = f"{url}/sendqr"
    try:
        response = requests.post(endpoint, data=qr_text.encode('utf-8'), headers={'Content-Type': 'text/plain'})
        return response.text
    except Exception as e:
        return f"Error al enviar QR: {e}"



