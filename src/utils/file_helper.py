import PyPDF2
import easyocr
import numpy as np
from PIL import Image
from io import BytesIO

# Inicializamos el lector (esto descargará los modelos la primera vez)
reader = easyocr.Reader(['es']) 

def extraer_texto_universal(archivo_storage) -> str:
    nombre_archivo = archivo_storage.filename.lower()
    contenido = archivo_storage.read()
    
    try:
        # 1. Caso: PDF (Sigue igual)
        if nombre_archivo.endswith('.pdf'):
            pdf_file = BytesIO(contenido)
            lector = PyPDF2.PdfReader(pdf_file)
            texto = ""
            for pagina in lector.pages:
                texto += pagina.extract_text() + "\n"
            return texto

        # 2. Caso: Imágenes (EasyOCR)
        elif nombre_archivo.endswith(('.png', '.jpg', '.jpeg')):
            # Convertimos la imagen a un formato que EasyOCR entienda (numpy array)
            imagen = Image.open(BytesIO(contenido))
            imagen_np = np.array(imagen)
            
            # Extraer texto
            resultados = reader.readtext(imagen_np, detail=0) # detail=0 devuelve solo el texto
            return " ".join(resultados)

        # 3. Caso: Texto plano
        elif nombre_archivo.endswith('.txt'):
            return contenido.decode('utf-8')

        else:
            raise Exception("Formato de archivo no soportado")

    except Exception as e:
        raise Exception(f"Error al procesar el archivo {nombre_archivo}: {str(e)}")