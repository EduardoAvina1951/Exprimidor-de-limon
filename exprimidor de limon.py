from pdf2image import convert_from_path
from PIL import Image
import img2pdf
import os

pdf_entrada = r"C:\Users\LALO\python\Actweek.pdf"
pdf_salida  = r"C:\Users\LALO\python\Actweekmini2.pdf"
poppler_path = r"C:\Users\LALO\python\poppler-24.08.0\Library\bin"

UMBRAL_KB = 150

# Tamaño original PDF KB
size_original = os.path.getsize(pdf_entrada) / 1024

# Convertir a imágenes con menor DPI
imagenes = convert_from_path(pdf_entrada, dpi=150, poppler_path=poppler_path)

print("\n===== DPI detectado por página =====")
for idx, img in enumerate(imagenes):
    print(f"Página {idx+1}: {img.info.get('dpi')}")

imagenes_comprimidas = []

print("\n===== Tamaño de cada página JPG temporal (KB) y ajuste automático =====")
for i, img in enumerate(imagenes):
    ruta_temp = f"temp_{i}.jpg"
    
    # calidad base
    calidad = 170
    img.save(ruta_temp, "JPEG", quality=calidad)
    
    # revisar tamaño
    size_kb = os.path.getsize(ruta_temp) / 1024
    
    if size_kb > UMBRAL_KB:
        # recomprimir con menor calidad solo esta página
        calidad = 25
        img.save(ruta_temp, "JPEG", quality=calidad)
        size_kb = os.path.getsize(ruta_temp) / 1024
        print(f"Página {i+1}: {size_kb:.2f} KB  (reducida calidad a {calidad})")
    else:
        print(f"Página {i+1}: {size_kb:.2f} KB  (calidad {calidad})")
    
    imagenes_comprimidas.append(ruta_temp)

# Crear PDF
with open(pdf_salida, "wb") as f:
    f.write(img2pdf.convert(imagenes_comprimidas))

# Tamaño final PDF KB
size_final = os.path.getsize(pdf_salida) / 1024

# Borrar temporales
for img in imagenes_comprimidas:
    os.remove(img)

print("\n===== RESULTADOS TOTALES =====")
print(f"Tamaño original PDF: {size_original:.2f} KB")
print(f"Tamaño comprimido PDF: {size_final:.2f} KB")

reduccion = ((size_original - size_final) / size_original) * 100
print(f"Reducción total: {reduccion:.2f}%")

print("\n PDF comprimido creado:", pdf_salida)


