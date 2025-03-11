import cv2
import numpy as np

# Definir las dimensiones de la imagen
width, height = 640, 480

# Crear una imagen negra (matriz de ceros)
image = np.zeros((height, width, 3), dtype=np.uint8)

# Definir el tamaño del cuadrado
square_size = 200

# Calcular las coordenadas para centrar el cuadrado
start_x = (width - square_size) // 2
start_y = (height - square_size) // 2
end_x = start_x + square_size
end_y = start_y + square_size

# Dibujar el cuadrado blanco en la imagen
image[start_y:end_y, start_x:end_x] = [127, 127, 0]

# Guardar la imagen en un archivo
cv2.imwrite('cuadrado_centrado.png', image)

# Mostrar la imagen en una ventana
cv2.imshow('Cuadrado Centrado', image)
cv2.waitKey()
cv2.destroyAllWindows()