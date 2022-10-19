import base64
from fastapi import FastAPI
from pydantic import BaseModel

#importaciones para liveness
from app.engine_liveness import get_liveness

# Se crea la instancia de la app con fastapi 
app = FastAPI()


# Se crea la clase para la imagen a recibir
class ImageBase(BaseModel):
    image_data: str


def get_img(image: ImageBase):
    data = image.image_data
    return base64.b64decode(data)


# Se construye el endpoint para liveness
@app.post("/liveness")
def liveness_image(image: ImageBase):

    # TODO: Crear diccionario de errores para que no truene
    
    data = get_img(image)
    label, value = get_liveness(data)

    if label == 1: 
        return {
            "status": 0,
            "person": True,
            "description": "Real person",
            "value": value
        }
    else: 
        return {
            "status": 0,
            "person": False,
            "description": "Fake person",
            "value": value
        }