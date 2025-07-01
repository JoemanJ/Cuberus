import requests
import numpy as np
import cv2

def capture_image(cam_url):
    try:
        response = requests.get(cam_url, timeout=5)
        response.raise_for_status()
        img_array = np.frombuffer(response.content, np.uint8)
        image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return image
    except Exception as e:
        print(f"[ERRO] Falha ao capturar imagem: {e}")
        return None