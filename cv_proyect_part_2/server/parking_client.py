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
def sendQR(url, qr_image):
    headers = {'Content-type': 'image/png'}
    with open(qr_image, 'rb') as file:
        response = requests.post(url + "/sendqr", data=file, headers=headers)
    
    # Print the server's response
    if response.status_code == 200:
        print("QR Code Information:", response.content.decode('utf-8'))
    else:
        print(f"Error: {response.text}")
    
    return response.content



