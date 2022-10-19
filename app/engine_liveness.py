import os
import cv2
import numpy as np 

# importaciones para el modelo 
from app.fas_utils.src.anti_spoof_predict import AntiSpoofPredict
from app.fas_utils.src.generate_patches import CropImage
from app.fas_utils.src.utility import parse_model_name

def get_liveness(image_name: bytes, model_dir = './app/fas_utils/resources/anti_spoof_models', device_id = 0):

    model_test = AntiSpoofPredict(device_id)
    image_croper = CropImage()

    # numpy image
    np_image = np.fromstring(image_name, dtype=np.uint8)  # type: ignore
    image = cv2.imdecode(np_image, 1)

    image_bbox = model_test.get_bbox(image)
    prediction = np.zeros((1, 3))

    for model_name in os.listdir(model_dir):
        h_input, w_input, model_type, scale = parse_model_name(model_name)

        param = {
            "org_img": image,
            "bbox": image_bbox,
            "scale": scale, 
            "out_w": w_input,
            "out_h": h_input,
            "crop": True,
        }

        if scale is None:
            param["crop"] = False
        
        img = image_croper.crop(**param)
        prediction += model_test.predict(img, os.path.join(model_dir, model_name))
    
    # dibujando resultados de la prediccion 
    label = np.argmax(prediction)
    value = prediction[0][label]/2

    return label, value
