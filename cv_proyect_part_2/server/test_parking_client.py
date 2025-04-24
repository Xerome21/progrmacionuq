import parking_client
# pip install pillow
from PIL import  Image
import io

# Intenta registrar un usuario
id=11111111
password="00000"
program="Electronics Engineering"
role="Student"
url="http://localhost:80"
print(parking_client.registerUser(url,id,password,program,role))


# Solicita un código QR al servidor (los códigos QR cambian cada fecha o cuando se reinicia el servidor)
imgBytes=parking_client.getQR(url,id,password)
# Obtiene un código QR y lo visualiza
image = Image.open(io.BytesIO(imgBytes))
image.show()


parking_client.sendQR(url,"qr.png")


