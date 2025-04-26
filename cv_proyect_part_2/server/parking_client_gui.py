import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import parking_client
import os
import io
from datetime import datetime

# Server URL
SERVER_URL = "http://192.168.1.63:9090"

# Function to register a user
def register_user():
    id = entry_id.get()
    password = entry_password.get()
    program = entry_program.get()
    role = entry_role.get()

    if not id or not password or not program or not role:
        messagebox.showerror("Error", "All fields are required!")
        return

    response = parking_client.registerUser(SERVER_URL, id, password, program, role)
    messagebox.showinfo("Registration", response)

# Function to request a QR code
def request_qr():
    id = entry_id.get()
    password = entry_password.get()

    if not id or not password:
        messagebox.showerror("Error", "ID and Password are required!")
        return

    imgBytes = parking_client.getQR(SERVER_URL, id, password)
    if imgBytes is None:
        messagebox.showerror("Error", "Failed to retrieve QR code: User not found or invalid credentials")
        return

    # Save the QR code
    qr_folder = "C:/Users/kkyto/Desktop/qr_codes/"
    os.makedirs(qr_folder, exist_ok=True)
    qr_filename = f"qr_code_{id}_{int(datetime.now().timestamp())}.png"
    save_path = os.path.join(qr_folder, qr_filename)

    image = Image.open(io.BytesIO(imgBytes))
    image.save(save_path)

    # Display the QR code in the GUI
    qr_image = ImageTk.PhotoImage(image.resize((200, 200)))
    qr_label.config(image=qr_image)
    qr_label.image = qr_image

    messagebox.showinfo("QR Code", f"QR code saved to {save_path}")

# Function to send a QR code
def send_qr():
    qr_file = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
    if not qr_file:
        return

    response = parking_client.sendQR(SERVER_URL, qr_file)
    if response:
        messagebox.showinfo("QR Code Sent", response.decode('utf-8'))
    else:
        messagebox.showerror("Error", "Failed to send QR code")

# Create the main window
root = tk.Tk()
root.title("Parking Client GUI")

# Create input fields for user information
frame_inputs = tk.Frame(root, padx=10, pady=10)
frame_inputs.pack()

tk.Label(frame_inputs, text="ID:").grid(row=0, column=0, sticky="e")
entry_id = tk.Entry(frame_inputs)
entry_id.grid(row=0, column=1)

tk.Label(frame_inputs, text="Password:").grid(row=1, column=0, sticky="e")
entry_password = tk.Entry(frame_inputs, show="*")
entry_password.grid(row=1, column=1)

tk.Label(frame_inputs, text="Program:").grid(row=2, column=0, sticky="e")
entry_program = tk.Entry(frame_inputs)
entry_program.grid(row=2, column=1)

tk.Label(frame_inputs, text="Role:").grid(row=3, column=0, sticky="e")
entry_role = tk.Entry(frame_inputs)
entry_role.grid(row=3, column=1)

# Create buttons for actions
frame_buttons = tk.Frame(root, padx=10, pady=10)
frame_buttons.pack()

btn_register = tk.Button(frame_buttons, text="Register User", command=register_user)
btn_register.grid(row=0, column=0, padx=5)

btn_request_qr = tk.Button(frame_buttons, text="Request QR Code", command=request_qr)
btn_request_qr.grid(row=0, column=1, padx=5)

btn_send_qr = tk.Button(frame_buttons, text="Send QR Code", command=send_qr)
btn_send_qr.grid(row=0, column=2, padx=5)

# Create a label to display the QR code
qr_label = tk.Label(root, text="QR Code will appear here", padx=10, pady=10)
qr_label.pack()

# Run the application
root.mainloop()