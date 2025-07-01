# src/main.py

from capture import capture_image
import cv2

def main():
    cam_url = "http://localhost:8080/cubo3.jpeg"

    print(f"[INFO] Testando captura da URL: {cam_url}")
    img = capture_image(cam_url)

    if img is None:
        print("[ERRO] A captura falhou.")
        return

    print(f"[INFO] Captura bem-sucedida. Dimensões: {img.shape}")
    cv2.imshow("Imagem capturada", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
