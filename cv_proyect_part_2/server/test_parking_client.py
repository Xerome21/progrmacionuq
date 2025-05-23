import os
import io  # Import io to handle in-memory file-like objects
from PIL import Image
from datetime import datetime
import parking_client

# User information
id = 1234
password = "yahoo"
program = "economy"
role = "student"
url = "http://192.168.1.63:9090"

# Register the user
print(parking_client.registerUser(url, id, password, program, role))

# Request a QR code from the server
imgBytes = parking_client.getQR(url, id, password)

if imgBytes is None:
    print("Failed to retrieve QR code: User not found or invalid credentials")
else:
    # Save the QR code with a unique name
    qr_folder = "C:/Users/kkyto/Desktop/qr_codes/"
    os.makedirs(qr_folder, exist_ok=True)
    qr_filename = f"qr_code_{id}_{int(datetime.now().timestamp())}.png"
    save_path = os.path.join(qr_folder, qr_filename)

    # Save the QR code
    image = Image.open(io.BytesIO(imgBytes))
    image.save(save_path)
    print(f"QR code saved to {save_path}")

    # Send the QR code to the server
    parking_client.sendQR(url, save_path)




