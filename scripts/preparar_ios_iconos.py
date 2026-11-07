import json, os
from PIL import Image
ruta = "ios/App/App/Assets.xcassets/AppIcon.appiconset"
fuente = Image.open("icono/icon-1024.png").convert("RGB")
cont = json.load(open(os.path.join(ruta, "Contents.json"), encoding="utf-8"))
escritos = 0
for img in cont["images"]:
    fn = img.get("filename")
    if not fn:
        continue
    ancho = float(img.get("size", "1024x1024").split("x")[0])
    escala = float(img.get("scale", "1x").rstrip("x"))
    tam = round(ancho * escala)
    fuente.resize((tam, tam), Image.LANCZOS).save(os.path.join(ruta, fn), "PNG")
    escritos += 1
if escritos == 0:
    raise SystemExit("No se encontró ningún archivo de icono en Contents.json")
print("Iconos escritos:", escritos)
