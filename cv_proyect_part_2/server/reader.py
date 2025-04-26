import os
from pyzbar.pyzbar import decode
from PIL import Image
from json import loads, dumps
from users import decrypt_AES_GCM  # Import the decryption function
import base64

# Folder containing QR codes
qr_folder = "C:/Users/kkyto/Desktop/qr_codes/"
output_folder = "C:/Users/kkyto/Desktop/qr_codes_data/"
decrypted_folder = "C:/Users/kkyto/Desktop/qr_codes_decrypted/"

# Ensure the folders exist
if not os.path.exists(qr_folder):
    print(f"Folder '{qr_folder}' does not exist.")
    exit()

os.makedirs(output_folder, exist_ok=True)
os.makedirs(decrypted_folder, exist_ok=True)

# Encryption key (ensure this matches the key used for encryption)
key = b"your_32_byte_encryption_key_here"  # Replace with your actual key

# Read all QR codes in the folder
for qr_file in os.listdir(qr_folder):
    if qr_file.endswith(".png"):  # Process only PNG files
        qr_path = os.path.join(qr_folder, qr_file)
        try:
            # Decode the QR code
            decoded_data = decode(Image.open(qr_path))
            if decoded_data:
                qr_content = decoded_data[0].data.decode('utf-8')
                print(f"Decoded content from {qr_file}: {qr_content}")  # Debugging

                # Parse the JSON data
                try:
                    qr_info = loads(qr_content)  # Convert JSON string to dictionary
                    # Save the JSON data to a .txt file
                    output_file = os.path.join(output_folder, f"{os.path.splitext(qr_file)[0]}.txt")
                    with open(output_file, "w", encoding="utf-8") as txt_file:
                        txt_file.write(dumps(qr_info, indent=4))
                    print(f"Data saved to {output_file}")
                except Exception as e:
                    print(f"Error parsing JSON from {qr_file}: {e}")
            else:
                print(f"Could not decode QR code in file: {qr_file}")
        except Exception as e:
            print(f"Error reading QR code from file {qr_file}: {e}")

# Decrypt the data in the .txt files
for txt_file in os.listdir(output_folder):
    if txt_file.endswith(".txt"):  # Process only .txt files
        txt_path = os.path.join(output_folder, txt_file)
        try:
            # Read the encrypted data from the .txt file
            with open(txt_path, "r", encoding="utf-8") as file:
                encrypted_data = loads(file.read())

            # Decrypt the data
            try:
                decrypted_data = {
                    key: decrypt_AES_GCM((
                        base64.b64decode(encrypted_data[f"{key}_0"]),
                        base64.b64decode(encrypted_data[f"{key}_1"]),
                        base64.b64decode(encrypted_data[f"{key}_2"])
                    ), key).decode('utf-8')
                    for key in encrypted_data if key.endswith("_0")
                }

                # Save the decrypted data to a new .txt file
                decrypted_file = os.path.join(decrypted_folder, f"decrypted_{txt_file}")
                with open(decrypted_file, "w", encoding="utf-8") as file:
                    file.write(dumps(decrypted_data, indent=4))
                print(f"Decrypted data saved to {decrypted_file}")
            except Exception as e:
                print(f"Error decrypting data in {txt_file}: {e}")
        except Exception as e:
            print(f"Error reading encrypted data from {txt_file}: {e}")